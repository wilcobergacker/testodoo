# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Journal Entry import',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'description': """
        Module will import Journal entry with lines from csv data.
    """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['account'],
    'data': [
        'wizard/journal_entry_import_view.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'price': 20,
    'currency': 'EUR',
}
