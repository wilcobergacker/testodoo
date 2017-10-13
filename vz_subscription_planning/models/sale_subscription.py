# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from datetime import timedelta


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    @api.multi
    def _planning_line_count(self):
        for subscription in self:
            subscription.planning_line_count = len(subscription.planning_id.line_ids.ids)

    @api.multi
    def _change_line_count(self):
        for subscription in self:
            lines = subscription.recurring_invoice_line_ids.mapped('change_ids')
            subscription.change_line_count = len(lines.ids)

    origin_order_id = fields.Many2one('sale.order', string='Origin Sale Order')
    planning_id = fields.Many2one('sale.subscription.planning', string="Planning")
    planning_line_count = fields.Integer(string='# of Planning Lines', compute='_planning_line_count')
    change_line_count = fields.Integer(string='# of Planning Changes', compute='_change_line_count')

    @api.model
    def _cron_create_lines_from_planning(self):
        self.search([('planning_id','!=',False),('state','=','open'),('origin_order_id','!=',False)]).create_lines_from_planning()

    @api.multi
    def create_lines_from_planning(self):
        today = fields.Date.from_string(fields.Date.today())
        day_limit = today + timedelta(1)
        for subscription in self:
            for line in subscription.planning_id.line_ids.filtered(lambda x: not x.order_line_id and fields.Date.from_string(x.date) >= today and fields.Date.from_string(x.date) < day_limit):
                line_data = line._prepare_order_line()
                line_id = self.env['sale.order.line'].create(line_data)
                line.order_line_id = line_id
        return True

    @api.multi
    def set_open(self):
        self.create_planning()
        res = super(SaleSubscription, self).set_open()
        self.mapped('origin_order_id').action_unlock()
        for subscription in self:
            if subscription.planning_id:
                subscription.sudo().create_lines_from_planning()
        return res

    def set_close(self):
        res = super(SaleSubscription, self).set_close()
        today = fields.Date.from_string(fields.Date.today())
        self.mapped('origin_order_id').action_done()
        for subscription in self.filtered(lambda x: x.planning_id):
            subscription.planning_id.line_ids.filtered(lambda y: fields.Date.from_string(y.date) >= today).unlink()
        return res

    def set_cancel(self):
        res = super(SaleSubscription, self).set_cancel()
        today = fields.Date.from_string(fields.Date.today())
        self.mapped('origin_order_id').action_done()
        for subscription in self.filtered(lambda x: x.planning_id):
            subscription.planning_id.line_ids.filtered(lambda y: fields.Date.from_string(y.date) >= today).unlink()
        return res

    def set_close(self):
        res = super(SaleSubscription, self).set_cancel()
        today = fields.Date.from_string(fields.Date.today())
        self.mapped('origin_order_id').action_done()
        for subscription in self.filtered(lambda x: x.planning_id):
            subscription.planning_id.line_ids.filtered(lambda y: fields.Date.from_string(y.date) > today).unlink()
        return res

    @api.multi
    def action_open_changes(self):
        lines = self.recurring_invoice_line_ids.mapped('change_ids')
        action = self.env.ref('vz_subscription_planning.subscription_planning_change_action').read()[0]
        if len(lines) >= 1:
            action['domain'] = [('id', 'in', lines.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_open_planning(self):
        lines = self.mapped('planning_id').mapped('line_ids')
        action = self.env.ref('vz_subscription_planning.subscription_planning_line_action').read()[0]
        if len(lines) >= 1:
            action['domain'] = [('id', 'in', lines.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def _prepare_destination_order_data(self):
        self.ensure_one()
        data = {
            'partner_id': self.partner_id.id,
            'contact_person_id': self.contact_person_id.id,
            'partner_invoice_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'user_id': self.partner_id.user_id.id or self.env.uid,
            'fiscal_position_id': self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id, self.partner_shipping_id.id),
            'type_id': self.partner_id.sale_type and self.partner_id.sale_type.id or False,
            'team_id': self.partner_id.team_id and self.partner_id.team_id.id or False,
        }

        if self.env['ir.config_parameter'].sudo().get_param('sale.use_sale_note') and self.env.user.company_id.sale_note:
            data['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note
        return data

    def _prepare_subscription_planning_data(self):
        self.ensure_one()
        values = {
            'name': self.code,
            'date_start': fields.Date.from_string(self.date_start),
            'subscription_id': self.id,
        }
        sub_lines = self.recurring_invoice_line_ids
        max_date = fields.Date.from_string(self.date_start) + timedelta(365)
        line_data = list()
        for subscription_line in sub_lines:
            line = subscription_line.origin_sale_order_line_id
            product = line.product_id.id
            price = line.price_unit
            qty = line.product_uom_qty
            uom = line.product_uom.id
            ref_date = fields.Date.from_string(line.delivery_date)

            for i in range(0, 52):
                new_date = ref_date + timedelta(days=(i * 7))
                if new_date <= max_date:
                    line_data.append((0, False, {
                        'product_id': product,
                        'date': new_date,
                        'price': price,
                        'qty': qty,
                        'uom_id': uom,
                        'subscription_line': subscription_line.id,
                    }))
                else:
                    break
        values['line_ids'] = line_data
        planning_id = self.env['sale.subscription.planning'].create(values)
        return planning_id

    @api.multi
    def create_planning(self):
        for subscription in self:
            subscription.planning_id = subscription._prepare_subscription_planning_data()