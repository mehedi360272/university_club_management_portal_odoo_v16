from odoo import models, fields


class DepartmentType(models.Model):
    _name = 'se.notice.type'
    _description = ''

    name = fields.Char(string='Notice Category:')
