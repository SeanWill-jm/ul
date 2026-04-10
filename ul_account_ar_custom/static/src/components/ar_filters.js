import { AgedPartnerBalanceFilters } from "@account_reports/components/aged_partner_balance/filters";
import { AccountReport } from "@account_reports/components/account_report/account_report";

export class UlArFilters extends AgedPartnerBalanceFilters {
    static template = "ul_account_ar_custom.ArFilters";

    getMultiRecordSelectorProps(resModel, optionKey) {
        return {
            resModel,
            resIds: this.controller.cachedFilterOptions[optionKey] || [],
            update: (resIds) => {
                this.filterClicked({ optionKey, optionValue: resIds, reload: true });
            },
        };
    }
}

AccountReport.registerCustomComponent(UlArFilters);
