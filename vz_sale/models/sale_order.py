# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    display_client_order_ref = fields.Char(compute='_compute_client_order_ref', inverse='_inverse_client_order_ref', string="Customer Reference")
    po_expire = fields.Date('PO Expire')
    po_expire_warned = fields.Boolean('PO Expire Warned', default=False)
    contact_person_id = fields.Many2one('res.partner', 'Contact Person')

    @api.depends('client_order_ref')
    def _compute_client_order_ref(self):
        for order in self:
            order.display_client_order_ref = order.client_order_ref

    def _inverse_client_order_ref(self):
        for order in self:
            if order.display_client_order_ref != order.client_order_ref:
                order.client_order_ref = order.display_client_order_ref

    @api.multi
    def write(self, values):
        res = super(SaleOrder, self).write(values)
        if 'client_order_ref' in values:
            self.mapped('order_line').mapped('subscription_id').write({'client_order_ref': values['client_order_ref']})
        if 'partner_invoice_id' in values:
            self.mapped('order_line').mapped('subscription_id').write({'partner_invoice_id': values['partner_invoice_id']})
        if 'partner_shipping_id' in values:
            self.mapped('order_line').mapped('subscription_id').write({'partner_shipping_id': values['partner_shipping_id']})
        return res


    def _prepare_subscription_data(self, template=None):
        self.ensure_one()
        res = super(SaleOrder, self)._prepare_subscription_data(template=template)
        res.update({
            'partner_shipping_id': self.partner_shipping_id.id,
            'partner_invoice_id': self.partner_invoice_id.id,
            'client_order_ref': self.client_order_ref,
        })
        if self.contact_person_id:
            res.update({
                'contact_person_id': self.contact_person_id.id,
            })
        return res

    def create_subscriptions(self):
        res = []
        for order in self:
            if order.type_id and order.type_id.create_subscription:
                res += super(SaleOrder, order).create_subscriptions()
        return res
