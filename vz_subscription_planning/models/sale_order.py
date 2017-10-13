# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        for order in self:
            if order.state == 'waiting_route':
                if order.carrier_id and order.partner_id.property_delivery_carrier_id:
                    super(SaleOrder, order).action_confirm()
                else:
                    raise UserError(_('To confirm this SO, you must fill "Carrier" field both on the SO and on the related partner'))
            else:
                order.state = 'waiting_route'
        return True

    @api.multi
    @api.depends('order_line','order_line.subscription_id','order_line.subscription_id.state')
    def _can_lock(self):
        for order in self:
            if len(order.order_line.mapped('subscription_id').filtered(lambda x: x.state == 'open')) > 0:
                order.can_lock = False
            else:
                order.can_lock = True

    can_lock = fields.Boolean(compute="_can_lock")
    state = fields.Selection(selection_add=[('waiting_route', _('Waiting for Route'))])

    def _prepare_subscription_data(self, template):
        res = super(SaleOrder, self)._prepare_subscription_data(template)
        res.update({'state':'draft', 'client_order_ref': self.display_client_order_ref, 'origin_order_id': self.id})
        return res

    def create_subscriptions(self):
        res = super(SaleOrder, self).create_subscriptions()
        #self.env['sale.subscription'].browse(res).create_planning()
        self.env['sale.subscription'].browse(res).set_open()
        return res

    @api.model
    def create(self, vals):
        return super(SaleOrder, self).create(vals)

