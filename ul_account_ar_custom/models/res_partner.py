from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Redefine user_id to add required=True and a default value, 
    # while preserving the base Odoo 17/18/19 compute logic.
    user_id = fields.Many2one(
        'res.users', 
        string='Salesperson',
        compute='_compute_user_id',
        precompute=True,
        readonly=False, 
        store=True,
        required=True,
        default=lambda self: self.env.user,
        help='The internal user in charge of this contact.'
    )
