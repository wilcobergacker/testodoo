# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = 'order_id, delivery_date DESC, layout_category_id, sequence, id'

    planning_line_id = fields.Many2one('sale.subscription.planning.line', 'Planning Line')
    note = fields.Text('Internal Notes')

    def _prepare_subscription_line_data(self):
        """Prepare a dictionnary of values to add lines to a subscription."""
        values = list()
        for line in self:
            values.append((0, False, {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_uom_qty,
                'uom_id': line.product_uom.id,
                'price_unit': line.price_unit,
                'discount': line.discount if line.order_id.subscription_management != 'upsell' else False,
                'start_date': line.delivery_date,
                'day_name': fields.Date.from_string(line.delivery_date).isoweekday()-1,
                'origin_sale_order_line_id': line.id,
            }))
        return values