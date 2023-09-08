from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    sale_order_line = fields.Many2one('sale.order.line', compute='find_order')
    dimensions = fields.Char(string="dimensions", compute='find_order', inverse='inverse_find_dim')
    lol = fields.Char(string="lol", default="lol")

    def inverse_find_dim(self):
        return

    @api.depends('origin')
    def find_order(self):
        for rec2 in self:
            for rec in rec2.env['sale.order'].search([]):


                if rec.name == rec2.origin:

                    for line in rec.order_line:

                        if line.product_id == rec2.product_id:
                            rec2.sale_order_line = line
                            print(rec2.sale_order_line)
                            rec2.dimensions = line.dimensions

            if not rec2.sale_order_line:
                rec2.sale_order_line = False
                rec2.dimensions = "0*0"

