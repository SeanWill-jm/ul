# Patch notes — 19.0.1.0.2

**Type:** install/upgrade fix (view validation). No functional change.
**Runtime validation status:** Python syntax, XML well-formedness, ZIP integrity validated.
Upgrade and the 14 tests on Staging are **not yet validated** for this version.

## Runtime result that triggered this version (Staging, 2026-09-30, 1.0.1 upgrade)

`ParseError ... Invalid view purchase.order.search.po.delivery.address definition`, with
`RELAXNG_ERR_INVALIDATTR: Invalid attribute string for element group` (and the follow-on
`Element search has extra content: field`). The form view and the two list views of 1.0.1 loaded
before it without error; the whole upgrade rolled back (database still on 1.0.0).

## Root cause

Odoo 19.0's search view schema does not accept a `string` attribute on a `<group>` inside
`<search>`. The standard `purchase.view_purchase_order_filter` (19.0 source) uses a bare
`<group>` for its Group By filters. 1.0.1 used `<group string="Delivery Address">`, a pre-19
habit.

## Change

- `views/purchase_order_views.xml`: `<group string="Delivery Address">` -> `<group>`.
- Manifest version 19.0.1.0.2.

## Same-class check

- Other inherited views (form, RFQ list, PO list) use only attributes already seen in 19.0 source
  (`optional`, `options`, `context`, `placeholder`) and passed validation on Staging.
- Portal and report templates are QWeb (not RNG-validated) and have not loaded yet because the
  upgrade stopped earlier; they are the next runtime checkpoint.

## What did not change

Model, tag, constraint, reports, portal block, tests, upgrade procedure.
