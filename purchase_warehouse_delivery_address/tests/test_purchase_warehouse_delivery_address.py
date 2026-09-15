from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestPurchaseWarehouseDeliveryAddress(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.vendor = cls.env["res.partner"].create({
            "name": "Test Purchase Vendor",
            "supplier_rank": 1,
        })
        cls.address_a = cls.env["res.partner"].create({
            "name": "Receiving Warehouse A",
            "street": "10 Test Industrial Avenue",
            "city": "Kingston",
            "country_id": cls.company.country_id.id or False,
            "company_id": cls.company.id,
        })
        cls.address_b = cls.env["res.partner"].create({
            "name": "Receiving Warehouse B",
            "street": "20 Test Distribution Road",
            "city": "Montego Bay",
            "country_id": cls.company.country_id.id or False,
            "company_id": cls.company.id,
        })
        cls.warehouse_a = cls.env["stock.warehouse"].create({
            "name": "Test Receiving Warehouse A",
            "code": "TWA",
            "company_id": cls.company.id,
            "partner_id": cls.address_a.id,
        })
        cls.warehouse_b = cls.env["stock.warehouse"].create({
            "name": "Test Receiving Warehouse B",
            "code": "TWB",
            "company_id": cls.company.id,
            "partner_id": cls.address_b.id,
        })

    def test_delivery_address_follows_deliver_to_warehouse(self):
        po = self.env["purchase.order"].create({
            "partner_id": self.vendor.id,
            "company_id": self.company.id,
            "picking_type_id": self.warehouse_a.in_type_id.id,
        })
        self.assertEqual(po.warehouse_delivery_address_id, self.address_a)
        po.picking_type_id = self.warehouse_b.in_type_id
        self.assertEqual(po.warehouse_delivery_address_id, self.address_b)

    def test_field_is_readonly_related_value(self):
        field = self.env["purchase.order"]._fields["warehouse_delivery_address_id"]
        self.assertTrue(field.readonly)
        self.assertEqual(field.related, ("picking_type_id", "warehouse_id", "partner_id"))
