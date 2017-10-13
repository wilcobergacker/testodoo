# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd. (<http://devintellecs.com>).
#
##############################################################################
{
    "name": "Sale Delivery by Dates",
    "version": '1.0',
    "sequence": 1,
    "category": 'Sale',
    "summary": """
                 Apps will create different delivery order for sale order based on given delivery date on sale order line
        """,
    "description": """
        Apps will create different delivery order for sale order based on given delivery date on sale order line
    """,
    "author": "DevIntelle Consulting Service Pvt.Ltd",
    "website": "http://www.devintellecs.com",
    "images": ['images/main_screenshot.png'],
    "depends": ['sale_stock'],
    "data": [
        'views/sale_order.xml',
        #'views/procurement_order_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable' : True,
	'auto_install' : False,	
	'application' : True,
    "price":30.0,
    "currency":'EUR',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
