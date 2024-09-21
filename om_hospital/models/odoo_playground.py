from odoo.tools.safe_eval import safe_eval
from odoo import api, fields,models

class odooPlayGround(models.Model):
    _name="odoo.playground"
    _description="odoo playground"
    DEFAULT_ENV_VARIABLES="""ezra begins coding at age of 19 and he is good coder and jesus love him and die for him"""

    model_id=fields.Many2one('ir.model',string='Model')
    code=fields.Text(string="code")
    result = fields.Text(string="Result")

    def action_execute(self):
        try:
            if self.model_id:
                model=self.env[self.model_id.model]
            else:
                model=self
            self.result=safe_eval(self.code.strip(),{'self': model})
        except Exception as e:
            self.result=str(e)