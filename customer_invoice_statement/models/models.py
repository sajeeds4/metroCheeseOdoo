# models/customer_statement.py
from odoo import models, fields, api


class CustomerStatement(models.AbstractModel):
    _name = 'report.customer_statement_report.statement_pdf'
    _description = 'Customer Statement Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        customer = self.env['res.partner'].browse(docids)
        invoices = self.env['account.move'].search([
            ('partner_id', '=', customer.id),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', 'in', ['posted', 'open'])
        ])

        total_outstanding = sum(inv.amount_residual for inv in invoices)

        return {
            'doc_model': 'res.partner',
            'doc_ids': docids,
            'docs': customer,
            'invoices': invoices,
            'total_outstanding': total_outstanding,
        }
