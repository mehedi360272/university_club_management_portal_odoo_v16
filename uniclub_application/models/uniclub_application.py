from odoo import api, models, fields, _
import logging
from odoo.exceptions import ValidationError, UserError

GENDER = [
    ('0', 'Male'),
    ('1', 'Female'),
    ('2', 'Other')
]


class UniclubApplication(models.Model):
    _name = 'uniclub.application'
    _description = 'Uniclub Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char(required=True, index=True, copy=False, default="NEW")

    session = fields.Many2one('uniclub.application.session')
    name = fields.Char(string='Name', compute='_compute_name_concat', store=True)
    application_date = fields.Date(default=fields.Date.today())
    # application_date = fields.Date(string='Date')

    session_id = fields.Many2many('uniclub.application.session', 'application_ids')
    # Personal Information
    first_name = fields.Char(string='First Name', required=True)
    middle_name = fields.Char(string='Middle Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    photo = fields.Image(string="Photo")
    date_of_birth = fields.Date(string="Date Of Birth")

    gender = fields.Selection(GENDER)

    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    blood_group = fields.Selection([
        ('0', 'A+'),
        ('1', 'A-'),
        ('2', 'B+'),
        ('3', 'B-'),
        ('4', 'AB+'),
        ('5', 'AB-'),
        ('6', 'O+'),
        ('7', 'O-'),
    ], string="Blood Group", store="True")
    # Academic Information
    student_id = fields.Char(string="Student ID")
    department = fields.Char(string="Department or Program")
    year_of_study = fields.Date(string="Year Of Study")
    note = fields.Text()
    expected_graduation_date = fields.Date(string="Expected Graduation Date")
    # Questions
    why_join_this_club = fields.Text(string="What do you want to join this club?")
    previous_experience = fields.Selection([
        ('0', 'Yes'),
        ('1', 'No'),
    ])

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name_concat(self):
        for partner in self:
            if not partner.middle_name:
                partner.name = str(partner.first_name) + " " + str(
                    partner.last_name
                )
            else:
                partner.name = str(partner.first_name) + " " + str(
                    partner.middle_name) + " " + str(partner.last_name)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('app_confirm', 'Application Confirmed'),
        ('reg_confirm', 'Registration Confirmed'),
        ('reject', 'Rejected'),
    ], default='draft', string='Status', tracking=True)

    def action_app_confirm(self):
        self.state = 'app_confirm'

    def action_reg_confirm(self):
        self.state = 'reg_confirm'
        name = self.name
        email = self.email
        # current_user = self.env.user
        user_data = {
            'name': name,
            'login': email,
            'email': email,
            'password': "password123",
        }
        new_user = self.env['res.users'].create(user_data)

        user_image = self.photo
        try:
            new_user.write({'image_1920': user_image})
        except ValidationError:
            pass
        new_user.action_reset_password()

        self.env.cr.commit()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_draft(self):
        self.state = 'draft'

    def action_reject(self):
        self.state = 'reject'

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('NEW')) == "NEW":
            vals['sequence'] = self.env['ir.sequence'].next_by_code('uniclub.application') or "NEW"
        result = super(UniclubApplication, self).create(vals)
        logging.info(vals['sequence'])
        return result

