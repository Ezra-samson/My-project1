import datetime
from odoo import api, fields,models, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta

class CancelAppointmentwizard(models.TransientModel):
    _name="cancel.appointment.wizard"
    _description="cancel Appointment wizard"

    @api.model
    def default_get(self, fields):
        res=super(CancelAppointmentwizard, self).default_get(fields)
        res['date_cancel']=datetime.date.today()
        res['appointment_id']=self.env.context.get('active_id')
        return res

    appointment_id=fields.Many2one('hospital.appointment',string="Appointment", domain=[('state', '=' ,'draft'),('priority', 'in', ('0','1',False))])
    reason=fields.Text(string=" Reason")
    date_cancel=fields.Date(string="Cancellation Date")
    def action_cancel(self):
        cancel_day=self.env['ir.config_parameter'].get_param('om_hospital.cancel_day')
        allow_date=self.appointment_id.booking_date + relativedelta.relativedelta(days=int(cancel_day))
        if allow_date > date.today():
            raise ValidationError(_("sorry you can not delete current day appointment  "))
        self.appointment_id.state='cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }




