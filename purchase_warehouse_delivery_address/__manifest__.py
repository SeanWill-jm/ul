{
    "name": "Purchase Warehouse Delivery Address",
    "summary": "Print the selected receiving warehouse address on RFQs and Purchase Orders",
    "version": "19.0.1.0.0",
    "category": "Purchases",
    "author": "SWIT Global Consultants",
    "license": "LGPL-3",
    "depends": ["purchase_stock"],
    "data": [
        "views/purchase_order_views.xml",
        "report/purchase_order_report.xml"
    ],
    "installable": True,
    "application": False,
}
