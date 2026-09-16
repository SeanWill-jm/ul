from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allowed_branch_ids = fields.Many2many(
        comodel_name="res.company",
        relation="product_template_allowed_branch_rel",
        column1="product_tmpl_id",
        column2="company_id",
        string="Allowed Branches",
        domain="[('parent_id', '!=', False)]",
        help=(
            "Branches allowed to sell and stock this product. Leave empty to allow "
            "every branch.\n"
            "The parent company is never restricted, so central purchasing always "
            "has the full catalogue. Listing a branch also allows its sub-branches.\n"
            "A branch removed from this list may still sell the stock it already "
            "holds; new receipts, positive inventory adjustments and reordering "
            "rules for that branch are refused."
        ),
    )

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------
    @api.constrains("allowed_branch_ids", "company_id")
    def _check_allowed_branch_ids(self):
        for template in self:
            for branch in template.allowed_branch_ids:
                if not branch.parent_id:
                    raise ValidationError(
                        _(
                            "%(branch)s is a parent company, not a branch. The parent "
                            "company is always allowed; only branches can be listed "
                            "in Allowed Branches of %(product)s.",
                            branch=branch.display_name,
                            product=template.display_name,
                        )
                    )
                if template.company_id and template.company_id not in branch.parent_ids:
                    raise ValidationError(
                        _(
                            "Branch %(branch)s does not belong to %(company)s, the "
                            "company set on product %(product)s.",
                            branch=branch.display_name,
                            company=template.company_id.display_name,
                            product=template.display_name,
                        )
                    )

    # ------------------------------------------------------------------
    # Assortment logic (single source of truth for every enforcement point)
    # ------------------------------------------------------------------
    def _is_allowed_for_company(self, company):
        """Return True when ``company`` may sell/stock this product.

        Rules:
        - no Allowed Branches -> allowed everywhere;
        - a listed branch, or any of its ancestors (parent company included)
          or descendants (sub-branches), is allowed;
        - any other branch is not.
        """
        self.ensure_one()
        allowed = self.allowed_branch_ids
        if not allowed or not company:
            return True
        # ``parent_ids`` is the record itself plus every ancestor up to the root.
        if allowed & company.parent_ids:
            return True
        return any(company in branch.parent_ids for branch in allowed)

    @api.model
    def _branch_assortment_domain(self, company):
        """Domain matching the products ``company`` may sell/stock.

        ``company`` may be a res.company record, an id, or an ``unquote`` name
        (for client-side field domains evaluated against the record).
        """
        if isinstance(company, models.BaseModel):
            company = company.id
        return [
            "|",
            ("allowed_branch_ids", "=", False),
            "|",
            ("allowed_branch_ids", "parent_of", company),
            ("allowed_branch_ids", "child_of", company),
        ]

    def _branch_assortment_error(self, company):
        self.ensure_one()
        return _(
            "%(product)s is not in the assortment of branch %(branch)s. "
            "Allowed branches: %(allowed)s. Ask an administrator to add the "
            "branch on the product form (Allowed Branches).",
            product=self.display_name,
            branch=company.display_name,
            allowed=", ".join(self.allowed_branch_ids.mapped("display_name")),
        )
