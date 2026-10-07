# Purchase Delivery Address — Odoo.sh 19.0

Version: 19.0.1.0.5 · Last Updated: 2026-10-07 · Copyright © 2026 SWIT Global Consultants · Created by: SWIT Global Consultants

> In Odoo: Apps › this module's card › **Module Info** shows the same guide (`static/description/index.html`).

(Technical name `purchase_warehouse_delivery_address`, kept from 19.0.1.0.0 so existing
installations upgrade in place. The display name is now "Purchase Delivery Address".)

## Purpose

Adds an editable **Delivery Address** (`purchase.order.po_delivery_address_id`) to RFQs and
Purchase Orders.

- The dropdown lists **only contacts tagged `PO Delivery Address`**.
- **One contact at a time** (Many2one). It can be changed in any state.
- It is printed as an **extra block** on the RFQ and Purchase Order PDFs (both 19.0 report
  templates), shown on the vendor portal page, and available as an optional column, search
  field and Group By in the RFQ/PO lists.
- Empty = the documents print as standard Odoo does (standard Shipping address included).
- When set, the standard **Shipping address** (Dropship) block is hidden and the vendor tax number prints as **TAX ID:** (1.0.4).

It does **not** change **Deliver To** (`picking_type_id`, the receiving operation), the
**Dropship Address** (`dest_address_id`) or the receipt created on confirmation.

## Target

Odoo.sh 19.0 — depends on `purchase_stock` (unchanged from 1.0.0).

## Version

`19.0.1.0.4` — (1.0.1 failed view validation on Staging, see `PATCH_NOTES_19.0.1.0.2.md`) replaces the read-only, warehouse-derived Delivery Address of 1.0.0.
See `PATCH_NOTES_19.0.1.0.1.md`, `PATCH_NOTES_19.0.1.0.2.md`, `PATCH_NOTES_19.0.1.0.3.md`, `PATCH_NOTES_19.0.1.0.4.md` and `docs/`.

## Quick setup

1. Upgrade the module on Staging (see `docs/INSTALLATION.md`).
2. Open **Contacts**, edit each delivery site contact and add the tag **PO Delivery Address**.
3. Create an RFQ, pick the contact in **Delivery Address** (under Currency).
4. Print the RFQ / PO and check the block.
5. Complete UAT before Production.

---
License: LGPL-3 · Summary: tagged-contact Delivery Address on RFQs and POs, printed on the PDFs · Platform Version: Odoo 19.0 (Odoo.sh) · Status: Staging validated (1.0.4); UAT pending
Copyright © 2026 SWIT Global Consultants — https://switconsulting.com · Created by: SWIT Global Consultants
