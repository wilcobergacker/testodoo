# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

WEEKDAYS = [
    (0, _("Monday")),
    (1, _("Tuesday")),
    (2, _("Wednesday")),
    (3, _("Thursday")),
    (4, _("Friday")),
    (5, _("Saturday")),
    (6, _("Sunday")),
]


class SaleSubscriptionPlanningMassiveChange(models.TransientModel):
    _name = 'subscription.planning.multi.massive.change'
    _description = 'Change Plan'

    planning_line_ids = fields.Many2many('sale.subscription.planning.line', 'planning_line_massive_change_wizard_rel', string="Planning Lines")
    date = fields.Date(string='Date')
    price = fields.Float('Unit Price', digits=dp.get_precision('Product Price'), default=0.0)
    qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    change_price = fields.Boolean()
    change_qty = fields.Boolean()
    change_date = fields.Boolean()

    @api.multi
    def make_change(self):
        self.ensure_one()

        lines = self.planning_line_ids

        write_data = {}
        if self.change_price:
            write_data.update({'price': self.price})
        if self.change_qty:
            write_data.update({'qty': self.qty})
        if self.change_date:
            write_data.update({'date': self.date})
        lines.write(write_data)
        return