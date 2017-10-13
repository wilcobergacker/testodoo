# -*- coding: utf-8 -*-

{
    'name': "VZ - Custom Reports",
    'summary': """VZ Custom Reports""",
    'author': 'ERP|OPEN',
    'website': 'http://www.erpopen.nl',
    'category': 'Technical Settings',
    'version': '11.0.1.0.0',
    'depends': [
        'account',
        'product',
        'purchase',
        'sale',
        'stock',
        'account_credit_control',
    ],
    'data': [
        'data/report_paperformat.xml',
        'report/templates/account_invoice.xml',
        'report/templates/credit_control.xml',
        'report/templates/purchase_order.xml',
        'report/templates/sale_order.xml',
        'report/templates/purchase_quotation.xml',
        'report/templates/report.xml',
        'report/templates/stock_picking.xml',
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
