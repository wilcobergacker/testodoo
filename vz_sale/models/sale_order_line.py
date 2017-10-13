# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_product_id_check_availability(self):
        return
