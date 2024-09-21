from odoo import api, fields, models,_

class patientTag(models.Model):
    _name="patient.tag"
    _description="patient tag"

    name=fields.Char(string="Name", require='true', copy=False)
    active=fields.Boolean(string="Active", default=True)
    color=fields.Integer(string="Color")
    sequence=fields.Integer(string="Sequence")

    @api.returns('self',lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default={}
        if not default.get('name'):
            default['name']=_("%s (copy)", self.name)
        default['sequence']=10
        return super(patientTag,self).copy(default)


    _sql_constraints = [
        ('unique_tag_name', 'unique (name,active)', 'Name must be unique'),
        ('check_sequence','check(sequence > 0)','sequance must be non zero positive number.')]



