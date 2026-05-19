from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.exceptions import AccessError, MissingError


class SaleOrderPortal(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(
        self,
        order_id,
        report_type=None,
        access_token=None,
        message=False,
        download=False,
        payment_amount=None,
        amount_selection=None,
        **kw
    ):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        # Override report_type to use custom proforma invoice
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=order_sudo,
                report_type=report_type,
                report_ref='ul_reports.action_report_ul_proforma_invoice',
                download=download,
            )

        # Call parent method for normal portal view
        return super().portal_order_page(
            order_id=order_id,
            report_type=report_type,
            access_token=access_token,
            message=message,
            download=download,
            payment_amount=payment_amount,
            amount_selection=amount_selection,
            **kw
        )
