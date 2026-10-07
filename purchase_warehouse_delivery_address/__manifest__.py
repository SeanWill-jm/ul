{
    "name": "Purchase Delivery Address",
    "summary": "Pick one tagged contact as the Delivery Address printed on RFQs and Purchase Orders",
    "description": """
Adds an editable Delivery Address to Purchase Orders / RFQs. The dropdown lists
only contacts carrying the "PO Delivery Address" tag, and one contact can be
selected at a time. The selected contact is printed as an extra block on the
RFQ and Purchase Order PDFs, shown on the vendor portal page, and available as
an optional column, search field and group-by in the RFQ/PO lists.

The standard Deliver To (receiving operation) and Dropship Address are not
changed. The technical name is kept from 19.0.1.0.0 so that existing
installations upgrade in place.
""",
    "version": "19.0.1.0.5",
    "category": "Purchases",
    "author": "SWIT Global Consultants",
    "license": "LGPL-3",
    "depends": ["purchase_stock"],
    "data": [
        "data/res_partner_category.xml",
        "views/purchase_order_views.xml",
        "views/purchase_portal_templates.xml",
        "report/purchase_order_report.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
