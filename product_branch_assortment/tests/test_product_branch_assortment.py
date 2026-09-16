from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestProductBranchAssortment(TransactionCase):
    """Runs against real databases (Odoo.sh staging), so the test builds its own
    throwaway company tree instead of relying on existing companies:

        Assortment Test Parent
        ├── Assortment Test Branch A
        │   └── Assortment Test Sub-branch A1
        └── Assortment Test Branch B

    Everything created is rolled back with the test transaction. Warehouses are
    created automatically for new companies while tests run (stock.res_company)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Company = cls.env["res.company"]
        cls.parent = Company.create({"name": "Assortment Test Parent"})
        cls.branch_a = Company.create({"name": "Assortment Test Branch A", "parent_id": cls.parent.id})
        cls.branch_b = Company.create({"name": "Assortment Test Branch B", "parent_id": cls.parent.id})
        cls.sub_a1 = Company.create({"name": "Assortment Test Sub-branch A1", "parent_id": cls.branch_a.id})
        cls.all_companies = cls.parent | cls.branch_a | cls.branch_b | cls.sub_a1
        cls.env.user.write({"company_ids": [(4, c.id) for c in cls.all_companies]})

        Warehouse = cls.env["stock.warehouse"]
        cls.wh = {}
        for company in cls.all_companies:
            wh = Warehouse.search([("company_id", "=", company.id)], limit=1)
            if not wh:
                wh = Warehouse.sudo().create({"name": company.name[:30], "code": f"T{company.id}"[:5], "company_id": company.id})
            cls.wh[company.id] = wh

        cls.supplier_loc = cls.env.ref("stock.stock_location_suppliers")
        cls.customer_loc = cls.env.ref("stock.stock_location_customers")
        cls.partner = cls.env["res.partner"].create({"name": "Assortment Test Customer"})

        # Shared product (Company blank) restricted to branch A only.
        cls.product_a_only = cls.env["product.product"].create({
            "name": "Assortment Test Product A-only",
            "type": "consu",
            "is_storable": True,
            "sale_ok": True,
            "purchase_ok": True,
            "allowed_branch_ids": [(6, 0, [cls.branch_a.id])],
        })
        # Shared, unrestricted product.
        cls.product_free = cls.env["product.product"].create({
            "name": "Assortment Test Product Free",
            "type": "consu",
            "is_storable": True,
            "sale_ok": True,
        })

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _sale_line(self, company, product):
        order = self.env["sale.order"].with_company(company).create({
            "partner_id": self.partner.id,
            "company_id": company.id,
            "warehouse_id": self.wh[company.id].id,
        })
        return self.env["sale.order.line"].with_company(company).create({
            "order_id": order.id,
            "product_id": product.id,
            "product_uom_qty": 1,
        })

    def _move(self, company, product, location_src, location_dest, **extra):
        vals = {
            "name": product.display_name,
            "company_id": company.id,
            "product_id": product.id,
            "product_uom_qty": 1,
            "product_uom": product.uom_id.id,
            "location_id": location_src.id,
            "location_dest_id": location_dest.id,
        }
        vals.update(extra)
        return self.env["stock.move"].with_company(company).create(vals)

    def _stock(self, company):
        return self.wh[company.id].lot_stock_id

    # ------------------------------------------------------------------
    # 01-04 assortment logic
    # ------------------------------------------------------------------
    def test_01_empty_list_allows_everyone(self):
        for company in self.all_companies:
            self.assertTrue(self.product_free._is_allowed_for_company(company))

    def test_02_listed_branch_parent_and_subbranch_allowed_sibling_not(self):
        p = self.product_a_only
        self.assertTrue(p._is_allowed_for_company(self.branch_a))
        self.assertTrue(p._is_allowed_for_company(self.sub_a1), "sub-branch of a listed branch")
        self.assertTrue(p._is_allowed_for_company(self.parent), "parent company is never restricted")
        self.assertFalse(p._is_allowed_for_company(self.branch_b))

    def test_03_domain_matches_python_rule(self):
        Product = self.env["product.product"]
        base = [("id", "in", (self.product_a_only | self.product_free).ids)]
        for company, expected in (
            (self.branch_a, self.product_a_only | self.product_free),
            (self.sub_a1, self.product_a_only | self.product_free),
            (self.parent, self.product_a_only | self.product_free),
            (self.branch_b, self.product_free),
        ):
            found = Product.search(base + Product._branch_assortment_domain(company))
            self.assertEqual(found, expected, company.name)

    def test_04_only_branches_of_the_product_company_can_be_listed(self):
        with self.assertRaises(ValidationError):
            self.product_free.product_tmpl_id.write({"allowed_branch_ids": [(4, self.parent.id)]})
        other_root = self.env["res.company"].create({"name": "Assortment Test Other Root"})
        other_branch = self.env["res.company"].create({"name": "Assortment Test Other Branch", "parent_id": other_root.id})
        self.product_free.product_tmpl_id.write({"company_id": self.parent.id})
        with self.assertRaises(ValidationError):
            self.product_free.product_tmpl_id.write({"allowed_branch_ids": [(4, other_branch.id)]})

    # ------------------------------------------------------------------
    # 05-07 sales
    # ------------------------------------------------------------------
    def test_05_sale_line_refused_outside_assortment(self):
        with self.assertRaises(ValidationError):
            self._sale_line(self.branch_b, self.product_a_only)

    def test_06_sale_line_accepted_for_listed_branch_and_parent(self):
        self._sale_line(self.branch_a, self.product_a_only)
        self._sale_line(self.sub_a1, self.product_a_only)
        self._sale_line(self.parent, self.product_a_only)
        self._sale_line(self.branch_b, self.product_free)

    def test_07_sell_down_when_branch_still_holds_stock(self):
        self.env["stock.quant"].with_company(self.branch_b)._update_available_quantity(
            self.product_a_only, self._stock(self.branch_b), 5
        )
        self.assertTrue(self.product_a_only._has_branch_stock(self.branch_b))
        self._sale_line(self.branch_b, self.product_a_only)  # must not raise

    # ------------------------------------------------------------------
    # 08-12 stock
    # ------------------------------------------------------------------
    def test_08_receipt_into_non_allowed_branch_refused(self):
        with self.assertRaises(ValidationError):
            self._move(self.branch_b, self.product_a_only, self.supplier_loc, self._stock(self.branch_b))

    def test_09_receipt_into_allowed_branch_and_parent_accepted(self):
        self._move(self.branch_a, self.product_a_only, self.supplier_loc, self._stock(self.branch_a))
        self._move(self.parent, self.product_a_only, self.supplier_loc, self._stock(self.parent))

    def test_10_outgoing_and_internal_moves_allowed_for_sell_down(self):
        stock_b = self._stock(self.branch_b)
        self._move(self.branch_b, self.product_a_only, stock_b, self.customer_loc)
        shelf = self.env["stock.location"].create({
            "name": "Assortment Test Shelf", "usage": "internal",
            "location_id": stock_b.id, "company_id": self.branch_b.id,
        })
        self._move(self.branch_b, self.product_a_only, stock_b, shelf)

    def test_11_customer_return_allowed(self):
        stock_b = self._stock(self.branch_b)
        delivery = self._move(self.branch_b, self.product_a_only, stock_b, self.customer_loc)
        self._move(self.branch_b, self.product_a_only, self.customer_loc, stock_b,
                   origin_returned_move_id=delivery.id)

    def test_12_inter_branch_transfer_checked_on_destination(self):
        with self.assertRaises(ValidationError):
            self._move(self.parent, self.product_a_only, self._stock(self.parent), self._stock(self.branch_b))
        self._move(self.parent, self.product_a_only, self._stock(self.parent), self._stock(self.branch_a))

    # ------------------------------------------------------------------
    # 13-14 reordering rules
    # ------------------------------------------------------------------
    def test_13_orderpoint_refused_outside_assortment(self):
        with self.assertRaises(ValidationError):
            self.env["stock.warehouse.orderpoint"].with_company(self.branch_b).create({
                "product_id": self.product_a_only.id,
                "warehouse_id": self.wh[self.branch_b.id].id,
                "location_id": self._stock(self.branch_b).id,
                "company_id": self.branch_b.id,
                "product_min_qty": 1, "product_max_qty": 5,
            })

    def test_14_orderpoint_accepted_and_replenishment_products_filtered(self):
        self.env["stock.warehouse.orderpoint"].with_company(self.branch_a).create({
            "product_id": self.product_a_only.id,
            "warehouse_id": self.wh[self.branch_a.id].id,
            "location_id": self._stock(self.branch_a).id,
            "company_id": self.branch_a.id,
            "product_min_qty": 1, "product_max_qty": 5,
        })
        # give the product a move so it is a replenishment candidate
        self._move(self.branch_a, self.product_a_only, self.supplier_loc, self._stock(self.branch_a))
        Orderpoint = self.env["stock.warehouse.orderpoint"]
        self.assertIn(self.product_a_only, Orderpoint.with_company(self.branch_a)._get_orderpoint_products())
        self.assertNotIn(self.product_a_only, Orderpoint.with_company(self.branch_b)._get_orderpoint_products())
        self.assertIn(self.product_a_only, Orderpoint.with_company(self.parent)._get_orderpoint_products())
