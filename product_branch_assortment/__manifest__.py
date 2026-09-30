{
    "name": "Product Branch Assortment",
    "summary": "Central catalogue at the parent company; per-branch sell/stock assortments",
    "description": """
Keeps every product available to the parent company (central purchasing) while
letting each branch sell and stock only the products assigned to it through a
dedicated "Allowed Branches" field. Products are never hidden; the restriction
is enforced on sales order lines, stock moves and reordering rules.
""",
    "version": "19.0.1.0.0",
    "category": "Inventory/Inventory",
    "author": "SWIT Global Consultants",
    "website": "https://switconsulting.com",
    "license": "LGPL-3",
    "depends": ["sale_stock"],
    "data": [
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
