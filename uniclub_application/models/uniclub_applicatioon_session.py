from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError


class UniclubApplicationSession(models.Model):
    _name = 'uniclub.application.session'
    _description = 'Uniclub Application Session'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    photo = fields.Image(string="Photo")
    club_ids = fields.Many2one('uniclub.core.club', string="Club Name")
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    year = fields.Selection(
        [(str(year), str(year)) for year in range(2000, 2051)],
        string='Year Selection',
        required=True,
    )

    member_type = fields.Many2one('hr.job', string='Member Type')
    minimum_member = fields.Integer(string="Minimum No. Of Members")
    maximum_member = fields.Integer(string="Maximum No. Of Members")
    registration_fee = fields.Integer(string="Registration Fee")

    application_ids = fields.Many2many('uniclub.application', inverse_name='session_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('publish', 'Published'),
        ('unpublish', 'Un-published'),
        ('cancel', 'Cancelled'),
    ], default='draft', string='Status')

    def action_publish(self):
        self.state = 'publish'

    def action_unpublish(self):
        self.state = 'unpublish'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'


    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for record in self:
            start_date = fields.Date.from_string(record.start_date)
            end_date = fields.Date.from_string(record.end_date)
            if start_date > end_date:
                raise ValidationError("End Date cannot be set before Start Date.")

    @api.constrains('minimum_member', 'maximum_member')
    def check_no_of_application(self):
        for record in self:
            if (record.minimum_member < 0) or (record.maximum_member < 0):
                raise ValidationError("No of Admission should be positive!")
            if record.minimum_member > record.maximum_member:
                raise ValidationError("Min Application can't be greater than Max Application")

