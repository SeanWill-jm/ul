import re

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


PREFIX_RE = re.compile(r"^\d{3}$")


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_account_prefix = fields.Char(
        string="Account Prefix",
        size=3,
        copy=False,
        index="btree_not_null",
        help=(
            "Three-digit branch prefix used when generating Customer Account No. "
            "Example: 103 produces account numbers such as 103-062001."
        ),
    )

    _partner_account_prefix_unique = models.Constraint(
        "unique(partner_account_prefix)",
        "The Account Prefix must be unique across all companies and branches.",
    )

    _partner_account_prefix_format = models.Constraint(
        "CHECK(partner_account_prefix IS NULL "
        "OR partner_account_prefix ~ '^[0-9]{3}$')",
        "The Account Prefix must contain exactly three digits.",
    )

    @api.onchange("partner_account_prefix")
    def _onchange_partner_account_prefix(self):
        for company in self:
            if company.partner_account_prefix:
                company.partner_account_prefix = company.partner_account_prefix.strip()

    @api.constrains("partner_account_prefix")
    def _check_partner_account_prefix(self):
        for company in self:
            prefix = (company.partner_account_prefix or "").strip()
            if not prefix:
                continue

            if not PREFIX_RE.fullmatch(prefix):
                raise ValidationError(
                    _("Account Prefix must contain exactly three digits, for example 103.")
                )

            duplicate = self.with_context(active_test=False).search(
                [
                    ("partner_account_prefix", "=", prefix),
                    ("id", "!=", company.id),
                ],
                limit=1,
            )
            if duplicate:
                raise ValidationError(
                    _(
                        "Account Prefix %(prefix)s is already assigned to %(company)s."
                    )
                    % {
                        "prefix": prefix,
                        "company": duplicate.display_name,
                    }
                )

    @api.model_create_multi
    def create(self, vals_list):
        normalized = []
        for vals in vals_list:
            vals = dict(vals)
            if "partner_account_prefix" in vals and vals["partner_account_prefix"]:
                vals["partner_account_prefix"] = vals["partner_account_prefix"].strip()
            normalized.append(vals)
        return super().create(normalized)

    def write(self, vals):
        vals = dict(vals)
        if "partner_account_prefix" in vals and vals["partner_account_prefix"]:
            vals["partner_account_prefix"] = vals["partner_account_prefix"].strip()
        return super().write(vals)
