# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import csv
import tempfile


class journal_entry_import(models.TransientModel):
    _name = 'journal.entry.import'

    file = fields.Binary('File')

    @api.model
    def check_data(self, line, count):
        if len(line) < 9:
            raise UserError(_(
                'Error!\n' +
                'Selected CSV File Does have columns < 10!'))
        if not line[4] or not line[5] or not line[6] or not line[7] or not\
                line[8]:
            raise UserError(_(
                'Error!\n'
                'Value is not proper, Please check CSV line %d') % (count + 1))

    @api.multi
    def read_file(self):
        data_dict = {}
        account_journal = self.env['account.journal']
        partner_obj = self.env['res.partner']
        account_obj = self.env['account.account']
        file_path = tempfile.gettempdir() + '/journal_import.csv'
        f = open(file_path, 'wb')
        f.write(self.file.decode('base64'))
        f.close()
        move_line = []
        line_count = 0
        partner_dict, account_dict = {}, {}
        data_reader = csv.reader(open(file_path))
        for line in data_reader:
            line_dict = {}
            if line_count == 0:
                line_count += 1
                continue
            self.check_data(line, line_count)
            if line_count == 1:
                journal = account_journal.search([('name', '=', line[0])],
                                                 limit=1)
                if journal:
                    data_dict['journal_id'] = journal.id
                data_dict['ref'] = line[1]
                data_dict['date'] = line[2]
                data_dict['narration'] = line[3]
#             account.move.line
            line_dict['name'] = line[1]
            if not partner_dict.get(line[4]):
                partner = partner_obj.search([('ref', '=', line[4])], limit=1)
                if partner:
                    line_dict['partner_id'] = partner.id
                    partner_dict[line[4]] = partner.id
                else:
                    raise UserError(_(
                        'Error!\n'
                        'No record found for partner with ref %s') % (line[4]))
            elif partner_dict.get(line[4]):
                line_dict['partner_id'] = partner_dict.get(line[4])

            if not account_dict.get(line[5]):
                account = account_obj.search([('code', '=', line[5])], limit=1)
                if account:
                    line_dict['account_id'] = account.id
                    account_dict[line[5]] = account.id
                else:
                    raise UserError(_(
                        'Error!\n'
                        'No record found for Account with ref %s') % (line[5]))
            elif account_dict.get(line[5]):
                line_dict['account_id'] = account_dict.get(line[5])
            line_dict['debit'] = float(line[6])
            line_dict['credit'] = float(line[7])
            line_dict['date_maturity'] = line[8]
            move_line.append((0, 0, line_dict))
            line_count += 1
        data_dict['line_ids'] = move_line
        return data_dict

    @api.multi
    def import_csv(self):
        vals = self.read_file()
        move = self.env['account.move'].create(vals)
        domain = [('id', 'in', [move.id])]
        return {
            'domain': domain,
            'name': 'Imported Journal Entries',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window'
        }
