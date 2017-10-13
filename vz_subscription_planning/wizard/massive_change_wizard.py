# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import timedelta
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
    _name = 'subscription.planning.massive.change'
    _description = 'Change Plan'

    line_id = fields.Many2one('sale.subscription.line', string="Subscription Line")
    date_start = fields.Date(string='Start Date', default=fields.Date.today)
    price = fields.Float('Unit Price', digits=dp.get_precision('Product Price'), default=0.0)
    qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    weekday = fields.Selection(WEEKDAYS, string="Weekday")
    cancel_lines = fields.Boolean('Cancel Planning Lines', default=False)

    @api.multi
    def make_change(self):
        self.ensure_one()

        date = fields.Date.from_string(self.date_start)
        lines = self.env['sale.subscription.planning.line'].search(
            [('subscription_line','=',self.line_id.id), ('date','>=',date)])

        if self.cancel_lines:
            lines.unlink()
        else:
            write_data = {}
            write_data.update({'price': self.price, 'qty': self.qty})
            self.line_id.write({'price_unit': self.price, 'quantity': self.qty})
            if self.weekday:
                self.line_id.day_name = self.weekday
            for line in lines:
                if line.immutable:
                    continue
                new_dict = write_data.copy()
                if self.weekday:
                    new_date = fields.Date.from_string(line.date) + timedelta(self.weekday - fields.Date.from_string(line.date).isoweekday()+1)
                    if new_date >= date:
                        new_dict.update({'date': new_date})
                line.write(new_dict)
        return