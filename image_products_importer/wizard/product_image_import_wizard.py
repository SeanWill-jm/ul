from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import zipfile
import io
import re
import logging

_logger = logging.getLogger(__name__)


class ProductImageImportWizard(models.TransientModel):
    _name = 'product.image.import.wizard'
    _description = 'Product Image Import Wizard'

    zip_file = fields.Binary(string="ZIP File", required=True)
    filename = fields.Char("Filename")

    def _normalize_key(self, text):
        if not text:
            return ""
        text = text.lower().strip()
        text = re.sub(r"[_-]+", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def action_import_images(self):
        self.ensure_one()

        if not self.zip_file:
            raise UserError(_("Please upload a ZIP file."))

        try:
            zip_data = base64.b64decode(self.zip_file)
            zip_file = zipfile.ZipFile(io.BytesIO(zip_data))
        except Exception:
            raise UserError(_("Invalid ZIP file."))

        exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')
        image_files = [f for f in zip_file.namelist()
                       if f.lower().endswith(exts)]
        if not image_files:
            raise UserError(_("No image files found in the ZIP."))

        PT = self.env['product.template'].sudo()
        image_field = 'image_1920' if 'image_1920' in PT._fields else 'image'

        products = PT.search([])
        product_map = {}
        for prod in products:
            for key in filter(None, [
                self._normalize_key(prod.default_code),
                self._normalize_key(prod.name),
                self._normalize_key(prod.barcode),  # ✅ Added barcode matching
            ]):
                product_map.setdefault(key, []).append(prod)

        matched, unmatched = 0, []
        for filename in image_files:
            name_no_ext = filename.split("/")[-1].rsplit(".", 1)[0]
            norm_name = self._normalize_key(name_no_ext)

            candidates = product_map.get(norm_name)
            if not candidates:
                unmatched.append(filename)
                continue

            product = candidates[0]
            try:
                product[image_field] = base64.b64encode(
                    zip_file.read(filename))
                matched += 1
            except Exception as e:
                raise UserError(_("Failed to process %s: %s") %
                                (filename, str(e)))

        # ✅ Professional success notification
        msg = _("✅ %s images imported.\n❌ %s unmatched.") % (
            matched, len(unmatched))
        if unmatched:
            msg += _("\nExamples: %s") % ", ".join(unmatched[:10])

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Import Complete"),
                'message': msg,
                'type': 'success',
                'sticky': False,  # auto disappear after a few seconds
            }
        }
