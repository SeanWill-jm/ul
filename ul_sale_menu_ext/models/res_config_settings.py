from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inventory_start_month = fields.Datetime(
        string="Inventory Calculation Start Date",
        config_parameter='ul_sale_menu_ext.inventory_start_month',
        help="Start date to calculate the number of months passed for average sales calculation."
    )
