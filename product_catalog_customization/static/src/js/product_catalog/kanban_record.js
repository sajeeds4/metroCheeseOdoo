/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { _t } from "@web/core/l10n/translation";

function sendCustomNotification(type, message) {
    return {
        type: "ir.actions.client",
        tag: "display_notification",
        params: {
            "type": type,
            "message": message
        },
    }
}

patch(ProductCatalogKanbanRecord.prototype, {
    updateQuantity(quantity) {
        if (quantity>this.props.record.data.available_qty && this.env.orderResModel === 'sale.order'){
                this.action.doAction(
                sendCustomNotification("warning", _t("You can't add Qty more than available Qty"))
                   );
                  return ;
        }
        if (this.productCatalogData.readOnly) {
            return;
        }
        this.productCatalogData.quantity = quantity || 0;
        this.debouncedUpdateQuantity();
    }

});