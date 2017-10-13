# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.depends('attribute_value_ids.price_ids.price_extra', 'attribute_value_ids.price_ids.product_tmpl_id')
    def _compute_product_price_extra(self):
        result = {}
        for product in self:
            price_extra = 0.0
            for variant_id in product.attribute_value_ids:
                for price_id in variant_id.price_ids:
                    if price_id.product_tmpl_id.id == product.product_tmpl_id.id:
                        price_extra += price_id.price_extra
            product.price_extra = price_extra + product.wk_extra_price
            product.attr_price_extra = price_extra

    wk_extra_price = fields.Float('Price Extra')
    price_extra = fields.Float(string='Variant Extra Price', compute='_compute_product_price_extra',
                               help="This shows the sum of all attribute price and additional price of variant (All Attribute Price+Additional Variant price)", digits=dp.get_precision('Product Price'))

    attr_price_extra = fields.Float(compute='_compute_product_price_extra',
                                    string='Variant Extra Price', digits_compute=dp.get_precision('Product Price'))
