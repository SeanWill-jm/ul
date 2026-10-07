{
    "name": "eCommerce Catalog Tiles",
    "summary": "Shop product tiles with internal reference, on-hand quantity and a quantity picker next to Add to Cart",
    "description": """
Brings the Sales "Catalog" look to the eCommerce shop grid: every product tile
shows the internal reference (SKU), the available on-hand quantity and a
quantity field with -/+ buttons next to the Add to Cart button, so the chosen
quantity goes straight into the cart. Each element can be switched on or off
per website, and the on-hand quantity can be limited to logged-in customers
(wholesale sites).
""",
    "version": "19.0.1.0.1",
    "category": "Website/eCommerce",
    "author": "SWIT Global Consultants",
    "license": "LGPL-3",
    "depends": ["website_sale_stock"],
    "data": [
        "views/product_tile_templates.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_catalog_tiles/static/src/scss/catalog_tiles.scss",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
