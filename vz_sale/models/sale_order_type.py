# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    create_subscription = fields.Boolean('Create Subscription', default=False)
    lock_order = fields.Boolean('Lock Order')