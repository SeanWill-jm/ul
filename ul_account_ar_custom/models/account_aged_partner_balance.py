# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.tools import SQL


class AccountAgedReceivableReportHandler(models.AbstractModel):
    _inherit = 'account.aged.receivable.report.handler'

    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(report, options, previous_options=previous_options)

        # Point the report to our custom JS filter component
        options['custom_display_config']['components'] = {
            'AccountReportFilters': 'UlArFilters',
        }

        # --- Sales Rep filter ---
        prev_sales_reps = previous_options.get('ar_sales_rep_ids', [])
        selected_sales_reps = self.env['res.users'].browse(
            [int(i) for i in prev_sales_reps]
        ).exists()
        options['ar_sales_rep_ids'] = selected_sales_reps.ids
        options['ar_selected_sales_rep_names'] = selected_sales_reps.mapped('name')

        # --- Branch filter (company_id) ---
        prev_branches = previous_options.get('ar_branch_ids', [])
        selected_branches = self.env['res.company'].browse(
            [int(i) for i in prev_branches]
        ).exists()
        options['ar_branch_ids'] = selected_branches.ids
        options['ar_selected_branch_names'] = selected_branches.mapped('name')

    def _aged_partner_report_custom_engine_common(self, options, internal_type, current_groupby, next_groupby, offset=0, limit=None):
        # Inject extra WHERE conditions via forced_domain before calling super
        extra_domain = []

        if options.get('ar_sales_rep_ids'):
            extra_domain.append(('move_id.invoice_user_id', 'in', options['ar_sales_rep_ids']))

        if options.get('ar_branch_ids'):
            extra_domain.append(('company_id', 'in', options['ar_branch_ids']))

        if extra_domain:
            # Temporarily extend forced_domain so the base query picks it up
            original_forced_domain = options.get('forced_domain', [])
            options = {**options, 'forced_domain': original_forced_domain + extra_domain}

        return super()._aged_partner_report_custom_engine_common(
            options, internal_type, current_groupby, next_groupby,
            offset=offset, limit=limit,
        )
