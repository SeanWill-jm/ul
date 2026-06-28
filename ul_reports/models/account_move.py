from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    ul_location = fields.Char(string='Location', copy=False)
    ul_ship_via = fields.Char(string='Ship Via', copy=False)
    ul_account_no = fields.Char(string='Account No', copy=False)
    ul_other_info = fields.Char(string='Other Info', copy=False)

    def action_invoice_download_pdf(self, target="download"):
        """ Override to print the custom invoice report if company != 3. """
        if len(self) == 1 and self.company_id.id != 3:
            return self.env.ref('ul_reports.action_report_ul_invoice').report_action(self)
        
        # If multiple records, and all are not company 3
        if len(self) > 1 and all(move.company_id.id != 3 for move in self):
            return self.env.ref('ul_reports.action_report_ul_invoice').report_action(self)

        return super().action_invoice_download_pdf(target=target)
