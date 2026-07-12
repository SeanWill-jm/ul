from odoo import models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append('public_description')
        return fields
