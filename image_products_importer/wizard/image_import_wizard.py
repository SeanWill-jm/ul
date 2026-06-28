import base64
import os
from odoo import models, fields


class ProductImageImportWizard(models.TransientModel):
    _name = 'product.image.import.file.wizard'
    _description = 'Import Product Images'

    image_folder = fields.Binary("Zip File of Images", required=True)
    filename = fields.Char("Filename")

    def import_images(self):
        if not self.image_folder:
            return

        # Save zip to temp folder
        zip_path = "/tmp/product_images.zip"
        with open(zip_path, "wb") as f:
            f.write(base64.b64decode(self.image_folder))

        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extract_path = "/tmp/product_images"
            zip_ref.extractall(extract_path)

        products_updated = 0
        for file_name in os.listdir(extract_path):
            if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            name_no_ext = os.path.splitext(file_name)[0].replace("_", " ")
            product = self.env['product.template'].search([
                '|',
                ('default_code', '=', name_no_ext),
                ('name', '=', name_no_ext)
            ], limit=1)

            if product:
                with open(os.path.join(extract_path, file_name), 'rb') as img_file:
                    product.image_1920 = base64.b64encode(img_file.read())
                products_updated += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Import Complete',
                'message': f'{products_updated} products updated with images.',
                'sticky': False,
            }
        }
