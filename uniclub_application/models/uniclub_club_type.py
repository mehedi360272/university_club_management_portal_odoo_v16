from odoo import api, models, fields, _
import logging
from odoo.exceptions import ValidationError, UserError


class UniclubClub(models.Model):
    _name = 'uniclub.club.type'
    _description = 'Club Type'

    name = fields.Char(string='Name', required=True)
