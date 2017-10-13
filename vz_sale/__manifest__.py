# -*- coding: utf-8 -*-
{
    'name': 'VZ - Sale',
    'version': '11.0.1.0.0',
    'category': 'Generic Module',
    'summary': 'Sale customization',
    'author': 'ERP|OPEN',
    'depends': [
        'sale',
        'sale_subscription',
        'sale_order_type',
        'sale_order_dates',
        'sale_stock',
        'sale_subscription_asset',
        'vz_product_display',
    ],
    'data': [
        'data/ir_cron.xml',
        'views/sale_order.xml',
        'views/sale_subscription.xml',
        'views/sale_order_type.xml',
        'views/res_company.xml',
    ],
    'installable': True,
}