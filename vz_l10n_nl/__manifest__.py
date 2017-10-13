# -*- coding: utf-8 -*-
# Copyright 2016 ERP|OPEN (<http://www.erpopen.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'VZ - Chart of accounts',
    'version': '1.0',
    'category': 'Localization',
    'author': 'ERP|OPEN',
    'website': 'http://www.erpopen.nl',
    'depends': [
        'account',
        'base',
        'base_vat',
        'base_iban',
    ],
    'data': [
        'data/account_account_tag.xml',
        'data/account_chart_template_groups.xml',
        'data/account_chart_template.xml',
        'data/account.account.template.xml',
        'data/account_tax_template.xml',
        'data/account_fiscal_position_template.xml',
        'data/account_fiscal_position_tax_template.xml',
        'data/account_fiscal_position_account_template.xml',
        'data/account_chart_template.yml',
        'data/menuitem.xml',
    ],
    'demo': [],
    'auto_install': False,
    'installable': True,
}
