from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    invoice_policy = fields.Selection(
        selection_add=[('picking', 'Picked Quantities (2-Step)')],
        ondelete={'picking': 'set delivery'},
    )
