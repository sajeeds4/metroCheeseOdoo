from odoo import api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_create_invoice_for_picked_qty(self):
        """Generate an invoice for only the picked quantities, link it to the sales order, and keep it in draft state."""
        sale_order = self.sale_id
        if not sale_order:
            raise UserError("No linked sale order found for this picking.")

        # Prepare invoice line values for picked quantities only
        invoice_line_vals = []
        for move_line in self.move_line_ids:
            if move_line.qty_done > 0:
                sale_line = move_line.move_id.sale_line_id
                if sale_line:
                    invoice_line_vals.append({
                        'product_id': move_line.product_id.id,
                        'quantity': move_line.qty_done,
                        'price_unit': sale_line.price_unit,
                        'sale_line_ids': [(6, 0, [sale_line.id])],  # Link to sale order line
                    })

        # Create the invoice in draft state
        if invoice_line_vals:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.partner_id.id,
                'invoice_origin': sale_order.name,
                'invoice_line_ids': [(0, 0, vals) for vals in invoice_line_vals],
            })

            # Link invoice to the sales order
            # sale_order.write({'invoice_ids': [(4, invoice.id)]})
            sale_order.invoice_ids = [(4, invoice.id)]

            # Generate PDF for download without posting the invoice
            return self.env.ref('account.account_invoices').report_action(invoice)

        raise UserError("No picked quantities found to invoice.")
