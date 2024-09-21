import random
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital appointement"
    _rec_name = 'patient_id'
    _order='id desc'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', related="patient_id.gender")
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string="Reference")
    prescription = fields.Html(string="prescription")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'draft'),
        ('in_consultation', 'In consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft',string="states",required=True)
    doctor_id=fields.Many2one('res.users', string="Doctor")
    pharmacy_line_ids=fields.One2many('appointment.pharmacy.lines','appointment_id',string='Pharmacy Lines')
    hide_sales_price=fields.Boolean(string="hide sales price")
    operation_id=fields.Many2one('hospital.operation', string="0peration")
    progress=fields.Integer(string="progress",compute="_compute_progress")
    duration=fields.Float(string="Duration")

    company_id=fields.Many2one('res.company',string='Company', default=lambda self: self.env.company)
    currency_id=fields.Many2one('res.currency', related='company_id.currency_id')
    total = fields.Monetary(string="total", compute="_total_amount")



    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    @api.model
    def create(self, vals):
        print("hello world.......", vals)
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalAppointment, self).create(vals)

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("you can delete appointment only in draft state "))
        return super(HospitalAppointment, self).unlink()
    def action_test(self):
            return{
                'type':'ir.actions.act_url',
                'target':'self',
                'url':'https://www.odoo.com'
            }
    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state="in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        action=  self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress=random.randrange(0,25)
            elif rec.state == 'in_consultation':
                progress=random.randrange(25,75)
            elif rec.state == 'done':
                progress=100
            else:
                progress=0
            rec.progress=progress
    @api.depends('pharmacy_line_ids.price_subtotal')
    def _total_amount(self):
            for rec in self:
                print(rec)
                for rat in rec.pharmacy_line_ids:
                    print(rat)
                    rec.total= rec.total + rat.price_subtotal





class Appointmentpharmacylines(models.Model):
    _name="appointment.pharmacy.lines"
    _description = "Appointment pharmacy lines"
    
    product_id=fields.Many2one('product.product',required=True)
    price_unit=fields.Float(related='product_id.list_price')
    qty=fields.Integer(string="Quantity", default=1)
    appointment_id=fields.Many2one('hospital.appointment',string="Appointment")
    currency_id=fields.Many2one('res.currency', related="appointment_id.currency_id")
    price_subtotal=fields.Monetary(string="subtotal", compute="_calculate_total" ,store=True)


    @api.depends('price_unit','qty')
    def _calculate_total(self):
       for rec in self:
                rec.price_subtotal=rec.price_unit * rec.qty











