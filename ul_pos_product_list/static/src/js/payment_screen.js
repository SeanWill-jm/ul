/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { onMounted } from "@odoo/owl";

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
        onMounted(() => {
            console.log("[ul_pos_product_list] ProductScreen mounted! Triggering live stock sync...");
            try {
                if (typeof this.pos._fetchProductStock === 'function') {
                    this.pos._fetchProductStock(); 
                }
                if (typeof this.pos._syncStock === 'function') {
                    this.pos._syncStock(); 
                }
            } catch (e) {
                console.warn("[ul_pos_product_list] Failed to trigger live stock sync:", e);
            }
        });
    }
});
