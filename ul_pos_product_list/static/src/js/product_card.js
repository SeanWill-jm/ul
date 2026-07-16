/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useState, useEffect } from "@odoo/owl";

patch(ProductCard.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
        this.ulStockState = useState({ qty: 0 });

        useEffect(
            () => {
                const product = this.props.product;
                if (!product) return;
                
                // Get the template ID from the product
                const tmplId = Array.isArray(product.product_tmpl_id)
                    ? product.product_tmpl_id[0]
                    : (product.product_tmpl_id || product.id);
                    
                // Read from our native sync engine
                const stockData = this.pos.ulStockMap?.[tmplId];
                
                // Fallbacks: live map -> python injected -> 0
                let qty = 0;
                if (stockData !== undefined) {
                    qty = stockData;
                } else if (product.qty_available !== undefined) {
                    qty = product.qty_available;
                }
                
                this.ulStockState.qty = typeof qty === 'number' ? qty : 0;
            },
            () => [this.pos.ulStockVersion?.v, this.pos.ulStockMap]
        );
    },

    get ulStockQtyDisplay() {
        const qty = this.ulStockState.qty;
        return Number.isInteger(qty) ? String(qty) : qty.toFixed(1);
    },

    get ulStockBadgeStyle() {
        const qty = this.ulStockState.qty;
        if (qty <= 0) {
            return { bg: "#DC3545", fg: "#FFFFFF" }; // Red out of stock
        } else if (qty <= 5) {
            return { bg: "#FD7E14", fg: "#FFFFFF" }; // Orange low stock
        } else {
            return { bg: "#28A745", fg: "#FFFFFF" }; // Green normal
        }
    }
});
