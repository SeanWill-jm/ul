from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestCatalogTiles(HttpCase):
    """Runs against real databases; creates its own published product and
    rolls everything back."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].get_current_website()
        # Pin the website to a warehouse of its company so free_qty is unambiguous
        # (an empty website warehouse means "all warehouses of the company").
        cls.warehouse = cls.website.warehouse_id or cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.website.company_id.id)], limit=1
        )
        cls.website.write({
            "warehouse_id": cls.warehouse.id,
            "tile_show_reference": True,
            "tile_show_on_hand": "all",
            "tile_quantity_picker": True,
        })
        cls.product = cls.env["product.product"].create({
            "name": "Catalog Tile Test Product",
            "default_code": "CTT-TEST-001",
            "type": "consu",
            "is_storable": True,
            "sale_ok": True,
            "list_price": 12.5,
            "website_published": True,
            "allow_out_of_stock_order": False,
        })
        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.warehouse.lot_stock_id, 7
        )

    def test_01_on_hand_info_reads_website_warehouse(self):
        info = self.product.product_tmpl_id._tile_on_hand_info(self.product, self.website)
        self.assertTrue(info["is_storable"])
        self.assertEqual(info["free_qty"], 7)
        self.assertFalse(info["allow_out_of_stock"])

    def test_02_on_hand_visibility_policy(self):
        public = self.env.ref("base.public_user")
        self.website.tile_show_on_hand = "logged"
        self.assertFalse(self.website.with_user(public)._tile_can_show_on_hand())
        self.assertTrue(self.website._tile_can_show_on_hand())
        self.website.tile_show_on_hand = "none"
        self.assertFalse(self.website._tile_can_show_on_hand())
        self.website.tile_show_on_hand = "all"
        self.assertTrue(self.website.with_user(public)._tile_can_show_on_hand())

    def test_03_shop_tile_renders_reference_stock_and_picker(self):
        html = self.url_open("/shop?search=CTT-TEST-001").text
        self.assertIn("CTT-TEST-001", html)
        self.assertIn("o_wsct_on_hand", html)
        self.assertIn("7 On Hand", html)
        self.assertIn('name="add_qty"', html)
        self.assertIn('data-max="7"', html)
        self.assertIn("js_add_cart_json", html)

    def test_04_settings_switch_elements_off(self):
        self.website.write({
            "tile_show_reference": False,
            "tile_show_on_hand": "none",
            "tile_quantity_picker": False,
        })
        html = self.url_open("/shop?search=CTT-TEST-001").text
        self.assertNotIn("o_wsct_reference", html)
        self.assertNotIn("o_wsct_on_hand", html)
        self.assertNotIn("o_wsct_qty", html)
        self.assertIn("o_wsale_product_btn_primary", html)

    def test_05_standard_classes_preserved_for_other_modules(self):
        """Other modules (comparison, wishlist...) anchor on these classes with hasclass();
        this module must only add classes, never drop the standard ones."""
        html = self.url_open("/shop?search=CTT-TEST-001").text
        self.assertIn("o_wsale_product_action_row", html)
        self.assertIn("o_wsct_action_row", html)
        self.assertIn("o_wsale_product_btn_primary", html)
        self.assertIn("o_wsct_add_btn", html)
