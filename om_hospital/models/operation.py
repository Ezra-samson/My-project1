from odoo import api, fields,models

class odooPlayGround(models.Model):
    _name="hospital.operation"
    _description="Hospital Operation"
    _log_access =False

    doctor_id=fields.Many2one('res.users', string="Doctors")
    operation_name=fields.Char(string="Name")
    reference_record=fields.Reference(selection=[('hospital.patient','patient'),('hospital.appointment','Appointment')],string="Record")

    @api.model
    def name_create(self,name):
        return self.create({'operation_name':name}).name_get()[0]


