# Configuration Guide

## Warehouse addresses

Go to **Inventory → Configuration → Warehouses**. For each receiving warehouse, verify the **Address** field contains the exact physical destination vendors should use.

Example:

```text
Warehouse: Kingston Main Warehouse
Address:
Kingston Main Warehouse
10 Industrial Avenue
Kingston 11
Jamaica
```

## Multiple warehouses

Configure each physical receiving site as the appropriate Odoo warehouse. Buyers then use the standard **Deliver To** dropdown on the RFQ/PO.

## Behavior

- Buyer changes **Deliver To**.
- Odoo resolves the selected operation's warehouse.
- Module resolves the warehouse Address.
- The read-only Delivery Address changes automatically.
- The same address prints on the RFQ/PO.

## Storage Locations

Ensure the relevant Inventory settings and warehouse structure are enabled so the required receiving warehouse operations are available to Purchase users.

## Dropship

Use standard Odoo Dropship and Dropship Address for direct vendor-to-customer delivery.
