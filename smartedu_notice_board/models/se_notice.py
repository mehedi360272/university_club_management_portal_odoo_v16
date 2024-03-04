from odoo import models, fields, api, _
import logging


class NoticeBoard(models.Model):
    _name = 'se.notice.board'
    _description = 'For posting announcements, news, events, and other information'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char(strign='Order Reference', required=True, index=True, copy=False, default="NEW")
    name = fields.Char(string='Notice name:')

    club = fields.Many2one('uniclub.core.club', string='Club Name:')
    notice_id = fields.Many2one('se.notice.type', string='Notice Category:')
    notice_type = fields.Char(related='notice_id.name')
    notice_description = fields.Html(string='Notice Descriptions:')
    start_date = fields.Date(string='Start date:', default=fields.Date.today())
    end_date = fields.Date(string='End date:')
    attachments = fields.Many2many('ir.attachment', string='Attachments')
    active = fields.Boolean(string='Active:', default=True)
    note = fields.Text(string='Note:')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Published'),
        ('cancel', 'Cancelled'),
    ], default='draft', string='Status', tracking=True)

    announcement = fields.Html(string='Note:')

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    # Sequence
    @api.model
    def create(self, vals):
        if vals.get('sequence', _('NEW')) == "NEW":
            vals['sequence'] = self.env['ir.sequence'].next_by_code('se.notice.board') or "NEW"
        result = super(NoticeBoard, self).create(vals)
        logging.info(vals['sequence'])
        return result
