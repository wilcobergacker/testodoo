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
    
class stock_move(models.Model):
    _inherit = 'stock.move'
    
    delivery_date = fields.Date('Delivery Date')
    
    def _get_new_picking_values(self):
        res=super(stock_move,self)._get_new_picking_values()
        res.update({'delivery_date':self.delivery_date})
        return res
        
    def _assign_picking(self):
        """ Try to assign the moves to an existing picking that has not been
        reserved yet and has the same procurement group, locations and picking
        type (moves should already have them identical). Otherwise, create a new
        picking to assign them to. """
        Picking = self.env['stock.picking']
        for move in self:
            recompute = False
            picking = Picking.search([
                ('group_id', '=', move.group_id.id),
                ('location_id', '=', move.location_id.id),
                ('location_dest_id', '=', move.location_dest_id.id),
                ('picking_type_id', '=', move.picking_type_id.id),
                ('printed', '=', False),
                ('delivery_date','=',move.delivery_date),
                ('state', 'in', ['draft', 'confirmed', 'waiting', 'partially_available', 'assigned'])], limit=1)
            if not picking:
                recompute = True
                picking = Picking.create(move._get_new_picking_values())
            move.write({'picking_id': picking.id})

            # If this method is called in batch by a write on a one2many and
            # at some point had to create a picking, some next iterations could
            # try to find back the created picking. As we look for it by searching
            # on some computed fields, we have to force a recompute, else the
            # record won't be found.
            if recompute:
                move.recompute()
        return True
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
    
    
        
