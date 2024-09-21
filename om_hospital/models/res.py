from odoo import api, fields,models

class resPartner(models.Model):
      _inherit = "res.partner"


      confirm_pay=fields.Integer(string="Hello genius ezra")



