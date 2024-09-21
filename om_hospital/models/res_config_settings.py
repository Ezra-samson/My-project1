from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit='res.config.settings'
    cancel_days=fields.Integer(string="cancel days ", config_parameter='om_hospital.cancel_day')