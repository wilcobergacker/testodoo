# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class TemporarySubscriptionBlock(models.TransientModel):
    _name = 'subscription.planning.temporary.block'
    _description = 'Temporary Subscription Block'

    partner_id = fields.Many2one('res.partner', 'Partner')
    subscription_ids = fields.Many2many('sale.subscription', 'temporary_block_subscription_rel')
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    @api.multi
    def set_block(self):
        self.ensure_one()

        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)

        if self.subscription_ids:
            subscriptions = self.subscription_ids
        else:
            subscriptions = self.env['sale.subscription'].search([])

        if self.partner_id:
            subscriptions = subscriptions.filtered(lambda x: x.partner_id == self.partner_id)

        if subscriptions:
            planning_lines = self.env['sale.subscription.planning.line'].search([('planning_id.subscription_id','in',subscriptions.ids),('date','>=',start_date)('date','<=',end_date)])
            planning_lines.unlink()
            return

        return

    @api.constrains('start_date','end_date')
    def _check_dates(self):
        for wizard in self:
            today = fields.Date.from_string(fields.Date.today())
            start_date = fields.Date.from_string(wizard.start_date)
            end_date = fields.Date.from_string(wizard.end_date)

            if start_date > end_date:
                raise ValidationError(_('Error ! Start date must precede end date.'))
            if start_date <= today + relativedelta(days=2):
                raise ValidationError(_('Error ! You cannot set temporary blocks for plans within next 2 days.'))

