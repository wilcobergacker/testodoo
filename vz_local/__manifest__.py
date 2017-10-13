# -*- coding: utf-8 -*-
# Copyright 2016 ERP|OPEN (<http://www.erpopen.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'VZ - Localisation',
    'version': '1.0',
    'category': 'Localization',
    'author': 'ERP|OPEN',
    'website': 'http://www.erpopen.nl',
    'depends': [
        'account',
        'base',
        'base_vat',
        'base_iban',
        'base_partner_sequence',
        'product',
        'stock',
        'l10n_nl_bank',
        'mrp_mps',
        'sale_subscription',
        'delivery',
        'sale_order_type',
        'vz_sale',
    ],
    'data': [
        'data/res_partner.xml',
        'data/res_company_parent.xml',
        'data/res_company.xml',
        'data/res_users.xml',
        'data/sale_subscription.xml',
        'data/product_template.xml',
        'data/account_journal.xml',
        'data/res_partner_suppliers.xml',
        'data/product_supplierinfo.xml',
        'data/sale_order_type.xml'
    ],
    'demo': [],
    'auto_install': False,
    'installable': True,
}
