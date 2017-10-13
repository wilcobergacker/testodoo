# -*- coding: utf-8 -*-
# © 2017 ERP|OPEN (http://www.erpopen.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools, fields, _

WEEKDAYS = [
    (0, _("Monday")),
    (1, _("Tuesday")),
    (2, _("Wednesday")),
    (3, _("Thursday")),
    (4, _("Friday")),
    (5, _("Saturday")),
    (6, _("Sunday")),
]


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    @api.multi
    def _has_planning_line(self):
        for line in self:
            if self.env['sale.subscription.planning.line'].search([('subscription_line','=',line.id)], limit=1):
                line.has_planning_line = True
            else:
                line.has_planning_line = False

    day_name = fields.Selection(WEEKDAYS, "Day Name")
    start_date = fields.Date(string='Start Date')
    origin_sale_order_line_id = fields.Many2one('sale.order.line', 'Origin Sale Order Line')
    has_planning_line = fields.Boolean('Planning Related', compute="_has_planning_line")
    change_ids = fields.One2many('sale.subscription.planning.change', 'subscription_line_id', string="Changes")

    @api.multi
    def action_make_change(self):
        self.ensure_one()
        action = self.env.ref('vz_subscription_planning.action_view_planning_massive_change').read()[0]
        action['context'] = "{'default_line_id': %s, 'default_price': %s, 'default_qty': %s, 'default_weekday': %s}" % (self.id, self.price_unit, self.quantity, self.day_name)
        return action
