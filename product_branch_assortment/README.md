# Product Branch Assortment — Odoo.sh 19.0

Installable Odoo 19.0 module for multi-branch databases where **purchasing is
central** (parent company) but **each branch sells and stocks only its own
assortment**.

Standard Odoo 19 offers one field for this, `Company` on the product, and it is
either/or: blank or parent = every branch may use the product; a branch = only
that branch may, and the parent can no longer put it on a purchase order. This
module adds a second, independent axis.

## Business rule

| Product setting | Parent company | Listed branch (and its sub-branches) | Other branch |
|---|---|---|---|
| `Company` = parent or blank, **Allowed Branches empty** | purchase, sell, stock | sell, stock | sell, stock |
| `Company` = parent or blank, **Allowed Branches = A** | purchase, sell, stock | sell, stock | **no new stock, no reorder rule, no sale** — except sell-down (below) |

- Products are **never hidden**. Every user still finds every product in
  Inventory, reports, valuation and transfers. The rule only refuses a
  transaction that would put a product outside its assortment.
- **Sell-down:** a branch removed from a product's Allowed Branches may still
  sell and deliver the stock it already holds. Receipts, inbound transfers,
  positive inventory adjustments and reordering rules for that branch are
  refused. Customer returns are always accepted.
- Purchasing is untouched by design. Keep `Company` = parent (or blank) on all
  products; that is what makes central purchasing possible in standard Odoo.

## What the module adds

### Field on Products (`product.template`, visible on variants too)

- **Allowed Branches** (`allowed_branch_ids`, Many2many to `res.company`,
  only companies that have a parent). Empty = all branches. Shown on the
  General Information tab (multi-company users only), as an optional column in
  the product list, and as search field plus "Branch-restricted" / "All
  branches" filters.
- Constraint: only branches can be listed (never a parent company), and when
  the product has a `Company`, only branches under that company.

### Enforcement (Python constraints, so imports and RPC are covered too)

| Where | Rule |
|---|---|
| Sales order line | Product must be allowed for the order's company, or the company must still hold on-hand stock of it (sell-down). |
| Stock move | Destination internal location of a non-allowed branch is refused, unless the move is a customer return or an internal relocation inside the same branch. Outgoing moves are never refused. |
| Reordering rule | Warehouse's company must be allowed. The Replenishment report also stops proposing non-allowed products for the current branch. |

### UI convenience

The product pickers on sales order lines only propose products in the
assortment of the order's company. This is a filter, not the safeguard: the
constraints above are.

### POS

Not customised. Use the standard **Restrict Categories** option on each POS
register (Point of Sale › Configuration › Point of Sale › *register* ›
Products › Available Categories) to limit what a register sells. Assortments
must therefore map to POS categories.

## Configuration

1. Install the module on a development/staging branch first.
2. On every product keep **Company** = parent company or blank.
3. Set **Allowed Branches** on the products that are branch-specific. Leave
   it empty on products every branch may sell.
4. Bulk maintenance: Inventory › Products › list view › select › multi-edit
   **Allowed Branches**, or import a CSV with columns
   `External ID`/`Internal Reference` and `Allowed Branches` (branch names
   separated by commas, or external IDs via `Allowed Branches/External ID`).
5. For POS registers, set Restrict Categories as needed.

## Removing a branch from a product

Nothing happens to existing stock or open orders. From that moment the branch
can sell its remaining quantity but cannot receive more, adjust upwards or keep
a reordering rule for it (existing reordering rules are refused the next time
they are edited; archive them).

## Known limits

- Assortment is per product, not per product category (a category default
  can be added later if the client needs it).
- Purchase orders raised **by a branch** are not filtered; the check happens
  when the goods are received into the branch's stock.
- The Replenishment report filters by the current company in the switcher.
- Not covered: eCommerce visibility, manufacturing consumption, dropshipping.

## Tests

`tests/test_product_branch_assortment.py` — 14 tests building a throwaway
Parent / Branch A / Sub-branch A1 / Branch B tree at runtime, safe on real
databases (everything is rolled back).

Run on Odoo.sh:

```bash
odoo-bin -d $PGDATABASE -u product_branch_assortment --test-enable --test-tags /product_branch_assortment --stop-after-init
```

## Release notes

- **19.0.1.0.0** (2026-09-16) — initial implementation. Static checks only
  (Python syntax, XML well-formedness, XPath anchors compared with 19.0
  source); runtime installation and tests not yet run.

## Sources

- Odoo 19.0 documentation, *Multi-company*: https://www.odoo.com/documentation/19.0/applications/general/companies/multi_company.html
- Odoo 19.0 documentation, *Companies / Branches*: https://www.odoo.com/documentation/19.0/applications/general/companies.html
- Odoo 19.0 source: `addons/product/security/product_security.xml` (record rule `('company_id', 'parent_of', company_ids)`), `odoo/orm/models.py` (`check_company_domain_parent_of`, `_check_company`), `addons/sale/models/sale_order_line.py` (`_domain_product_id`), `addons/stock/models/stock_orderpoint.py` (`_get_orderpoint_products`).
