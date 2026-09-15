# Purchase Warehouse Delivery Address — Odoo.sh 19.0

## Purpose

This module implements the internal warehouse delivery scenario for Odoo Purchase Orders. It deliberately uses Odoo's standard **Deliver To** field instead of creating a second warehouse selector.

The selected receiving operation determines the warehouse, and the module resolves that warehouse's configured **Address**. It then:

1. displays a read-only **Delivery Address** on the Purchase Order form; and
2. prints the address on the standard RFQ/Purchase Order PDF.

This keeps the physical PO synchronized with the warehouse used by Odoo to create the incoming receipt.

## Target

- Odoo.sh
- Odoo 19.0
- Purchase + Inventory (`purchase_stock`)

## Technical name

`purchase_warehouse_delivery_address`

## Version

`19.0.1.0.0`

## Core mapping

`purchase.order.picking_type_id` → `stock.picking.type.warehouse_id` → `stock.warehouse.partner_id`

The custom read-only field is:

`purchase.order.warehouse_delivery_address_id`

## Dropship compatibility

Standard Odoo uses `dest_address_id` for dropship/customer delivery. This module does not replace or duplicate that flow. The internal warehouse address block is rendered only when there is no dropship address.

## Quick setup

1. Install on an Odoo.sh Development/Staging branch.
2. Configure every receiving warehouse's **Address**.
3. Create an RFQ.
4. Select **Deliver To**.
5. Review the derived Delivery Address.
6. Print the RFQ/PO and verify the address.
7. Complete UAT before Production.

See `docs/` for complete documentation.
