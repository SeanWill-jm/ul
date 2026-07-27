/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { reactive } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { onMounted } from "@odoo/owl";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
        this.ulStockMap = reactive({});
        this.ulStockVersion = reactive({ v: 0 });
        
        // Initial sync
        await this._syncUlStock();
        
        // Background polling every 30 seconds
        setInterval(() => this._syncUlStock(), 30000);
    },

    async _syncUlStock() {
        try {
            const session = [...this.models['pos.session'].records.values()][0];
            if (!session || !this.config) return;

            const result = await this.env.services.orm.call(
                'pos.session',
                'get_ul_pos_stock',
                [this.config.id]
            );

            // result is a dict of {product_tmpl_id: free_qty}
            if (result) {
                // Update existing keys
                for (const key of Object.keys(this.ulStockMap)) {
                    if (!(key in result)) {
                        delete this.ulStockMap[key];
                    }
                }
                // Assign new keys
                Object.assign(this.ulStockMap, result);
                this.ulStockVersion.v += 1;
            }
        } catch (e) {
            console.warn("[ul_pos_product_list] Background stock sync failed:", e.message);
        }
    }
});

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
        onMounted(() => {
            // When returning to the main screen after payment, force a sync
            if (this.pos && typeof this.pos._syncUlStock === 'function') {
                this.pos._syncUlStock();
            }
        });
    }
});
