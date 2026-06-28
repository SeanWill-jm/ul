# -*- coding: utf-8 -*-

from odoo import models, _

class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def action_create_returns(self):
        """ 
        Extend the return creation process to notify the salesperson 
        assigned to the customer when a return picking is created.
        """
        res = super(StockReturnPicking, self).action_create_returns()
        
        # res is typically an action dictionary containing the ID of the newly created picking
        new_picking_id = res.get('res_id')
        if new_picking_id:
            new_picking = self.env['stock.picking'].browse(new_picking_id)
            
            # The salesperson is linked to the customer (partner_id.user_id)
            salesperson = self.picking_id.partner_id.user_id
            
            if salesperson and salesperson.partner_id:
                # Use Odoo's direct chat (Discuss) to notify the salesperson without sending an email
                # This will make a notification appear in the top bar (chat icon)
                channel = self.env['discuss.channel']._get_or_create_chat(
                    partners_to=[salesperson.partner_id.id]
                )
                
                from markupsafe import Markup
                body = Markup(_(
                    "<b>Return Picking Created</b><br/>"
                    "<b>Customer:</b> %s<br/>"
                    "<b>Original Picking:</b> %s<br/>"
                    "<b>Return Picking:</b> %s"
                )) % (
                    self.picking_id.partner_id.name,
                    self.picking_id.name, 
                    new_picking.name
                )
                
                # Post the message to the private chat channel
                channel.message_post(
                    body=body,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment'
                )
                
                # Also log it on the pickings for traceability (without notifying again)
                trace_body = _("Return created: %s. Salesperson notified via direct chat.", new_picking.name)
                self.picking_id.message_post(body=trace_body)
                new_picking.message_post(body=trace_body)
        
        return res
