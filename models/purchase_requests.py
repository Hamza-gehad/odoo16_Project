from odoo import api, fields, models, exceptions

from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    # _inherit = 'purchase.order'
    _name = "purchase.requests"
    _description = "purchase requests"
    _rec_name = 'request_name'

    request_name = fields.Char(string="Request Name", required=True)
    po_ids = fields.One2many('purchase.order', 'request_name', string='order')

    requested_by_id = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user)
    start_date = fields.Datetime(string="Start Date", default=lambda self: fields.Datetime.now())
    end_date = fields.Datetime(string="End Date")
    rejection_reason = fields.Text(string="Rejection Reason", readonly=True)
    status_selection = fields.Selection([('draft', 'Draft'), ('to_be_approved', 'To be approved'), ('reject', 'Reject'),
                                         ('cancel', 'Cancel'), ('approve', 'Approve')], default='draft',
                                        string="Status")
    order_lines_ids = fields.One2many('purchase.request.line', 'request_name_', string="Order Lines")
    total_price = fields.Float(string="Total Price", compute='_compute_total_price', readonly=1)
    order_count = fields.Integer(compute='compute_orders', string="order count")
    total_qty = fields.Float(compute='compute_total_qty')
    no_po = fields.Boolean(compute='compute_check_qty')
    order_lines_count = fields.Integer(compute='compute_lines_count')

    def action_submit(self):
        for rec in self:
            rec.status_selection = 'to_be_approved'

    def action_cancel(self):
        for rec in self:
            rec.status_selection = 'cancel'

    def action_approve(self):
        if self:
            self.status_selection = 'approve'
            template = self.env.ref('purchase_request.approve_mail_template')
            for rec in self:
                for user in rec.env.ref('purchase_request.group_purchase_manager').users:
                    email_values = {'email_to': user.email}
                    template.send_mail(self.id, force_send=True, email_values=email_values)



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


    @api.depends('po_ids')
    def compute_orders(self):
        for rec in self:
            rec.order_count = len(rec.po_ids)
    @api.depends('order_lines_ids')
    def compute_lines_count(self):
        for rec in self:
            rec.order_lines_count = len(rec.order_lines_ids)


    def action_view_po(self):
        return {
            'name': ("purchase orders"),
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'domain': [('request_name','=',self.request_name)],
            'target': 'current'
        }



    @api.depends('order_lines_ids')
    def compute_total_qty(self):
        total = 0
        for rec in self:
            for line in rec.order_lines_ids:
                total += line.qntty_remain
            rec.total_qty = total
            total = 0


    @api.depends('total_qty')
    def compute_check_qty(self):
        for rec in self:
            if rec.total_qty == 0.0:
                rec.no_po = False
            else:
                rec.no_po = True


class PurchaseRequestLine(models.Model):
    _name = "purchase.request.line"
    _description = "purchase requests line"
    request_name_ = fields.Many2one('purchase.requests', string="request name")
    po = fields.Many2one('purchase.order.wizard', string='order')
    product_id = fields.Many2one('product.product', string="Product ID", required=True)
    description = fields.Char(string="Description", related="product_id.product_tmpl_id.name")
    quantity = fields.Float(string="Quantity", default=lambda self: 1)
    cost_price = fields.Float(string="Cost Price", related="product_id.standard_price")
    total = fields.Float(string="Total", compute='_compute_total', readonly=1)
    qntty_remain = fields.Float(string="max")



    @api.onchange('quantity')
    def remain_default(self):
        for rec in self:
            rec.qntty_remain = rec.quantity

    @api.depends('cost_price', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.cost_price
