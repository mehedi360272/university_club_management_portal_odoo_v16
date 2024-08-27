from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError


class UniclubApplicationSession(models.Model):
    _name = 'uniclub.application.session'
    _description = 'Uniclub Application Session'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The name must be unique!'),
    ]

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if record.name and self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("Name must be unique!")

    photo = fields.Image(string="Photo")
    club_ids = fields.Many2one('uniclub.create.club', string="Club Name")
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    year = fields.Selection(
        [(str(year), str(year)) for year in range(2000, 2051)],
        string='Year Selection',
        required=True,
    )

    member_type = fields.Many2one('hr.job', string='Member Type')
    minimum_member = fields.Integer(string="Minimum No. Of Members")
    maximum_member = fields.Integer(string="Maximum No. Of Members")
    registration_fee = fields.Integer(string="Registration Fee")
    note = fields.Html(string="Note")
    details = fields.Html(string="Details")

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

    def create_application(self):
        self.ensure_one()
        view_id = self.env.ref(
            'uniclub_application.uniclub_application_view_form', False)
        return {
            'name': _('New Application'),
            'view_mode': 'form',
            'res_model': 'uniclub.application',
            'view_id': view_id and view_id.id or False,
            'type': 'ir.actions.act_window',
            'context': {
                'default_type_id': self.id,
            }
        }

    def open_submitted_application(self):
        self.ensure_one()
        view_id = self.env.ref(
            'uniclub_application.uniclub_application_view_form', False)
        return {
            'name': _('Submitted Application'),
            'view_mode': 'tree,form',
            'res_model': 'uniclub.application',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('session', '=', self.id)],
            'context': {
                'default_type_id': self.id,
            }
        }

    def open_new_submitted_application(self):
        self.ensure_one()
        view_id = self.env.ref(
            'uniclub_application.uniclub_application_view_form', False)
        return {
            'name': _('Submitted Application'),
            'view_mode': 'tree,form',
            'res_model': 'uniclub.application',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('session', '=', self.id), ('state', '=', 'draft')],
            'context': {
                'default_type_id': self.id,
            }
        }

    total_new = fields.Integer(compute="_new_submitted_request")

    total_application = fields.Integer(compute="_total_submitted_request")

    def _new_submitted_request(self):
        for r in self:
            r.total_new = self.env['uniclub.application'].search_count(
                [('session', '=', r.id), ('state', '=', 'draft')])

    def _total_submitted_request(self):
        for r in self:
            r.total_application = self.env['uniclub.application'].search_count(
                [('session', '=', r.id)])






