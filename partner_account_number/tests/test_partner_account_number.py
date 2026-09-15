from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestPartnerAccountNumber(TransactionCase):
    """Runs against real databases (Odoo.sh staging with migrated data), so every
    prefix and suffix used here is chosen at runtime from values that are free.
    Everything created is rolled back with the test transaction."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Company = cls.env["res.company"].with_context(active_test=False)
        Partner = cls.env["res.partner"].with_context(active_test=False)

        used_prefixes = set(
            Company.search([("partner_account_prefix", "!=", False)]).mapped(
                "partner_account_prefix"
            )
        )
        free = [f"{n:03d}" for n in range(999, 899, -1) if f"{n:03d}" not in used_prefixes]
        cls.prefix_a, cls.prefix_b, cls.prefix_unassigned = free[0], free[1], free[2]

        cls.branch_a = Company.create(
            {"name": f"Account Test Branch {cls.prefix_a}", "partner_account_prefix": cls.prefix_a}
        )
        cls.branch_b = Company.create(
            {"name": f"Account Test Branch {cls.prefix_b}", "partner_account_prefix": cls.prefix_b}
        )

        # Suffix pool: six-digit values with a leading zero (so the legacy 5-digit
        # form round-trips through zero-padding) not used by any partner, active
        # or archived. Taken from the top of the 0xxxxx range downwards.
        used_suffixes = set(
            Partner.search([("customer_account_suffix", "!=", False)]).mapped(
                "customer_account_suffix"
            )
        )
        cls._suffix_pool = iter(
            f"{n:06d}" for n in range(99999, 10000, -1) if f"{n:06d}" not in used_suffixes
        )

        # Generator start for tests: first free value at/after 700001.
        cls.seq_start = next(
            n for n in range(700001, 799999) if f"{n:06d}" not in used_suffixes
        )
        cls.sequence = cls.env.ref("partner_account_number.seq_partner_account_suffix")

    def setUp(self):
        super().setUp()
        # PostgreSQL sequences advance outside transaction rollback, so a test
        # that consumes values would shift the next test's expectations. Reset
        # the counter before every test (ALTER SEQUENCE ... RESTART is
        # transactional and is rolled back with the test).
        self.sequence.sudo().write({"number_next": self.seq_start})

    @classmethod
    def suffix(cls):
        """Next free six-digit suffix (as a string with leading zeros)."""
        return next(cls._suffix_pool)

    @staticmethod
    def short(suffix):
        """Legacy form of a pool suffix: leading zeros dropped (``099998`` -> ``99998``)."""
        return suffix.lstrip("0")

    # -------------------------------------------------------------------------
    # Original behaviour (01–06)
    # -------------------------------------------------------------------------

    def test_01_imported_account_infers_branch(self):
        sfx = self.suffix()
        partner = self.env["res.partner"].create(
            {
                "name": "Imported Customer",
                "customer_type": "customer",
                "customer_account_no": f"{self.prefix_a}-{sfx}",
            }
        )
        self.assertEqual(partner.account_branch_id, self.branch_a)
        self.assertEqual(partner.customer_account_suffix, sfx)
        self.assertFalse(partner.legacy_account_no)

    def test_02_generator_skips_existing_imported_suffix(self):
        reserved = f"{self.seq_start:06d}"
        self.env["res.partner"].create(
            {
                "name": "Reserved Imported Number",
                "customer_type": "customer",
                "customer_account_no": f"{self.prefix_a}-{reserved}",
            }
        )
        generated = self.env["res.partner"].create(
            {
                "name": "Generated Customer",
                "customer_type": "customer",
                "account_branch_id": self.branch_b.id,
            }
        )
        self.assertEqual(generated.customer_account_no, f"{self.prefix_b}-{self.seq_start + 1:06d}")
        self.assertEqual(generated.customer_account_suffix, f"{self.seq_start + 1:06d}")

    def test_03_suffix_is_global_across_prefixes(self):
        sfx = self.suffix()
        self.env["res.partner"].create(
            {
                "name": "Branch A Customer",
                "customer_type": "customer",
                "customer_account_no": f"{self.prefix_a}-{sfx}",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Branch B Duplicate",
                    "customer_type": "vendor",
                    "customer_account_no": f"{self.prefix_b}-{sfx}",
                }
            )

    def test_04_prefix_must_match_selected_branch(self):
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Mismatched Branch",
                    "customer_type": "customer",
                    "customer_account_no": f"{self.prefix_a}-{self.suffix()}",
                    "account_branch_id": self.branch_b.id,
                }
            )

    def test_05_account_and_branch_are_immutable(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Immutable Customer",
                "customer_type": "customer",
                "customer_account_no": f"{self.prefix_a}-{self.suffix()}",
            }
        )
        with self.assertRaises(UserError):
            partner.write({"customer_account_no": f"{self.prefix_a}-{self.suffix()}"})
        with self.assertRaises(UserError):
            partner.write({"account_branch_id": self.branch_b.id})

    def test_06_numbered_partner_cannot_be_deleted(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Archive Me",
                "customer_type": "vendor",
                "customer_account_no": f"{self.prefix_b}-{self.suffix()}",
            }
        )
        with self.assertRaises(UserError):
            partner.unlink()

    # -------------------------------------------------------------------------
    # Legacy (ManageMore) normalization (07–17)
    # -------------------------------------------------------------------------

    def test_07_legacy_number_without_prefix_uses_current_company(self):
        sfx = self.suffix()
        raw = self.short(sfx)
        partner = self.env["res.partner"].with_company(self.branch_b).create(
            {"name": "Legacy no prefix", "customer_type": "customer", "customer_account_no": raw}
        )
        self.assertEqual(partner.customer_account_no, f"{self.prefix_b}-{raw.zfill(6)}")
        self.assertEqual(partner.customer_account_suffix, raw.zfill(6))
        self.assertEqual(partner.account_branch_id, self.branch_b)
        self.assertEqual(partner.legacy_account_no, raw)

    def test_08_legacy_number_with_leading_dash(self):
        raw = "-" + self.short(self.suffix())
        partner = self.env["res.partner"].with_company(self.branch_a).create(
            {"name": "Legacy dash", "customer_type": "vendor", "customer_account_no": raw}
        )
        self.assertEqual(partner.customer_account_no, f"{self.prefix_a}-{raw[1:].zfill(6)}")
        self.assertEqual(partner.legacy_account_no, raw)

    def test_09_prefixless_value_current_company_wins_over_branch_column(self):
        raw = self.short(self.suffix())
        partner = self.env["res.partner"].with_company(self.branch_b).create(
            {
                "name": "Legacy with branch column",
                "customer_type": "customer",
                "customer_account_no": raw,
                "account_branch_id": self.branch_a.id,
            }
        )
        self.assertEqual(partner.customer_account_no, f"{self.prefix_b}-{raw.zfill(6)}")
        self.assertEqual(partner.account_branch_id, self.branch_b)

    def test_10_short_suffix_with_prefix_is_padded(self):
        sfx = self.suffix()
        raw = f"{self.prefix_a}-{self.short(sfx)}"
        partner = self.env["res.partner"].create(
            {"name": "Legacy short", "customer_type": "customer", "customer_account_no": raw}
        )
        self.assertEqual(partner.customer_account_no, f"{self.prefix_a}-{sfx}")
        self.assertEqual(partner.legacy_account_no, raw)

    def test_11_canonical_number_has_no_legacy_value(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Canonical",
                "customer_type": "customer",
                "customer_account_no": f"{self.prefix_a}-{self.suffix()}",
            }
        )
        self.assertFalse(partner.legacy_account_no)

    def test_12_legacy_normalization_still_enforces_global_uniqueness(self):
        raw = self.short(self.suffix())
        self.env["res.partner"].with_company(self.branch_a).create(
            {"name": "Legacy once", "customer_type": "customer", "customer_account_no": raw}
        )
        with self.assertRaises(ValidationError):
            self.env["res.partner"].with_company(self.branch_b).create(
                {"name": "Legacy twice", "customer_type": "customer", "customer_account_no": raw}
            )

    def test_13_invalid_legacy_value_is_rejected(self):
        for bad in ("ABC-12", "1234567890", "0103-30007", "12-3456"):
            with self.assertRaises(ValidationError, msg=bad):
                self.env["res.partner"].create(
                    {"name": "Bad value", "customer_type": "customer", "customer_account_no": bad}
                )

    def test_14_generator_unaffected_by_legacy_range(self):
        self.env["res.partner"].with_company(self.branch_a).create(
            {
                "name": "Legacy before generation",
                "customer_type": "customer",
                "customer_account_no": self.short(self.suffix()),
            }
        )
        generated = self.env["res.partner"].create(
            {
                "name": "Generated after legacy",
                "customer_type": "customer",
                "account_branch_id": self.branch_a.id,
            }
        )
        self.assertEqual(generated.customer_account_no, f"{self.prefix_a}-{self.seq_start:06d}")
        self.assertFalse(generated.legacy_account_no)

    def test_15_unassigned_prefix_falls_back_to_current_company(self):
        sfx = self.suffix()
        raw = f"{self.prefix_unassigned}-{self.short(sfx)}"
        partner = self.env["res.partner"].with_company(self.branch_a).create(
            {"name": "Legacy unassigned prefix", "customer_type": "customer", "customer_account_no": raw}
        )
        self.assertEqual(partner.customer_account_no, f"{self.prefix_a}-{self.short(sfx).zfill(6)}")
        self.assertEqual(partner.account_branch_id, self.branch_a)
        self.assertEqual(partner.legacy_account_no, raw)

    def test_16_assigned_prefix_in_value_wins_over_current_company(self):
        sfx = self.suffix()
        raw = f"{self.prefix_b}-{self.short(sfx)}"
        partner = self.env["res.partner"].with_company(self.branch_a).create(
            {"name": "Legacy assigned prefix", "customer_type": "customer", "customer_account_no": raw}
        )
        self.assertEqual(partner.customer_account_no, f"{self.prefix_b}-{self.short(sfx).zfill(6)}")
        self.assertEqual(partner.account_branch_id, self.branch_b)
        self.assertEqual(partner.legacy_account_no, raw)

    def test_17_current_company_without_prefix_is_rejected(self):
        no_prefix_company = self.env["res.company"].create({"name": "No Prefix Company"})
        with self.assertRaises(ValidationError):
            self.env["res.partner"].with_company(no_prefix_company).create(
                {
                    "name": "Legacy without usable prefix",
                    "customer_type": "customer",
                    "customer_account_no": self.short(self.suffix()),
                }
            )

    def test_18_concatenated_prefix_and_suffix_without_dash(self):
        # Export dropped the dash: "PPPNNNNN" / "PPPNNNNNN".
        sfx = self.suffix()                       # e.g. 099998
        Partner = self.env["res.partner"].with_company(self.branch_a)
        # assigned prefix, 5-digit suffix run together -> prefix kept
        raw = f"{self.prefix_b}{self.short(sfx)}"
        partner = Partner.create(
            {"name": "Concat assigned", "customer_type": "customer", "customer_account_no": raw}
        )
        self.assertEqual(partner.customer_account_no, f"{self.prefix_b}-{sfx}")
        self.assertEqual(partner.account_branch_id, self.branch_b)
        self.assertEqual(partner.legacy_account_no, raw)
        # unassigned prefix, 6-digit suffix run together -> current company
        sfx2 = self.suffix()
        raw2 = f"{self.prefix_unassigned}{sfx2}"
        partner2 = Partner.create(
            {"name": "Concat unassigned", "customer_type": "customer", "customer_account_no": raw2}
        )
        self.assertEqual(partner2.customer_account_no, f"{self.prefix_a}-{sfx2}")
        self.assertEqual(partner2.account_branch_id, self.branch_a)
        self.assertEqual(partner2.legacy_account_no, raw2)
