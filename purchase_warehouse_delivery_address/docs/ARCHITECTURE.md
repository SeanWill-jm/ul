# Architecture

## Business requirement

The buyer selects the internal receiving warehouse and the RFQ/Purchase Order must print that warehouse's physical delivery address.

## Design decision

No parallel address selector is introduced. Odoo 19 already defines `purchase.order.picking_type_id` as **Deliver To**. It points to the incoming `stock.picking.type`, which belongs to a `stock.warehouse`. The warehouse address is `stock.warehouse.partner_id`.

## Data flow

```text
Deliver To
  ↓
purchase.order.picking_type_id
  ↓
stock.picking.type.warehouse_id
  ↓
stock.warehouse.partner_id
  ↓
PO Delivery Address + RFQ/PO PDF
```

## Why this architecture

A second independent address field could create a mismatch between the address printed to the vendor and the warehouse used for the actual receipt. Using the standard Deliver To selection preserves one source of truth.

## Dropship separation

Standard Odoo `dest_address_id` remains authoritative for direct vendor-to-customer delivery. The internal warehouse block is suppressed when a dropship address exists.

## Upgradeability

The module inherits standard models, views, and reports. It does not modify core code or override receipt creation.
