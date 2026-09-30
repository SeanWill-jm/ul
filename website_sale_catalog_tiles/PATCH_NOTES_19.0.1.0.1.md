# Patch notes — 19.0.1.0.1

**Type:** install fix (view inheritance). No functional change intended.
**Runtime validation status:** Python syntax, XML well-formedness, ZIP integrity validated.
Install and the 5 tests on Staging are **not yet validated** for this version. (1.0.0 never installed.)

## Runtime result that triggered this version (Staging, 2026-09-30, Apps -> Install 1.0.0)

`ParseError: Element '<xpath expr="//div[hasclass('o_wsale_product_action_row')]">' cannot be
located in parent view`, error context view `Comparison List Button` (ir.ui.view 2750), parent
view 2546 (`website_sale.shop_product_buttons`), xmlid shown = `shop_product_buttons_catalog`
(the record being loaded).

## Root cause

The failing xpath is not ours: it belongs to `website_sale_comparison.add_to_compare`
(inherits `website_sale.shop_product_buttons`, priority 32, xpath
`//div[hasclass('o_wsale_product_action_row')]`, read from the 19.0 source). Our template
(priority 16, applied first) replaced the `class` attribute of that `div` (and of the Add to Cart
button) by a `t-attf-class` and emptied `class` (`<attribute name="class"/>` removes it). After
our edit the node had no `class`, so the comparison view's `hasclass()` anchor could not find it,
and Odoo's whole-tree validation rejected the install. Upstream anchors were fine; the damage
was caused by our attribute edit. Evidence level: error text + 19.0 source of both templates;
not yet confirmed by a successful install.

## Change

- `views/product_tile_templates.xml`: stop removing `class`. Both `attributes` edits now only set
  a dynamic `t-attf-class` (`{{ picker and 'o_wsct_... ' or '' }}`); QWeb merges it with the
  standard static class. The Add button still gets `t-att-data-show-quantity` overridden.
- `tests/test_catalog_tiles.py`: new test 05 (standard and added classes are both rendered).
- Manifest 19.0.1.0.1; README anchor note.

## Same-class check

- `products_item` xpath only inserts after the title: no attribute removal.
- Settings view: `setting[@id='cart_redirect_setting']` exists in the 19.0 `website_sale`
  settings form (source-read); insert-after only.
- Rule added: never drop/replace `class` on nodes that other modules may anchor with `hasclass()`;
  add classes instead.

## What did not change

Models, settings fields, SCSS, tile reference/on-hand block, runbook.
The 1.0.0 PDF copies of README/RUNBOOK were not regenerated.
