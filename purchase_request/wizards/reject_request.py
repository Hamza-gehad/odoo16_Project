from odoo import api, fields, models


class RejectRequestWizard(models.TransientModel):
    _name = "reject.request.wizard"
    _description = "Reject Request Wizard"
    reject_reason = fields.Text(string="Rejection Reason", required=True)
    # purchase_requests_id=fields.Many2one('purchase.requests',string = "purchase requests")




    def action_reject(self):
        purch_req = self.env['purchase.requests'].browse([self.env.context.get('active_id')])
        for rec in self:
            purch_req.rejection_reason = self.reject_reason
            purch_req.status_selection = 'reject'

    def action_close_window(self):
        return {'type': 'ir.actions.act_window_close'}