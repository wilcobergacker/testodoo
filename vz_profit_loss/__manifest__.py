# -*- coding: utf-8 -*-
# Copyright 2016 ERP|OPEN (<http://www.erpopen.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "VZ - Profit & Loss",
    'summary': """VZ Profit & Loss""",
    'author': 'ERP|OPEN',
    'website': 'http://www.erpopen.nl',
    'category': 'Technical Settings',
    'version': '11.0.1.0.0',
    'depends': [
        'account',
        'account_reports',
    ],
    'data': [
        'data/vz_profit_loss.xml',
    ],
}
