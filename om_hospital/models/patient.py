from datetime import date
from lxml import etree
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class Hospitalpatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital patient"
    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date(string="Date of Birth")
    ref = fields.Char(string="Reference", tracking=True)
    age = fields.Integer(string="age", compute='_compute_age',inverse="_inverse_compute_age",search="_search_age", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='gender', tracking=True,default="female")
    active = fields.Boolean(string="Active", default="True")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    image=fields.Image(string="Image")
    tag_ids=fields.Many2many('patient.tag');
    appointment_count=fields.Integer(string="Appointment count" ,store=True)
    appointment_ids=fields.One2many('hospital.appointment','patient_id', string="Appointment")
    parent=fields.Char(string="Parent")
    marital_status=fields.Selection([('married', 'Married'), ('single', 'Single')], string='marital_status',tracking=True)
    partner_name=fields.Char(string="PartnerName")
    is_birthday=fields.Boolean(string="birth  day ?", compute='_compute_is_birthday')
    phone=fields.Char(string="Phone")
    email = fields.Char(string="E-mail")
    web = fields.Char(string="website")






    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("the enter date is not accebtale"))
    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("you can not delete patient with appointment"))




    @api.model
    def create(self,vals):
        vals['ref']=  self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(Hospitalpatient, self).create(vals)

    def write(self,vals):
        print("hello odoo mates ",vals)
        return super(Hospitalpatient,self).write(vals)

    def action_done(self):
        return

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age=today.year-rec.date_of_birth.year
            else:
                rec.age=0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth=today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year=date_of_birth.replace(day=1,month=1)
        end_of_year=date_of_birth.replace(day=31,month=12)
        return [('date_of_birth', '>=', start_of_year),('date_of_birth', '<=', end_of_year)]

    def name_get(self):
        patient_list=[]
        for record in self:
              name=str(record.ref) + str(record.name)
              patient_list.append((record.id,name))
        return patient_list

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        is_birthday=False
        for rec in self:
            if rec.date_of_birth:
                today=date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday=True
            rec.is_birthday= is_birthday







