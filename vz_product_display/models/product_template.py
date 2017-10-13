# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, models, tools, fields, _, SUPERUSER_ID
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_display = fields.Boolean('Is Display', default=False)
