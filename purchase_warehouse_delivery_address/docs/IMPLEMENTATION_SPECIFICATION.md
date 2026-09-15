# Implementation Specification

## In scope

- Odoo.sh 19.0.
- Internal warehouse receiving.
- Standard Deliver To selection.
- Read-only delivery-address display.
- RFQ/Purchase Order PDF output.

## Out of scope

- Arbitrary non-warehouse delivery sites.
- New destination master model.
- Dropship redesign.
- Routing/carrier integration.
- Warehouse creation.

## Field

| Attribute | Value |
|---|---|
| Model | `purchase.order` |
| Field | `warehouse_delivery_address_id` |
| Label | Delivery Address |
| Type | Many2one |
| Target | `res.partner` |
| Related path | `picking_type_id.warehouse_id.partner_id` |
| Editable | No |
| Stored | No |

## Report condition

Print the internal warehouse address only when `dest_address_id` is empty and `warehouse_delivery_address_id` is present.

## Failure behavior

The module does not fabricate fallback delivery addresses. If a warehouse is misconfigured, correct its Address.
