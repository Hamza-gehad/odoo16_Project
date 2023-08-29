from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrderWizard(models.Model):
    _name = "purchase.order.wizard"
    _description = "purchase order creation Wizard"

    purchase_order_id = fields.Many2one('res.partner', string="vendor")
    po_order_lines_ids = fields.One2many('purchase.request.line', 'po', string="Order Lines")

    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrderWizard, self).default_get(fields)
        res.update({
            'po_order_lines_ids': self.env['purchase.requests'].browse(
                [self.env.context.get('active_id')]).order_lines_ids

        })
        return res

    @api.onchange('po_order_lines_ids')
    def remains_def(self):
        for rec in self:
            for line in rec.po_order_lines_ids:
                if line.qntty_remain < line.quantity:
                    line.quantity=line.qntty_remain

    def create_po(self):
        order_lines = []
        for rec in self:

            for line in rec.po_order_lines_ids:
                if line.qntty_remain !=0:
                    order_lines.append([0, 0, {
                        'name': line.description,
                        'product_id': line.product_id.id,
                        'product_qty': line.qntty_remain,
                        'price_unit': line.cost_price,
                        'date_planned': fields.Datetime.now(),
                    }])
            po = self.env['purchase.order'].create({
                'partner_id': self.purchase_order_id.id,
                'request_name': line.request_name_.id,
                'order_line': order_lines
            })
