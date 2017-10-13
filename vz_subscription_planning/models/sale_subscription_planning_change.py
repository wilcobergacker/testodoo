# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _, exceptions
from odoo.addons import decimal_precision as dp

WEEKDAYS = [_("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), _("Saturday"), _("Sunday")]


class SubscriptionPlanningChange(models.Model):
    _name = "sale.subscription.planning.change"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Subscription Planning Line"

    @api.multi
    @api.depends('planning_line_id', 'planning_line_id.name')
    def _get_record_name(self):
        for change in self:
            change.name = _("Change on %s" % change.planning_line_id.name)

    @api.multi
    @api.depends('old_date', 'new_date', 'old_date', 'new_date', 'old_product_id', 'new_product_id', 'old_price', 'new_price', 'old_qty', 'new_qty')
    def _get_changes(self):
        for line in self:
            description = ''
            if line.old_date != line.new_date:
                description += _("Date changed from: %s to %s; " % (line.old_date, line.new_date))
                line.date_changed = True
            if line.old_product_id != line.new_product_id:
                description += _("Product changed from: %s to %s; " % (line.old_product_id, line.new_product_id))
                line.product_id_changed = True
            if line.old_price != line.new_price:
                description += _("Price changed from: %s to %s; " % (line.old_price, line.new_price))
                line.price_changed = True
            if line.old_qty != line.new_qty:
                description += _("Quantity changed from: %s to %s; " % (line.old_qty, line.new_qty))
                line.qty_changed = True
            line.description = description

    name = fields.Char("Name", compute="_get_record_name")

    subscription_line_id = fields.Many2one('sale.subscription.line')
    planning_line_id = fields.Many2one('sale.subscription.planning.line')

    old_date = fields.Date(string='Old Date')
    new_date = fields.Date(string='New Date')
    date_changed = fields.Boolean(string='Date Changed', store=True, compute="_get_changes")

    old_product_id = fields.Many2one('product.product', string='Old Product')
    new_product_id = fields.Many2one('product.product', string='New Product')
    product_id_changed = fields.Boolean(string='Product Changed', store=True, compute="_get_changes")

    old_price = fields.Float('Old Unit Price', digits=dp.get_precision('Product Price'))
    new_price = fields.Float('New Unit Price', digits=dp.get_precision('Product Price'))
    price_changed = fields.Boolean(string='Price Changed', store=True, compute="_get_changes")

    old_qty = fields.Float(string='Old Quantity', digits=dp.get_precision('Product Unit of Measure'))
    new_qty = fields.Float(string='New Quantity', digits=dp.get_precision('Product Unit of Measure'))
    qty_changed = fields.Boolean(string='Quantity Changed', store=True, compute="_get_changes")

    description = fields.Text('Description', store=True, compute="_get_changes")
