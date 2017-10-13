# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _, exceptions
from odoo.addons import decimal_precision as dp
from datetime import timedelta
from odoo.osv import expression
from dateutil.relativedelta import relativedelta
from odoo.tools import pycompat

WEEKDAYS = [_("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), _("Saturday"), _("Sunday")]


class SubscriptionPlanningLine(models.Model):
    _name = "sale.subscription.planning.line"
    _description = "Subscription Planning Line"

    @api.multi
    @api.depends('date', 'product_id', 'planning_id')
    def _get_record_name(self):
        for line in self:
            line.name = line.planning_id.name + ' - ' + line.product_id.name + ' - ' + line.date

    @api.multi
    @api.depends('date')
    def _get_day_name(self):
        for line in self:
            if line.date:
                line.day_name = WEEKDAYS[fields.Date.from_string(line.date).isoweekday()-1]

    @api.multi
    def _get_immutable(self):
        today = fields.Date.from_string(fields.Date.today())
        for line in self:
            if line.date and fields.Date.from_string(line.date) < today + timedelta(2):
                line.immutable = True
            else:
                line.immutable = False

    @api.multi
    def _prepare_order_line(self):
        self.ensure_one()
        company = self.planning_id.subscription_id.origin_order_id.company_id.id
        if self.product_id:
            taxes = self.product_id.taxes_id
        company_taxes = [tax_rec.id for tax_rec in taxes if tax_rec.company_id.id == company]
        values = {
            'name': self.product_id and self.product_id.name,
            'order_id': self.planning_id.subscription_id.origin_order_id.id,
            'product_uom_qty': self.qty,
            'product_id': self.product_id and self.product_id.id or False,
            'product_uom': self.uom_id and self.uom_id.id,
            'price_unit': self.price,
            'company_id': company,
            'tax_id': [(6, 0, company_taxes)],
            'planning_line_id': self.id,
            'delivery_date': self.date,
            'note': self.note,
        }
        return values

    name = fields.Char(string="Name", compute="_get_record_name", store=True)
    planning_id = fields.Many2one('sale.subscription.planning', string="Planning", required=True)
    date = fields.Date(string='Date', required=True)
    day_name = fields.Char("Day Name", compute="_get_day_name", store=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    price = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    changeable = fields.Boolean(compute='_can_be_changed', string="Can Be Changed")
    subscription_line = fields.Many2one('sale.subscription.line', string='Origin Subscription Line')
    order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line")
    destination_order_line_ids = fields.One2many('sale.order.line', 'planning_line_id', 'Destination Order Lines')
    immutable = fields.Boolean(compute="_get_immutable")
    partner_id = fields.Many2one('res.partner', string='Partner', related='planning_id.partner_id', store=True, readonly=True)
    note = fields.Text('Internal Notes')
    change_ids = fields.One2many('sale.subscription.planning.change', 'planning_line_id', string="Changes")

    @api.model
    def create(self, vals):
        return super(SubscriptionPlanningLine, self.with_context(prevent_change_tracking=True)).create(vals)

    @api.multi
    def write(self, vals):
        if not self.env.context.get('prevent_change_tracking', False) and ('product_id' in vals or 'price' in vals or 'date' in vals or 'qty' in vals):
            for line in self:
                self.env['sale.subscription.planning.change'].create({
                    'planning_line_id': line.id,
                    'subscription_line_id': line.subscription_line.id,
                    'old_product_id': line.product_id.id,
                    'new_product_id': vals.get('product_id', False) or line.product_id.id,
                    'old_qty': line.qty,
                    'new_qty': vals.get('qty', False) or line.qty,
                    'old_price': line.price,
                    'new_price': vals.get('price', False) or line.price,
                    'old_date': line.date,
                    'new_date': vals.get('date', False) or line.date,
                })
        return super(SubscriptionPlanningLine, self).write(vals)

    @api.multi
    def adjust_grid(self, row_domain, column_field, column_value, cell_field, change):
        if column_field != 'date' or cell_field != 'qty':
            raise exceptions.UserError(
                _("Grid adjustment for planning lines only supports the "
                  "'date' columns field and the 'qty' cell "
                  "field, got respectively %(column_field)r and "
                  "%(cell_field)r") % {
                    'column_field': column_field,
                    'cell_field': cell_field,
                }
            )

        from_, to_ = pycompat.imap(fields.Date.from_string, column_value.split('/'))
        start = fields.Date.to_string(from_)
        # range is half-open get the actual end date
        end = fields.Date.to_string(to_ - relativedelta(days=1))

        if start != end:
            raise exceptions.UserError(
                _("Grid adjustment for planning lines only supports "
                  "'date' columns which cover single day periods"))

        # see if this change is on a date within 2 days
        day_limit = fields.Date.from_string(fields.Date.today()) + relativedelta(days=2)
        if from_ <= day_limit:
            raise exceptions.UserError(
                _("Adjustments are not allowed for planning lines closer than 2 days from now")
            )

        # see if there is an exact match
        cell = self.search(expression.AND([row_domain, [
            ['date', '=', start]
        ]]), limit=1)
        # if so, adjust in-place
        if cell:
            cell[cell_field] += change
            return False

        # otherwise copy an existing cell from the row, ignore eventual
        # non-monthly forecast
        self.search(row_domain, limit=1).ensure_one().copy({
            'date': start,
            cell_field: change,
        })
        return False


class SubscriptionPlanning(models.Model):
    _name = "sale.subscription.planning"
    _description = "Subscription Planning"

    name = fields.Char("Name")
    subscription_id = fields.Many2one('sale.subscription', string="Subscription")
    partner_id = fields.Many2one('res.partner', string='Partner', related='subscription_id.partner_id', readonly=True)
    active = fields.Boolean(default=True)
    date_start = fields.Date(string='Start Date', default=fields.Date.today)
    line_ids = fields.One2many('sale.subscription.planning.line', 'planning_id', string="Planning Lines")

