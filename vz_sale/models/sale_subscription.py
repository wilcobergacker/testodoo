# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    contact_person_id = fields.Many2one('res.partner', 'Contact Person')
    partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address')
    partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address')
    client_order_ref = fields.Char(string="Customer Reference")

    def set_close(self):
        res = super(SaleSubscription, self).write({'state': 'close', 'date': fields.Date.from_string(fields.Date.today())})
        for subscription in self:
            display_products = subscription.recurring_invoice_line_ids.mapped('product_id').filtered(lambda x: x.is_display == True)
            if display_products:
                display_delivered = {}
                for product in display_products:
                    display_delivered[product.id] = 0

                for move_line in subscription.destination_order_id.picking_ids.filtered(lambda x: x.state == 'done' and x.picking_type_id.code in ['incoming','outgoing']).mapped('move_lines').filtered(lambda y: y.product_id in display_products):
                    if move_line.picking_id.picking_type_id.code == 'outgoing':
                        display_delivered[move_line.product_id.id] += move_line.quantity_done
                    else:
                        display_delivered[move_line.product_id.id] -= move_line.quantity_done

                return_moves = []
                for product in display_delivered:
                    if display_delivered[product] > 0:
                        return_moves.append(subscription.destination_order_id.picking_ids.filtered(lambda x: x.state == 'done' and x.picking_type_id.code == 'outgoing').mapped('move_lines').filtered(lambda y: y.product_id.id == product))


                if return_moves:
                    reference_picking = subscription.destination_order_id.picking_ids.filtered(lambda x: x.state == 'done' and x.picking_type_id.code == 'outgoing')[0]
                    picking_type_id = reference_picking.picking_type_id.return_picking_type_id.id
                    return_picking = reference_picking.copy({
                        'move_lines': [],
                        'picking_type_id': picking_type_id,
                        'state': 'draft',
                        'origin': _("Return of displays - Subscription %s") % subscription.code,
                        'location_id': reference_picking.location_dest_id.id,
                        'location_dest_id': reference_picking.location_id.id
                    })
                    for move in return_moves:
                        new_move = move.copy({
                            'product_uom_qty': display_delivered[move.product_id.id],
                            'picking_id': return_picking.id,
                            'state': 'draft',
                            'location_id': return_picking.location_id.id,
                            'location_dest_id': return_picking.location_dest_id.id,
                            'picking_type_id': return_picking.picking_type_id.id,
                            'origin_returned_move_id': None,
                            'procure_method': 'make_to_stock',
                        })

        return res
