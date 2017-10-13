# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://devintellecs.com>).
#
##############################################################################
#
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import sys
from datetime import datetime
from time import mktime, strptime
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    
    delivery_date = fields.Date('Delivery Date', default=fields.Datetime.now, required=True)
        
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.order_id:
                self.delivery_date = self.order_id.date_order

    @api.multi
    def _action_launch_procurement_rule(self):
        for line in self:
            super(SaleOrderLine, line.with_context(delivery_date=line.delivery_date))._action_launch_procurement_rule()
        return True


    @api.multi
    def _prepare_procurement_values (self, group_id):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id=group_id)
        res.update({'delivery_date':self.delivery_date})
        return res
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
    
    
        
