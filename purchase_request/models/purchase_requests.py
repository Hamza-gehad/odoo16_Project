from odoo import api, fields, models


class PurchaseRequest(models.Model):
    # _inherit = 'purchase.order'
    _name = "purchase.requests"
    _description = "purchase requests"
    _rec_name = 'request_name'

    request_name = fields.Char(string="Request Name", required=True)
    requested_by_id = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user)
    start_date = fields.Datetime(string="Start Date", default=lambda self: fields.Datetime.now())
    end_date = fields.Datetime(string="End Date")
    rejection_reason = fields.Text(string="Rejection Reason", readonly=True)
    status_selection = fields.Selection([('draft', 'Draft'), ('to_be_approved', 'To be approved'), ('reject', 'Reject'),
                                         ('cancel', 'Cancel'), ('approve', 'Approve')], default='draft',
                                        string="Status")
    order_lines_ids = fields.One2many('purchase.request.line', 'request_name_', string="Order Lines")
    total_price = fields.Float(string="Total Price", compute='_compute_total_price', readonly=1)

    def action_submit(self):
        for rec in self:
            rec.status_selection = 'to_be_approved'

    def action_cancel(self):
        for rec in self:
            rec.status_selection = 'cancel'

    # def action_approve(self):
    #
    #     template = self.env.ref('purchase_request.approve_mail_template')
    #     self.status_selection = 'approve'
    #     for rec in self:
    #         id1 = self.env.ref('purchase_request.group_purchase_manager').users.id
    #         id2 = self.env['res.users'].id
    #         print(id1)
    #         template.send_mail(id1)
    #
    #         # for user in self.env.ref('purchase_request.group_purchase_manager').users:
    #         #     template.send_mail(user.id)
    def action_approve(self):
        self.status_selection = 'approve'
        template = self.env.ref('purchase_request.approve_mail_template')
        for user in self.env.ref('purchase_request.group_purchase_manager').users:
            print(user)
            email_values = {'email_to': user.email}
            template.send_mail(user.id, force_send=True,email_values = email_values)


    def action_reset(self):
        for rec in self:
            rec.status_selection = 'draft'

    @api.depends('order_lines_ids')
    def _compute_total_price(self):
        for rec in self:
            if rec.order_lines_ids:
                for rec2 in rec.order_lines_ids:
                    rec.total_price = rec.total_price + rec2.total
            else:
                rec.total_price = 0


class PurchaseRequestLine(models.Model):
    _name = "purchase.request.line"
    _description = "purchase requests line"
    request_name_ = fields.Many2one('purchase.requests', string="request name")
    product_id = fields.Many2one('product.product', string="Product ID", required=True)
    description = fields.Char(string="Description", related="product_id.product_tmpl_id.name")
    quantity = fields.Float(string="Quantity", default=lambda self: 1)
    cost_price = fields.Float(string="Cost Price", related="product_id.standard_price")
    total = fields.Float(string="Total", compute='_compute_total', readonly=1)

    @api.depends('cost_price', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.cost_price
