from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        if 'qty_available' in self._fields and 'qty_available' not in fields:
            fields.append('qty_available')
        return fields

    @api.model
    def _load_pos_data_read(self, records, config):
        res = super()._load_pos_data_read(records, config)

        # Optimize stock fetching by reading stock.quant directly (like pos_smart_discount_control)
        warehouse = config.picking_type_id.warehouse_id or config.warehouse_id
        if warehouse and warehouse.lot_stock_id:
            location = warehouse.lot_stock_id
            all_locations = self.env['stock.location'].sudo().search([
                ('id', 'child_of', location.id),
                ('usage', '=', 'internal'),
            ])
            location_ids = all_locations.ids or [location.id]

            quants = self.env['stock.quant'].sudo().read_group(
                domain=[
                    ('location_id', 'in', location_ids),
                    ('product_id.is_storable', '=', True),
                ],
                fields=['product_id', 'quantity:sum', 'reserved_quantity:sum'],
                groupby=['product_id'],
            )

            product_ids = [q['product_id'][0] for q in quants]
            products = self.env['product.product'].sudo().browse(product_ids)
            tmpl_map = {p.id: p.product_tmpl_id.id for p in products}

            stock_by_tmpl = {}
            for q in quants:
                prod_id = q['product_id'][0]
                tmpl_id = tmpl_map.get(prod_id)
                if tmpl_id:
                    free = (q['quantity'] or 0.0) - (q['reserved_quantity'] or 0.0)
                    stock_by_tmpl[tmpl_id] = max(0.0, stock_by_tmpl.get(tmpl_id, 0.0) + free)

            # Inject stock into the POS data dictionaries
            for r in res:
                r['qty_available'] = stock_by_tmpl.get(r['id'], 0.0)
        return res

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def get_ul_pos_stock(self, config_id):
        config = self.env['pos.config'].sudo().browse(config_id)
        if not config.exists():
            return {}
            
        warehouse = config.picking_type_id.warehouse_id or config.warehouse_id
        if not warehouse or not warehouse.lot_stock_id:
            return {}
            
        location = warehouse.lot_stock_id
        all_locations = self.env['stock.location'].sudo().search([
            ('id', 'child_of', location.id),
            ('usage', '=', 'internal'),
        ])
        location_ids = all_locations.ids or [location.id]

        quants = self.env['stock.quant'].sudo().read_group(
            domain=[
                ('location_id', 'in', location_ids),
                ('product_id.is_storable', '=', True),
            ],
            fields=['product_id', 'quantity:sum', 'reserved_quantity:sum'],
            groupby=['product_id'],
        )

        product_ids = [q['product_id'][0] for q in quants]
        products = self.env['product.product'].sudo().browse(product_ids)
        tmpl_map = {p.id: p.product_tmpl_id.id for p in products}

        stock_by_tmpl = {}
        for q in quants:
            prod_id = q['product_id'][0]
            tmpl_id = tmpl_map.get(prod_id)
            if tmpl_id:
                free = (q['quantity'] or 0.0) - (q['reserved_quantity'] or 0.0)
                stock_by_tmpl[tmpl_id] = max(0.0, stock_by_tmpl.get(tmpl_id, 0.0) + free)

        return stock_by_tmpl
