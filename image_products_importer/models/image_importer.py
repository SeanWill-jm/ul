from odoo import models, fields, api
import base64
import os


class ProductImageImportWizard(models.TransientModel):
    _name = 'product.image.import.wizard'
    _description = 'Wizard to import product images'

    folder_path = fields.Char(string="Folder Path", required=True)

    @api.model
    def import_images(self):
        # This will be replaced with your bulk import logic
        folder = self.folder_path
        if not folder or not os.path.isdir(folder):
            return {'warning': {'title': "Error", 'message': "Invalid folder path"}}

        # TODO: implement actual import logic here
        return {'effect': {'fadeout': 'slow', 'message': 'Images imported', 'type': 'rainbow_man'}}
