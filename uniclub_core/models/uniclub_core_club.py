from odoo import api, models, fields, _
import logging
from odoo.exceptions import ValidationError, UserError


class UniclubClub(models.Model):
    _name = 'uniclub.core.club'
    _description = 'Clubs'

    name = fields.Char(string='Name', required=True)
    club_type_ids = fields.Many2one('uniclub.core.club.type', string='Club Type', required=True)
    image = fields.Image(string='Image', required=True)
    bank_account = fields.Char(string='Bank Account Number')
    purpose_and_goal = fields.Html(string='Club Purpose And Goal')
    rules = fields.Html(string='Policies And Guidelines')

    count = fields.Integer(string='Total Record Count', compute='_compute_record_count')

    @api.model
    def _compute_record_count(self):
        self.count = self.env['uniclub.core.club'].search_count([])
