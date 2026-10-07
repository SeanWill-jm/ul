# Configuration Runbook — Unique Living websites (Odoo.sh 19.0)

Companion to `SOLUTION_DESIGN_unique_living_websites.md` (v3, client sign-off
2026-09-23). Every step below is standard Odoo configuration unless marked
**[module]**. Do it on the `test` (staging) branch first, run the UAT script,
then repeat on production. Tick each box as you go; note deviations in the
right-hand column.

Conventions: UL-JA = Unique Living Jamaica (retail), ULD = UL Distributors
(wholesale), S&L = Supplies and Logistics (parent, no shop).

## 0. Modules

| # | Step | Where | Done / note |
|---|---|---|---|
| 0.1 | Apps installed: Website, eCommerce, Sales, Inventory, Invoicing; `website_sale_stock` (comes with eCommerce + Inventory). | Apps | |
| 0.2 | **[module]** `product_branch_assortment` 19.0.1.0.1 installed (Allowed Branches + default list filter). | shell | |
| 0.3 | **[module]** `website_sale_catalog_tiles` 19.0.1.0.0 installed. | shell | |
| 0.4 | Both committed and pushed to `test`. | shell | |

## 1. Websites

| # | Step | Where | Done / note |
|---|---|---|---|
| 1.1 | Website A "Unique Living" — Company = UL-JA; domain (client's retail domain); theme; Warehouse = UL-JA warehouse (Website › Configuration › Settings › Inventory section). | Website › Configuration › Settings (select website A) | |
| 1.2 | Website B "UL Distributors" — Company = ULD; domain `uldistributors.com`; theme (yellow/white per current site); Warehouse = ULD/Stock. | same, website B | |
| 1.3 | Decide fate of the existing brochure site (becomes A, or stays as a third website). | client | |

## 2. Accounts and access

| # | Step | Where | Done / note |
|---|---|---|---|
| 2.1 | A: Customer Accounts = **Free sign up**; guest checkout allowed (Checkout policy = optional sign-in). | Settings › eCommerce (website A) | |
| 2.2 | B: Customer Accounts = **On invitation**; Shop access / prices for logged-in users only (Settings › eCommerce › Access; and "Shop - Prices" visibility as documented under B2B). | Settings (website B) | |
| 2.3 | B: only Administrators grant portal access: Contacts › customer › Action › Grant portal access. | Contacts | |
| 2.4 | Activity type "Portal access request" (Settings › Technical › Activity Types), default user = an Administrator; reps log it on the customer contact. | Settings | |
| 2.5 | Sales reps: Sales user rights; Website B login as internal users (they see the shop as employees). | Settings › Users | |

## 3. Prices, taxes, payment, invoicing

| # | Step | Where | Done / note |
|---|---|---|---|
| 3.1 | A and B: Display Product Prices = **Tax Included**. | Settings › eCommerce (each website) | |
| 3.2 | Pricelists enabled; create "Retail JMD" (Website = A) and "Wholesale JMD" (Website = B); customer-specific pricelists on ULD customers where needed. | Website › eCommerce › Pricelists | |
| 3.3 | Comparison Price enabled (for RRP strikethrough via Compare to Price). | Settings › eCommerce | |
| 3.4 | Payment provider **Cash on Delivery** enabled on A and on B; every other provider disabled/test only. Provider name shown to customers: "Pay on delivery". | Website › Configuration › Payment Providers | |
| 3.5 | Invoicing policy default = **Delivered quantities** (Settings › eCommerce › Invoicing Policy; common to all websites). Check existing ULD products carry it. | Settings | |
| 3.6 | Automatic Invoice left **off** (it only fires on online payment). Daily routine: Sales › To Invoice › Orders to Invoice → Create Invoices. | Sales | |

## 4. Catalogue

| # | Step | Where | Done / note |
|---|---|---|---|
| 4.1 | eCommerce categories: one tree per website (categories can be restricted to a website). ULD tree: Tools, Plumbing, Paints & Adhesives, Garden & Farm, Bathroom, Kitchen, Hardware… | Website › eCommerce › eCommerce Categories | |
| 4.2 | Import `public_categ_ids` on products (CSV, by category name). | Products › Import | |
| 4.3 | Images: bulk load what exists (file name = internal reference); placeholder for the rest. | Products | |
| 4.4 | Allowed Branches check: ULD list = UL Distributors (done 2026-09-22 import); UL-JA retail products = Unique Living Jamaica; both-site products = both. | Products list › filter "Branch-restricted" | |
| 4.5 | Publish products per website (product form › Website field or bulk "Publish on Website"). Publish the historical catalogue **before** step 5.2 so it is not all "new". | Products | |
| 4.6 | Per product: "Sell when Out-of-Stock" and "Show availability Qty" as the client wants (affects sold-out behaviour and the picker maximum). | Product › Sales tab | |

## 5. New Items and Items for Sale

| # | Step | Where | Done / note |
|---|---|---|---|
| 5.1 | Ribbon "SALE": Assign = On Sale. | Website › eCommerce › Ribbons | |
| 5.2 | Ribbon "NEW": Assign = When New, New period = **30**. Create only after 4.5. | same | |
| 5.3 | Home page (each site): Dynamic Products snippets — one per category section; one "New Items" (sort Newest Arrivals); one "On Sale" (filter on products with a discount / SALE tag). Menu: Home · Categories · New Items · On Sale · Orders (portal). | Website editor | |
| 5.4 | First promotion import: pricelist rules CSV (`pricelist_id`, `applied_on`, `product_tmpl_id/id`, `compute_price`=percentage, `percent_price`, `date_start`, `date_end`, `id` external ID for updates). | Sales › Products › Pricelists › rules import | |
| 5.5 | Verify on the shop: strikethrough + SALE on a promoted product; NEW on a freshly published one. | Shop | |

## 6. Catalog tiles **[module]**

| # | Step | Where | Done / note |
|---|---|---|---|
| 6.1 | A: Catalog Tiles → Reference on, Picker on, On-hand = Everyone (or Never, client choice). | Settings › eCommerce › Catalog Tiles (website A) | |
| 6.2 | B: Reference on, Picker on, On-hand = **Logged-in customers only**. | same (website B) | |
| 6.3 | Website editor tile options (columns, image ratio) as desired; the module's elements sit inside the standard tile. | Shop › Edit | |

## 7. Rep flow (phase 1)

| # | Step | Where | Done / note |
|---|---|---|---|
| 7.1 | Rep on tablet: Website B logged in → showcase; then Sales app › New quotation › Customer › **Catalog** › add lines › Confirm. | Sales (mobile) | |
| 7.2 | Confirmed order → delivery in ULD/Stock → validate → invoice (3.6). Salesperson = rep on order and invoice. | Inventory / Sales | |

## 8. UAT (from design §10)

Run the 9 acceptance criteria in the solution design on staging with: a public
visitor, a retail customer, an invited wholesale customer, a rep, an
administrator. Record results in CLAUDE.md §7/§8 runtime log.

## 9. Production cut-over

Same steps 1–7 on production; modules pushed via the Odoo.sh production
branch; re-run only UAT items 1, 2, 6 and 7 as smoke tests.
