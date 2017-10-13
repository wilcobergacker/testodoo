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

class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'
    
    
    delivery_date = fields.Date('Delivery Date')

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        res = super(ProcurementRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
        res.update({'delivery_date': self.env.context.get('delivery_date', res.get('date_expected')), 'date_expected': self.env.context.get('delivery_date', res.get('date_expected'))})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
    
    
        
