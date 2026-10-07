import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


ACCOUNT_RE = re.compile(r"^(?P<prefix>\d{3})-(?P<suffix>\d{6})$")

# Legacy (ManageMore) forms accepted on import/manual entry and normalized to
# PPP-NNNNNN:
#   "30007", "-36798"          -> no prefix (1-6 digits, optional leading dash)
#   "103-30007", "103 - 1234"  -> prefix + dash + 1-6 digit suffix
#   "10240048", "101000001"    -> dash dropped by the export: 7-9 digits =
#                                 3-digit prefix + 4-6 digit suffix
# Runs of more than nine digits, and "0103-30007" (prefix must be exactly three
# digits), are rejected.
LEGACY_RE = re.compile(
    r"^(?:(?P<prefix>\d{3})\s*-|-)?\s*(?P<suffix>\d{1,6})$"
)
LEGACY_CONCAT_RE = re.compile(r"^(?P<prefix>\d{3})(?P<suffix>\d{4,6})$")


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _default_customer_type(self):
        # Do not automatically classify child invoice/delivery/contact addresses.
        if self.env.context.get("default_parent_id") or self.env.context.get("default_type") in {
            "invoice",
            "delivery",
            "other",
        }:
            return False

        search_mode = self.env.context.get("res_partner_search_mode")
        if search_mode == "customer":
            return "customer"
        if search_mode == "supplier":
            return "vendor"
        return False

    customer_type = fields.Selection(
        selection=[
            ("customer", "Customer"),
            ("vendor", "Vendor"),
            ("both", "Customer & Vendor"),
        ],
        string="Customer Type",
        default=_default_customer_type,
        copy=False,
        index=True,
        help=(
            "Migration/business classification for this contact. "
            "This supplements Odoo's native customer/vendor behavior."
        ),
    )

    customer_account_no = fields.Char(
        string="Customer Account No.",
        copy=False,
        index="btree_not_null",
        help=(
            "Branch-prefixed globally unique account number in PPP-NNNNNN format, "
            "for example 103-062001."
        ),
    )

    account_branch_id = fields.Many2one(
        comodel_name="res.company",
        string="Account Branch",
        copy=False,
        index=True,
        ondelete="restrict",
        domain=[("partner_account_prefix", "!=", False)],
        help=(
            "Branch whose three-digit Account Prefix forms the first part of "
            "Customer Account No. Existing assigned account numbers are immutable."
        ),
    )

    legacy_account_no = fields.Char(
        string="Legacy Account No.",
        copy=False,
        index="btree_not_null",
        help=(
            "Original account number exactly as it existed in the legacy system "
            "(for example ManageMore) before it was normalized to PPP-NNNNNN. "
            "Populated automatically when an imported or typed value needed "
            "normalization. Kept for audit and reconciliation."
        ),
    )

    customer_account_suffix = fields.Char(
        string="Account Sequence",
        size=6,
        copy=False,
        readonly=True,
        index="btree_not_null",
        help="Technical six-digit globally unique portion of Customer Account No.",
    )

    _customer_account_no_unique = models.Constraint(
        "unique(customer_account_no)",
        "Customer Account No. must be unique.",
    )

    _customer_account_suffix_unique = models.Constraint(
        "unique(customer_account_suffix)",
        "The six-digit account sequence has already been used.",
    )

    _customer_account_no_format = models.Constraint(
        "CHECK(customer_account_no IS NULL "
        "OR customer_account_no ~ '^[0-9]{3}-[0-9]{6}$')",
        "Customer Account No. must use the format 103-062001.",
    )

    _customer_account_suffix_format = models.Constraint(
        "CHECK(customer_account_suffix IS NULL "
        "OR customer_account_suffix ~ '^[0-9]{6}$')",
        "Account Sequence must contain exactly six digits.",
    )

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @api.model
    def _parse_account_number(self, account_no):
        account_no = (account_no or "").strip()
        match = ACCOUNT_RE.fullmatch(account_no)
        if not match:
            raise ValidationError(
                _(
                    "Customer Account No. '%(account)s' is invalid. "
                    "Expected format: 103-062001."
                )
                % {"account": account_no or _("(blank)")}
            )
        return account_no, match.group("prefix"), match.group("suffix")

    @api.model
    def _normalize_account_number(self, raw_value):
        """Return (account_no, prefix, suffix, legacy_raw, branch, prefix_from_value).

        Precedence rules (decided 2026-09-01):

        1. The value carries a three-digit prefix that belongs to an assigned
           branch (``101-36798`` -> ``101-036798``): that prefix and branch are
           used, whatever company the import runs in.
        2. Otherwise (no prefix: ``30007``, ``-36798``; or a prefix no branch
           owns: ``100-36798``): the **current company** (``self.env.company``,
           i.e. the company selected while importing) supplies the prefix and
           becomes the Account Branch.

        The numeric part is zero-padded to six digits. ``legacy_raw`` holds the
        original value whenever normalization changed it, otherwise ``False``.
        ``prefix_from_value`` is True only in rule 1.
        """
        raw_value = (raw_value or "").strip()
        match = (
            ACCOUNT_RE.fullmatch(raw_value)
            or LEGACY_RE.fullmatch(raw_value)
            or LEGACY_CONCAT_RE.fullmatch(raw_value)
        )
        if not match:
            raise ValidationError(
                _(
                    "Customer Account No. '%(account)s' is invalid. "
                    "Expected PPP-NNNNNN (for example 103-062001) or a legacy "
                    "number: up to six digits with an optional three-digit "
                    "prefix (30007, -36798, 103-30007) or the prefix and number "
                    "run together (10330007)."
                )
                % {"account": raw_value or _("(blank)")}
            )

        value_prefix = match.group("prefix")
        suffix = match.group("suffix").zfill(6)

        branch = self._branch_for_prefix(value_prefix, raise_if_missing=False) if value_prefix else None
        prefix_from_value = bool(branch)
        if not branch:
            branch = self.env.company
        prefix = self._validate_branch_prefix(branch)

        account_no = f"{prefix}-{suffix}"
        legacy_raw = raw_value if raw_value != account_no else False
        return account_no, prefix, suffix, legacy_raw, branch, prefix_from_value

    @api.model
    def _branch_for_prefix(self, prefix, raise_if_missing=True):
        # Global lookup: prefixes are unique across ALL companies, so the search
        # must not be narrowed by the user's currently enabled companies.
        branches = self.env["res.company"].sudo().with_context(active_test=False).search(
            [("partner_account_prefix", "=", prefix)],
            limit=2,
        )
        if not branches:
            if not raise_if_missing:
                return self.env["res.company"]
            raise ValidationError(
                _(
                    "No Odoo company/branch is configured with Account Prefix %(prefix)s."
                )
                % {"prefix": prefix}
            )
        if len(branches) > 1:
            raise ValidationError(
                _(
                    "More than one company/branch uses Account Prefix %(prefix)s. "
                    "Correct the branch configuration before continuing."
                )
                % {"prefix": prefix}
            )
        return branches

    @api.model
    def _validate_branch_prefix(self, branch, expected_prefix=None):
        if not branch:
            raise ValidationError(
                _(
                    "An Account Branch is required before a Customer Account No. "
                    "can be generated."
                )
            )

        prefix = (branch.partner_account_prefix or "").strip()
        if not prefix:
            raise ValidationError(
                _(
                    "Branch %(branch)s does not have an Account Prefix configured."
                )
                % {"branch": branch.display_name}
            )

        if not re.fullmatch(r"\d{3}", prefix):
            raise ValidationError(
                _(
                    "Branch %(branch)s has invalid Account Prefix '%(prefix)s'. "
                    "The prefix must contain exactly three digits."
                )
                % {
                    "branch": branch.display_name,
                    "prefix": prefix,
                }
            )

        if expected_prefix and prefix != expected_prefix:
            raise ValidationError(
                _(
                    "Customer Account No. prefix %(number_prefix)s does not match "
                    "the selected Account Branch prefix %(branch_prefix)s."
                )
                % {
                    "number_prefix": expected_prefix,
                    "branch_prefix": prefix,
                }
            )
        return prefix

    @api.model
    def _assert_account_available(self, account_no, suffix, exclude_id=False):
        domain = [
            "|",
            ("customer_account_no", "=", account_no),
            ("customer_account_suffix", "=", suffix),
        ]
        if exclude_id:
            domain = ["&", ("id", "!=", exclude_id)] + domain

        # Global invariant: the suffix is unique across all branches, so check
        # across every company regardless of the user's enabled companies and
        # record rules. Only display_name / account number are read from the
        # match, for the error message.
        duplicate = self.sudo().with_context(active_test=False).search(domain, limit=1)
        if duplicate:
            if duplicate.customer_account_suffix == suffix:
                raise ValidationError(
                    _(
                        "Account sequence %(suffix)s is already used by %(partner)s "
                        "(%(account)s). The six-digit suffix is globally unique "
                        "across all branches."
                    )
                    % {
                        "suffix": suffix,
                        "partner": duplicate.display_name,
                        "account": duplicate.customer_account_no,
                    }
                )
            raise ValidationError(
                _(
                    "Customer Account No. %(account)s is already assigned to %(partner)s."
                )
                % {
                    "account": account_no,
                    "partner": duplicate.display_name,
                }
            )

    @api.model
    def _prepare_supplied_account(self, account_no, branch_id=False, exclude_id=False):
        (
            account_no,
            prefix,
            suffix,
            legacy_raw,
            branch,
            prefix_from_value,
        ) = self._normalize_account_number(account_no)

        if branch_id and prefix_from_value:
            # Explicit prefix in the value and an explicit Account Branch: they
            # must agree. (For prefix-less/unknown-prefix values the current
            # company wins and any supplied Account Branch is ignored.)
            supplied_branch = self.env["res.company"].browse(branch_id).exists()
            if not supplied_branch:
                raise ValidationError(_("The selected Account Branch does not exist."))
            self._validate_branch_prefix(supplied_branch, expected_prefix=prefix)

        self._assert_account_available(account_no, suffix, exclude_id=exclude_id)
        values = {
            "customer_account_no": account_no,
            "customer_account_suffix": suffix,
            "account_branch_id": branch.id,
        }
        if legacy_raw:
            values["legacy_account_no"] = legacy_raw
        return values

    @api.model
    def _next_account_values(self, branch):
        prefix = self._validate_branch_prefix(branch)
        sequence = self.env["ir.sequence"].sudo()

        # Skip imported/reserved numbers if they overlap the automatic range.
        for _attempt in range(100000):
            suffix = sequence.next_by_code("partner.account.number")
            if not suffix:
                raise ValidationError(
                    _(
                        "The Partner Account Number sequence is missing or inactive. "
                        "Install or repair the module sequence before creating accounts."
                    )
                )

            suffix = suffix.strip()
            if not re.fullmatch(r"\d{6}", suffix):
                raise ValidationError(
                    _(
                        "The Partner Account Number sequence returned '%(suffix)s'. "
                        "It must return exactly six digits."
                    )
                    % {"suffix": suffix}
                )

            account_no = f"{prefix}-{suffix}"
            duplicate = self.sudo().with_context(active_test=False).search(
                [
                    "|",
                    ("customer_account_no", "=", account_no),
                    ("customer_account_suffix", "=", suffix),
                ],
                limit=1,
            )
            if not duplicate:
                return {
                    "customer_account_no": account_no,
                    "customer_account_suffix": suffix,
                    "account_branch_id": branch.id,
                }

        raise ValidationError(
            _(
                "Odoo checked 100,000 sequence values but could not find an unused "
                "Customer Account No. Review imported numbers and sequence configuration."
            )
        )

    # -------------------------------------------------------------------------
    # UI validation
    # -------------------------------------------------------------------------

    @api.onchange("customer_type")
    def _onchange_customer_type(self):
        for partner in self:
            if partner.customer_type and not partner.account_branch_id:
                partner.account_branch_id = self.env.company

    @api.onchange("customer_account_no")
    def _onchange_customer_account_no(self):
        for partner in self:
            if not partner.customer_account_no:
                continue

            (
                account_no,
                prefix,
                suffix,
                legacy_raw,
                branch,
                prefix_from_value,
            ) = self._normalize_account_number(partner.customer_account_no)
            partner.customer_account_no = account_no
            if legacy_raw and not partner.legacy_account_no:
                partner.legacy_account_no = legacy_raw

            if partner.account_branch_id and prefix_from_value:
                self._validate_branch_prefix(
                    partner.account_branch_id,
                    expected_prefix=prefix,
                )
            else:
                partner.account_branch_id = branch

            # Do not populate the technical suffix until save; the user may still
            # correct an unsaved account number in the form.
            self._assert_account_available(
                account_no,
                suffix,
                exclude_id=partner.id if isinstance(partner.id, int) else False,
            )

    # -------------------------------------------------------------------------
    # ORM integrity
    # -------------------------------------------------------------------------

    @api.constrains(
        "customer_type",
        "customer_account_no",
        "customer_account_suffix",
        "account_branch_id",
    )
    def _check_customer_account_integrity(self):
        for partner in self:
            if not partner.customer_account_no:
                if partner.customer_type:
                    raise ValidationError(
                        _(
                            "A contact classified as Customer, Vendor, or Customer & Vendor "
                            "must have a Customer Account No."
                        )
                    )
                continue

            if not partner.customer_type:
                raise ValidationError(
                    _("Customer Type is required when a Customer Account No. is assigned.")
                )

            account_no, prefix, suffix = self._parse_account_number(
                partner.customer_account_no
            )
            if partner.customer_account_suffix != suffix:
                raise ValidationError(
                    _(
                        "Stored Account Sequence does not match Customer Account No. "
                        "Use the supported create/import process to correct the record."
                    )
                )

            self._validate_branch_prefix(
                partner.account_branch_id,
                expected_prefix=prefix,
            )
            self._assert_account_available(
                account_no,
                suffix,
                exclude_id=partner.id,
            )

    @api.model_create_multi
    def create(self, vals_list):
        prepared_vals_list = []
        batch_numbers = set()
        batch_suffixes = set()
        default_type = self._default_customer_type()

        for incoming in vals_list:
            vals = dict(incoming)

            if "customer_account_no" in vals:
                vals["customer_account_no"] = (
                    (vals["customer_account_no"] or "").strip() or False
                )

            if not vals.get("customer_type") and default_type:
                vals["customer_type"] = default_type

            customer_type = vals.get("customer_type")
            supplied_account = vals.get("customer_account_no")

            if supplied_account and not customer_type:
                raise ValidationError(
                    _("Customer Type is required when importing/entering Customer Account No.")
                )

            if customer_type:
                if supplied_account:
                    account_vals = self._prepare_supplied_account(
                        supplied_account,
                        branch_id=vals.get("account_branch_id"),
                    )
                    if vals.get("legacy_account_no"):
                        # An explicit legacy value in the import wins.
                        account_vals.pop("legacy_account_no", None)
                else:
                    branch = (
                        self.env["res.company"].browse(vals["account_branch_id"]).exists()
                        if vals.get("account_branch_id")
                        else self.env.company
                    )
                    account_vals = self._next_account_values(branch)

                if account_vals["customer_account_no"] in batch_numbers:
                    raise ValidationError(
                        _(
                            "Customer Account No. %(account)s occurs more than once "
                            "in the same import/create batch."
                        )
                        % {"account": account_vals["customer_account_no"]}
                    )
                if account_vals["customer_account_suffix"] in batch_suffixes:
                    raise ValidationError(
                        _(
                            "Account sequence %(suffix)s occurs more than once "
                            "in the same import/create batch."
                        )
                        % {"suffix": account_vals["customer_account_suffix"]}
                    )

                batch_numbers.add(account_vals["customer_account_no"])
                batch_suffixes.add(account_vals["customer_account_suffix"])
                vals.update(account_vals)
            else:
                vals.pop("customer_account_suffix", None)

            prepared_vals_list.append(vals)

        return super().create(prepared_vals_list)

    def write(self, vals):
        # Write per record because bulk classification may require a different
        # sequence-generated account number for each partner.
        for partner in self:
            record_vals = dict(vals)

            supplied = (
                record_vals.get("customer_account_no")
                if "customer_account_no" in record_vals
                else None
            )
            if "customer_account_no" in record_vals:
                supplied = (supplied or "").strip() or False
                record_vals["customer_account_no"] = supplied

            # Issued number and originating branch are immutable.
            if partner.customer_account_no:
                if "customer_account_no" in record_vals:
                    normalized = False
                    if supplied:
                        try:
                            normalized = self._normalize_account_number(supplied)[0]
                        except ValidationError:
                            normalized = False
                    if not supplied or normalized != partner.customer_account_no:
                        raise UserError(
                            _(
                                "Customer Account No. %(account)s has already been issued "
                                "and cannot be changed or cleared. Archive the contact instead "
                                "of reusing its number."
                            )
                            % {"account": partner.customer_account_no}
                        )
                    record_vals.pop("customer_account_no", None)

                if "account_branch_id" in record_vals:
                    new_branch_id = record_vals.get("account_branch_id") or False
                    if new_branch_id != partner.account_branch_id.id:
                        raise UserError(
                            _(
                                "Account Branch cannot be changed after Customer Account No. "
                                "%(account)s has been issued."
                            )
                            % {"account": partner.customer_account_no}
                        )
                    record_vals.pop("account_branch_id", None)

                if "customer_type" in record_vals and not record_vals.get("customer_type"):
                    raise UserError(
                        _(
                            "Customer Type cannot be cleared while Customer Account No. "
                            "%(account)s is assigned."
                        )
                        % {"account": partner.customer_account_no}
                    )

                record_vals.pop("customer_account_suffix", None)
            else:
                resulting_type = record_vals.get("customer_type", partner.customer_type)

                if supplied and not resulting_type:
                    raise ValidationError(
                        _(
                            "Customer Type is required when importing/entering "
                            "Customer Account No."
                        )
                    )

                if resulting_type:
                    if supplied:
                        account_vals = self._prepare_supplied_account(
                            supplied,
                            branch_id=record_vals.get(
                                "account_branch_id",
                                partner.account_branch_id.id,
                            ),
                            exclude_id=partner.id,
                        )
                        if record_vals.get("legacy_account_no"):
                            account_vals.pop("legacy_account_no", None)
                    else:
                        branch_id = record_vals.get(
                            "account_branch_id",
                            partner.account_branch_id.id,
                        )
                        branch = (
                            self.env["res.company"].browse(branch_id).exists()
                            if branch_id
                            else self.env.company
                        )
                        account_vals = self._next_account_values(branch)

                    record_vals.update(account_vals)
                else:
                    record_vals.pop("customer_account_suffix", None)

            super(ResPartner, partner).write(record_vals)

        return True

    @api.ondelete(at_uninstall=False)
    def _prevent_numbered_partner_deletion(self):
        numbered = self.filtered("customer_account_no")
        if numbered:
            examples = ", ".join(numbered.mapped("customer_account_no")[:5])
            raise UserError(
                _(
                    "Contacts with issued Customer Account No. cannot be deleted. "
                    "Archive them instead. Affected account(s): %(accounts)s"
                )
                % {"accounts": examples}
            )
