/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { KanbanRecord } from "@web/views/kanban/kanban_record";
import { onMounted } from "@odoo/owl";

patch(KanbanRecord.prototype, {
    setup() {
        super.setup();
        onMounted(() => {
            const container = this.rootRef.el.querySelector('.ul_clickable_image');
            if (container) {
                const img = container.querySelector('img');
                if (img) {
                    container.onclick = (ev) => {
                        ev.preventDefault();
                        ev.stopPropagation();
                        // Get the higher resolution image if available
                        const src = img.src.replace('image_128', 'image_1920');
                        this.showFullImage(src);
                    };
                }
            }
        });
    },

    showFullImage(src) {
        let modal = document.querySelector('.ul_image_modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.className = 'ul_image_modal';
            modal.innerHTML = `
                <span class="ul_image_modal_close">&times;</span>
                <img class="ul_image_modal_content">
            `;
            document.body.appendChild(modal);
            modal.querySelector('.ul_image_modal_close').onclick = (ev) => {
                ev.stopPropagation();
                modal.style.display = "none";
            };
            modal.onclick = (ev) => {
                modal.style.display = "none";
            };
        }
        modal.querySelector('.ul_image_modal_content').src = src;
        modal.style.display = "block";
    }
});
