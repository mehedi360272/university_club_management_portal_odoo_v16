from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError


class ApplicationMemberType(models.Model):
    _name = 'uniclub.application.member.type'
    _description = 'Member Type'

    name = fields.Many2one('hr.job', string='Name')
