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

class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    delivery_date = fields.Date('Delivery Date')
    
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
    
    
        
