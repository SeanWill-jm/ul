from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

TAG_XMLID = "purchase_warehouse_delivery_address.partner_category_po_delivery_address"


@tagged("post_install", "-at_install")
class TestPurchaseDeliveryAddress(TransactionCase):
    """Tests create their own throwaway records; safe on databases with real data."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.tag = cls.env.ref(TAG_XMLID)
        cls.vendor = cls.env["res.partner"].create({"name": "PDA Test Vendor"})
        cls.site_a = cls.env["res.partner"].create({
            "name": "PDA Test Site A",
            "street": "10 Test Industrial Avenue",
            "city": "Kingston",
            "phone": "876-555-0101",
            "category_id": [(4, cls.tag.id)],
        })
        cls.site_b = cls.env["res.partner"].create({
            "name": "PDA Test Site B",
            "street": "20 Test Distribution Road",
            "city": "Montego Bay",
            "category_id": [(4, cls.tag.id)],
        })
        cls.untagged = cls.env["res.partner"].create({
            "name": "PDA Test Untagged",
            "street": "30 Nowhere Lane",
        })

    def _po(self, **vals):
        return self.env["purchase.order"].create({
            "partner_id": self.vendor.id,
            "company_id": self.company.id,
            **vals,
        })

    def _render(self, report_ref, po):
        html, _kind = self.env["ir.actions.report"]._render_qweb_html(report_ref, po.ids)
        return html.decode() if isinstance(html, bytes) else html

    # -- model ---------------------------------------------------------------
    def test_01_tag_is_created_by_module(self):
        self.assertEqual(self.tag.name, "PO Delivery Address")

    def test_02_field_is_single_stored_editable_many2one(self):
        field = self.env["purchase.order"]._fields["po_delivery_address_id"]
        self.assertEqual(field.type, "many2one")
        self.assertEqual(field.comodel_name, "res.partner")
        self.assertTrue(field.store)
        self.assertFalse(field.readonly)
        self.assertFalse(field.related)
        self.assertEqual(field.string, "Delivery Address")

    def test_03_old_readonly_related_field_is_gone(self):
        self.assertNotIn("warehouse_delivery_address_id", self.env["purchase.order"]._fields)

    def test_04_domain_lists_only_tagged_contacts(self):
        domain = self.env["purchase.order"]._po_delivery_address_domain()
        listed = self.env["res.partner"].search(domain)
        self.assertIn(self.site_a, listed)
        self.assertIn(self.site_b, listed)
        self.assertNotIn(self.untagged, listed)

    def test_05_select_and_change_one_contact(self):
        po = self._po(po_delivery_address_id=self.site_a.id)
        self.assertEqual(po.po_delivery_address_id, self.site_a)
        po.po_delivery_address_id = self.site_b
        self.assertEqual(po.po_delivery_address_id, self.site_b)
        po.po_delivery_address_id = False
        self.assertFalse(po.po_delivery_address_id)

    def test_06_untagged_contact_rejected(self):
        with self.assertRaises(ValidationError):
            self._po(po_delivery_address_id=self.untagged.id)
        po = self._po()
        with self.assertRaises(ValidationError):
            po.po_delivery_address_id = self.untagged

    def test_07_removing_tag_later_does_not_block_other_edits(self):
        po = self._po(po_delivery_address_id=self.site_a.id)
        self.site_a.category_id = [(3, self.tag.id)]
        po.partner_ref = "PDA-REF-1"  # unrelated write must still work
        self.assertEqual(po.partner_ref, "PDA-REF-1")
        self.assertEqual(po.po_delivery_address_id, self.site_a)

    def test_08_editable_in_every_state(self):
        po = self._po()
        # Read the states from the field itself: 19.0 has no 'done' state (it uses `locked`).
        states = [key for key, _label in self.env["purchase.order"]._fields["state"].selection]
        self.assertIn("purchase", states)
        for state in states:
            for locked in (False, True):
                po.write({"state": state, "locked": locked})
                po.po_delivery_address_id = self.site_a
                po.po_delivery_address_id = self.site_b
                self.assertEqual(po.po_delivery_address_id, self.site_b, (state, locked))

    def test_09_duplicate_keeps_address(self):
        po = self._po(po_delivery_address_id=self.site_a.id)
        self.assertEqual(po.copy().po_delivery_address_id, self.site_a)

    # -- views ---------------------------------------------------------------
    def test_10_form_view_has_field_without_readonly(self):
        arch = self.env["purchase.order"].get_view(view_type="form")["arch"]
        self.assertIn('name="po_delivery_address_id"', arch)

    # -- reports -------------------------------------------------------------
    def test_11_po_report_prints_selected_contact(self):
        po = self._po(po_delivery_address_id=self.site_a.id)
        html = self._render("purchase.report_purchaseorder", po)
        self.assertIn("po_delivery_address_block", html)
        self.assertIn("PDA Test Site A", html)
        self.assertIn("10 Test Industrial Avenue", html)

    def test_12_rfq_report_prints_selected_contact(self):
        po = self._po(po_delivery_address_id=self.site_b.id)
        html = self._render("purchase.report_purchasequotation", po)
        self.assertIn("po_delivery_address_block", html)
        self.assertIn("PDA Test Site B", html)

    def test_13_reports_unchanged_when_empty(self):
        po = self._po()
        for ref in ("purchase.report_purchaseorder", "purchase.report_purchasequotation"):
            self.assertNotIn("po_delivery_address_block", self._render(ref, po))

    def test_14_deliver_to_is_not_touched(self):
        po = self._po(po_delivery_address_id=self.site_a.id)
        self.assertTrue(po.picking_type_id)  # standard Deliver To still resolved by Odoo
        self.assertNotEqual(po.picking_type_id.warehouse_id.partner_id, self.site_a)

    # -- 1.0.4 report layout ----------------------------------------------------
    def _vendor_with_vat(self):
        return self.env["res.partner"].with_context(no_vat_validation=True).create({
            "name": "PDA Test Vendor VAT",
            "vat": "PDA-TAX-12345",
            "street": "1 Vendor Street",
        })

    def test_15_vendor_block_prints_tax_id_label_once(self):
        vendor = self._vendor_with_vat()
        for ref in ("purchase.report_purchaseorder", "purchase.report_purchasequotation"):
            po = self._po(partner_id=vendor.id)
            html = self._render(ref, po)
            self.assertIn("TAX ID:", html, ref)
            self.assertIn("po_partner_tax_id", html, ref)
            # printed exactly once: the contact widget must no longer print it as "VAT"
            self.assertEqual(html.count("PDA-TAX-12345"), 1, ref)

    def test_16_no_tax_line_when_vendor_has_no_vat(self):
        po = self._po()
        for ref in ("purchase.report_purchaseorder", "purchase.report_purchasequotation"):
            self.assertNotIn("po_partner_tax_id", self._render(ref, po), ref)

    def test_17_shipping_block_hidden_only_when_delivery_address_set(self):
        dropship = self.env["res.partner"].create({
            "name": "PDA Test Dropship Customer",
            "street": "77 Dropship Street",
        })
        for ref in ("purchase.report_purchaseorder", "purchase.report_purchasequotation"):
            plain = self._po(dest_address_id=dropship.id)
            self.assertIn("77 Dropship Street", self._render(ref, plain), ref)
            both = self._po(dest_address_id=dropship.id, po_delivery_address_id=self.site_a.id)
            html = self._render(ref, both)
            self.assertNotIn("77 Dropship Street", html, ref)
            self.assertIn("PDA Test Site A", html, ref)

