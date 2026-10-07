# Functional Specification — Product Branch Assortment

Client: Unique Living (Odoo.sh, Odoo 19.0, parent company with branches)
Module: `product_branch_assortment` 19.0.1.0.0
Author: SWIT Global Consultants
Date: 2026-09-16
Status: specification approved in principle (defaults accepted 2026-09-16); build delivered for staging validation

## 1. Executive summary

Purchasing for every branch happens at the parent company, so every product
must be usable there. At the same time each branch must sell and stock only
the products assigned to it. Standard Odoo 19 has a single `Company` field on
the product and it gives one or the other, never both.

The module keeps the standard field set to the parent (or blank) — which is
what makes central purchasing work — and adds an independent **Allowed
Branches** list on the product. Empty means all branches. A listed branch (and
its sub-branches) may sell and stock the product; other branches are refused
when they try to sell it, receive it, adjust it upwards or set a reordering
rule for it. Nothing is hidden from anyone; reports, valuation and transfers
keep working. A branch removed from a product keeps the right to sell down
what it already holds. POS uses the standard per-register category
restriction; no POS code.

## 2. Facts versus inference

Documented facts (Odoo 19.0 documentation and source, verified 2026-09-16):

- Products are shared by default; setting `Company` restricts the record
  (Multi-company documentation).
- Product visibility rule: `['|', ('company_id', 'parent_of', company_ids), ('company_id', '=', False)]`
  (`addons/product/security/product_security.xml`). A product whose company is
  the parent is therefore visible and usable from every branch.
- Company consistency on documents uses `check_company_domain_parent_of`
  (`product.template._check_company_domain`); a product assigned to branch A
  is refused on a parent-company document.
- `product.template.company_id` is a `Many2one`; there is no standard
  multi-branch assignment.
- POS registers can restrict categories (`pos.config.limit_categories`,
  `iface_available_categ_ids`).
- `sale.order.line.product_template_id` reuses the `product_id` field domain
  (`_description_domain`) in 19.0.
- `stock.warehouse.orderpoint._get_orderpoint_products()` feeds the
  Replenishment report.

Inference / design (SWIT synthesis, not documented Odoo behaviour): everything
in sections 3–6.

## 3. Decisions taken (defaults accepted by Thomas 2026-09-16)

| Topic | Decision |
|---|---|
| Meaning of "assigned to a branch" | Sell/stock only. Products are never hidden. |
| Stranded stock | Sell-down allowed: existing on-hand can be sold/delivered; new receipts, positive adjustments and reordering rules refused. |
| POS | Native Restrict Categories per register; assortments must map to POS categories. |
| Maintenance | Per product, importable by CSV / list multi-edit. No category-level default in this version. |
| Packaging | Separate module `product_branch_assortment`, depends on `sale_stock`. |

## 4. Data model

`product.template.allowed_branch_ids` — Many2many `res.company`, relation
`product_template_allowed_branch_rel`, domain: companies with a parent.
Exposed on `product.product` through `_inherits`.

Constraint `_check_allowed_branch_ids`: listed companies must be branches; if
the product has a `Company`, the branches must be under it.

Allowed-for test (`_is_allowed_for_company(company)`): true when the list is
empty, when a listed branch is the company or one of its ancestors, or when
the company is an ancestor of a listed branch (so the parent is always
allowed). Search form of the same rule (`_branch_assortment_domain`):
`['|', ('allowed_branch_ids', '=', False), '|', ('allowed_branch_ids', 'parent_of', C), ('allowed_branch_ids', 'child_of', C)]`.

## 5. Enforcement points

| Model | Trigger | Rule | Exemptions |
|---|---|---|---|
| `sale.order.line` | `product_id`, `company_id` | product allowed for order company | sell-down: company holds on-hand stock (`stock.quant`, internal locations, read under minimal `sudo()`) |
| `stock.move` | product, source, destination, company, return link | destination internal location's company must be allowed | outgoing moves; internal relocation within the same branch; customer returns |
| `stock.warehouse.orderpoint` | product, warehouse, company | warehouse company must be allowed | — |
| Replenishment report | `_get_orderpoint_products` | non-allowed products dropped for the current branch | parent company unfiltered |
| Purchase | — | not enforced by design | — |

UI convenience only: `sale.order.line._domain_product_id` adds the assortment
domain evaluated against the line's `company_id`, so both product pickers on
the order line propose only assortment products.

## 6. Views

Inherited views, anchors verified against 19.0 `product/views/product_views.xml`
and `product_template_views.xml`:

- `product.product_template_form_view` — `//page[@name='general_information']//group[@name='group_general']`, inside (applies to the variant form, which inherits it in primary mode).
- `product.product_template_tree_view` — `//list`, inside, optional hidden column.
- `product.product_template_search_view` — `//search`, inside: search field and two filters.

No new models, so no ACL or record rules. Field visibility limited to
`base.group_multi_company`.

## 7. Acceptance criteria (UAT on staging)

1. Parent-company user raises a PO with a product allowed only for branch A: accepted.
2. Branch B user adds that product to a quotation: refused with a message naming the product, the branch and the allowed branches.
3. Branch A user and Sub-branch A1 user add it to a quotation: accepted.
4. Branch B receipt (supplier → B stock) of that product: refused. Same receipt at A and at the parent: accepted.
5. Inter-branch transfer parent → B of that product: refused; parent → A: accepted.
6. Branch B has 5 units on hand from before the restriction: quotation, delivery, internal relocation and customer return at B all accepted; receipt and positive adjustment refused.
7. Reordering rule for that product on B's warehouse: refused; on A's: accepted. Replenishment report at B does not propose it; at the parent it does.
8. Product with empty Allowed Branches: behaves exactly as before installation everywhere.
9. Listing the parent company, or a branch of another company tree, as an allowed branch: refused.
10. CSV import of Allowed Branches on 100 products (update mode) works with branch names and with external IDs.
11. Users tested: single-branch user, multi-branch user, parent-only user, administrator (master prompt §15).
12. Automated tests 14/14 pass on staging.

## 8. Risks and open points

- The sell-down check reads quants under `sudo()` (read-only aggregate, one company, one product); documented in code.
- A branch-level purchase order is not filtered; the goods are refused at receipt. If branches must not even order, a purchase-line constraint is a small addition.
- Category-level defaults are out of scope for 1.0.0.
- Runtime validation (installation, XPath resolution against the staging database's resolved views, tests) has not yet been performed in this build environment.

## 9. Rollback

Uninstalling removes the field, the relation table and the views. No standard
data is modified by the module; orders, moves and rules created while it was
installed remain valid.
