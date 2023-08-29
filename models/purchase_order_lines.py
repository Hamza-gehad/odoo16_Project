from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']
    request_name = fields.Many2one('purchase.requests',string = "request name")

    @api.constrains('order_line','request_name.order_lines_ids','state')
    def constraint_qty(self):
        if(self.state == 'purchase'):
            for line1,line2 in  zip(self.order_line , self.request_name.order_lines_ids):
                if line1.product_qty > line2.qntty_remain:
                    raise ValidationError(("product quantity limit exceeded"))
                else:
                    value = (line2.qntty_remain - line1.product_qty)

                    line2.qntty_remain = value




    def count_orders(self):
        total = 0
        for rec in self:
            if rec.state =='purchase':
                total += 1

        return total

