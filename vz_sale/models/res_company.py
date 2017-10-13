# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta
from odoo import api, models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    po_number_expire_mail_template = fields.Many2one('mail.template','PO Number Expiring Mail Template', domain=lambda self: [("model_id", "=", self.env.ref('sale.model_sale_order').id)])
    po_number_expire_days_advance = fields.Integer('PO Number Expiring Warning Days')

    @api.model
    def _cron_warn_po_expiring(self):
        self.search([('po_number_expire_mail_template','!=',False)]).warn_po_expiring()

    @api.multi
    def warn_po_expiring(self):
        today = fields.Date.from_string(fields.Date.today())
        for company in self:
            day_limit = today + timedelta(company.po_number_expire_days_advance or 0)
            orders_to_warn = self.env['sale.order'].search([('po_expire_warned','=',False),('state','not in',['draft','cancel']),('po_expire','<=',day_limit)])
            for order in orders_to_warn:
                company.po_number_expire_mail_template.send_mail(order.id, force_send=True)
            orders_to_warn.write({'po_expire_warned': True})
        return True
