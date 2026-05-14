from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta

class ProductProduct(models.Model):
    _inherit = 'product.product'

    avg_sales_per_month = fields.Float(
        string="Average product sales/month",
        compute="_compute_avg_sales_per_month",
        digits=(16, 2),
        help="Formula: (Total quantity sold till date) / (Number of months passed since start date)"
    )

    def _compute_avg_sales_per_month(self):
        start_date_str = self.env['ir.config_parameter'].sudo().get_param('ul_sale_menu_ext.inventory_start_month')
        
        if not start_date_str:
            for product in self:
                product.avg_sales_per_month = 0.0
            return

        start_date_val = fields.Datetime.to_datetime(start_date_str)
        start_date = start_date_val.date()
        today = date.today()
        
        # Calculate months passed. 
        # Using a simple (days / 30.0) or (relativedelta).
        # Let's use days / 30.0 to be more granular, or as requested "number of months passed".
        # If they want integer months, we can use delta.years * 12 + delta.months.
        # But for an average, float months is usually better. 
        # I'll use total days / 30.0 for a more accurate 'average'.
        
        days_passed = (today - start_date).days
        if days_passed <= 0:
            months_passed = 1.0 # Avoid division by zero
        else:
            months_passed = days_passed / 30.0

        # Batch fetch sold quantities to optimize performance
        # We only count sales from the start_date onwards to match the denominator
        sales_data = self.env['sale.order.line'].read_group(
            [
                ('product_id', 'in', self.ids), 
                ('state', 'in', ['sale', 'done']),
                ('order_id.date_order', '>=', start_date)
            ],
            ['product_id', 'product_uom_qty'],
            ['product_id']
        )
        sales_map = {item['product_id'][0]: item['product_uom_qty'] for item in sales_data}

        for product in self:
            if product.product_tmpl_id.id == 6051:
                print(product,sales_map.get(product.id, 0.0),months_passed)
            total_sold = sales_map.get(product.id, 0.0)
            product.avg_sales_per_month = total_sold / months_passed
