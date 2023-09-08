from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    dimensions = fields.Char(string="dimensions", compute='find_dim')

    @api.depends('sale_line_ids')
    def find_dim(self):
        self.dimensions = "0*0"
        for rec in self.env['stock.move'].search([]):
            # print(self.sale_line_ids.id,rec.sale_order_line.id)

            if self.sale_line_ids.id==rec.sale_order_line.id:

                self.dimensions = rec.dimensions

