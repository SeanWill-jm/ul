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
        
        # Get the last day of the previous month (exclude current running month)
        # If today is May 23, we calculate till April 30
        first_day_current_month = today.replace(day=1)
        last_day_previous_month = first_day_current_month - relativedelta(days=1)
        
        # Calculate number of complete months from start_date to last_day_previous_month
        delta = relativedelta(last_day_previous_month, start_date)
        months_passed = delta.years * 12 + delta.months + 1  # +1 to include the start month
        
        if months_passed <= 0:
            for product in self:
                product.avg_sales_per_month = 0.0
            return

        # Batch fetch sold quantities only till the end of last month
        sales_data = self.env['sale.order.line'].read_group(
            [
                ('product_id', 'in', self.ids), 
                ('state', 'in', ['sale', 'done']),
                ('order_id.date_order', '>=', start_date),
                ('order_id.date_order', '<=', last_day_previous_month)
            ],
            ['product_id', 'product_uom_qty'],
            ['product_id']
        )
        sales_map = {item['product_id'][0]: item['product_uom_qty'] for item in sales_data}

        for product in self:
            total_sold = sales_map.get(product.id, 0.0)
            product.avg_sales_per_month = total_sold / months_passed
