# Official Odoo References

Target: Odoo 19.0.

## Purchase RFQ / Deliver To

Odoo documents **Deliver To** as the warehouse operation used to receive the shipment.

https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/purchase/manage_deals/rfq.html

## Purchase Stock model

`purchase.order.picking_type_id` is the standard **Deliver To** field.

https://github.com/odoo/odoo/blob/19.0/addons/purchase_stock/models/purchase_order.py

## Warehouse model

`stock.warehouse.partner_id` is the warehouse Address.

https://github.com/odoo/odoo/blob/19.0/addons/stock/models/stock_warehouse.py

## Standard Purchase report

Standard Odoo uses `dest_address_id` for customer/dropship shipping address.

https://github.com/odoo/odoo/blob/19.0/addons/purchase/report/purchase_order_templates.xml

## Purchase Stock view

Standard Odoo adds the Deliver To field to the Purchase Order form.

https://github.com/odoo/odoo/blob/19.0/addons/purchase_stock/views/purchase_views.xml

## Odoo.sh custom modules

https://www.odoo.com/documentation/19.0/administration/odoo_sh/create_module.html

## Odoo testing

https://www.odoo.com/documentation/19.0/developer/reference/addons/testing.html

## Added for 19.0.1.0.1 (read from the 19.0 branch source text)

- RFQ/PO report templates and actions: `addons/purchase/report/purchase_order_templates.xml`
  (`report_purchaseorder_document`), `addons/purchase/report/purchase_quotation_templates.xml`
  (`report_purchasequotation_document`), `addons/purchase/report/purchase_reports.xml`
  (`action_report_purchase_order`, `report_purchase_quotation`).
  https://github.com/odoo/odoo/tree/19.0/addons/purchase/report
- Portal: `addons/purchase/views/portal_templates.xml` (`purchase_order_portal_content`, `#informations`).
- Form/list/search: `addons/purchase/views/purchase_views.xml` (`purchase_order_form`,
  `purchase_order_view_tree`, `purchase_order_tree`, `view_purchase_order_filter`).
- Callable `domain` on relational fields: `odoo/orm/fields_relational.py`.

Evidence level: source text was read through a summarising fetch, not a checkout, and no Odoo 19
database was available. Anchors are therefore "verified against source text", not runtime-validated.
