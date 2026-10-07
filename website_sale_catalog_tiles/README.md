# eCommerce Catalog Tiles — Odoo.sh 19.0

Version: 19.0.1.0.1 · Last Updated: 2026-10-07 · Copyright © 2026 SWIT Global Consultants · Created by: SWIT Global Consultants

> In Odoo: Apps › this module's card › **Module Info** shows the same guide (`static/description/index.html`).

Gives the shop grid (`/shop`, category pages, dynamic product snippets, wishlist)
the look of the Sales app's **Catalog** view that the client liked: on every
product tile,

- the **internal reference / SKU** under the product name,
- the **on-hand quantity** in the website's warehouse ("7 On Hand" in green,
  "0 On Hand" in red, "· order anyway" when selling out of stock is allowed),
- a **quantity picker** ( − [ 1 ] + ) next to **Add to Cart**; the chosen
  quantity goes straight into the cart in one click, no pop-up.

Each element is a per-website switch (Website › Configuration › Settings ›
eCommerce › **Catalog Tiles**), so the retail site and the wholesale site can be
set differently. The on-hand quantity can be limited to logged-in customers,
which is the right setting for an invitation-only wholesale site.

## How it works (no custom JavaScript)

Standard `website_sale` (19.0) already reads an `add_qty` input inside the tile
form when the tile's Add to Cart button is clicked (`_updateRootProduct`), and
its `onChangeQuantity` handler drives any `−`/`+` anchor with class
`js_add_cart_json` inside an `.input-group`. This module only adds that markup
to the tile (`website_sale.shop_product_buttons`) and turns off the standard
quantity pop-up for the tile button, so the quantity typed on the tile is what
is added. Stock is read the same way the standard product page does
(`website._get_product_available_qty`, `website_sale_stock`), under a
read-only `sudo()` because visitors cannot read stock quants.

When "Sell when Out-of-Stock" is off on a product, the picker's maximum is the
available quantity; the standard cart checks still apply at checkout.

## Settings

| Setting | Default | Effect |
|---|---|---|
| Show Internal Reference on Tiles | on | SKU under the name |
| Quantity Picker on Tiles | on | − [qty] + next to Add to Cart |
| Show On-Hand Quantity on Tiles | Logged-in customers only | Never / Logged-in only / Everyone |

Suggested: retail site → reference on, picker on, on-hand "Everyone" (or
"Never" if the client prefers not to expose stock); wholesale site → all on,
on-hand "Logged-in customers only".

## Views inherited (anchors verified against 19.0 source)

- `website_sale.products_item` — `//h2[hasclass('o_wsale_products_item_title')]`, after.
- `website_sale.shop_product_buttons` — `//button[hasclass('o_wsale_product_btn_primary')]`, before + attributes; `//div[hasclass('o_wsale_product_action_row')]`, attributes. Both `attributes` edits only add a `t-attf-class`; the standard `class` is kept so other modules' `hasclass()` anchors still resolve.
- `website_sale.res_config_settings_view_form` — `setting[@id='cart_redirect_setting']`, after.

Tiles keep working with the website editor's own tile options (image ratio,
columns, description, etc.); this module adds elements, it does not replace
the tile.

## Tests

`tests/test_catalog_tiles.py` — 5 tests (HttpCase): on-hand info reads the
website warehouse; visibility policy per user type; `/shop` renders reference,
stock and picker; settings switch the elements off; standard classes are preserved (test 05).

```bash
odoo-bin -d $PGDATABASE -i website_sale_catalog_tiles --stop-after-init
odoo-bin -d $PGDATABASE -u website_sale_catalog_tiles --test-enable --test-tags /website_sale_catalog_tiles --stop-after-init
```

## Known limits

- Stock is computed per tile (one `free_qty` read per product on the page);
  fine for 20–40 tiles per page, revisit if the client raises products per
  page to the maximum.
- Configurable products (attributes) still open the standard configurator on
  Add to Cart; the tile quantity is passed to it.
- The picker is not shown on the product page itself (standard page already
  has one).

## Release notes

- **19.0.1.0.0** (2026-09-23) — initial implementation. Static checks only;
  runtime installation and tests not yet run.

---
License: LGPL-3 · Summary: shop tiles with SKU, on-hand quantity and a quantity picker next to Add to Cart · Platform Version: Odoo 19.0 (Odoo.sh) · Status: Static checks only; staging install pending
Copyright © 2026 SWIT Global Consultants — https://switconsulting.com · Created by: SWIT Global Consultants
