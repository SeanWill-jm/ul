# Patch notes — 19.0.1.0.1 (2026-09-23)

Requested by Thomas after the first staging build: branch users should not see
out-of-assortment products in their day-to-day product lists, without hiding
the records (the sell/stock-only premise is unchanged; no record rule added).

## Added

- `product.template.in_branch_assortment` — computed, non-stored, searchable
  Boolean: True when the company currently selected in the switcher may
  sell/stock the product (same rule as the constraints). Available on
  `product.product` through `_inherits`.
- Search filters "In my branch's assortment" / "Outside my branch's assortment"
  on the product search view (multi-company users).
- Two shared favourite filters (`ir.filters`, `data/ir_filters.xml`,
  `noupdate="1"`): "My branch's assortment", model `product.template` and
  `product.product`, default, no action and no user, so they are applied by
  default on every product list and kanban. Any user can remove the filter for
  the current view; administrators can edit or disable it under Settings ›
  Technical › User-defined Filters, and their edits survive module upgrades.
- `migration_templates/product_assortment_import_template.csv` (master prompt §31).
- Tests 15 and 16.

## Unchanged

Constraints, product-picker domain, Replenishment filter, sell-down rule,
views/anchors from 1.0.0.

## Notes

- The favourite is a list/kanban filter only; it does not affect the product
  picker on documents (already filtered by the 1.0.0 domain), reports, or
  many2one searches elsewhere.
- Static checks only; runtime installation (`-u product_branch_assortment`)
  and tests 1–16 still to be run on staging.
