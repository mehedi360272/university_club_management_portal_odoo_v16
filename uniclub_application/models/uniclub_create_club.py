from odoo import api, models, fields, _
import logging
from odoo.exceptions import ValidationError, UserError


class UniclubClub(models.Model):
    _name = 'uniclub.create.club'
    _description = 'Clubs'

    name = fields.Char(string='Name', required=True)
    club_type_ids = fields.Many2one('uniclub.club.type', string='Club Type', required=True)
    image = fields.Image(string='Image', required=True)
    bank_account = fields.Char(string='Bank Account Number')
    purpose_and_goal = fields.Html(string='Club Purpose And Goal')
    rules = fields.Html(string='Policies And Guidelines')


