from odoo import http
from odoo.http import request, Response
import datetime
from datetime import datetime
import pytz
import requests
from odoo.exceptions import ValidationError
import json
import io, base64
import calendar
import werkzeug.urls
import werkzeug.utils
from werkzeug.utils import redirect
import json


# show notice in website
class MyController(http.Controller):
    @http.route(['/notice', '/notice/page/<int:page>'], type='http', auth='public', website=True)
    def my_controller(self, page=0, **kw):
        my_data = request.env['se.notice.board'].sudo().search([('state', '=', 'done')])
        total = my_data.sudo().search_count([])
        pager = request.website.pager(
            url='/notice',
            total=total,
            page=page,
            step=5,
        )
        offset = pager['offset']
        my_data = my_data[offset: offset + 5]
        return request.render('smartedu_notice_board.notice_page', {
            'my_data': my_data,
            'pager': pager,
        })

    @http.route(['/view/<int:record_id>'], type='http', auth="public", website=True)
    def view_list(self, record_id=None,):
        values = {}
        notice_view = http.request.env['se.notice.board'].sudo().search([('id', '=', record_id)])
        if notice_view:
            notice_attachments_list = []
            for notice in notice_view.attachments:
                notice_attachments = http.request.env['ir.attachment'].sudo().search([('id', '=', notice.id)])
                notice_attachments_list.append(notice_attachments)
            values.update({
                'notice_attachments': notice_attachments_list,
                'notice_attachments_count': len(notice_attachments_list),
            })

        values.update({
            'notice_view': notice_view,
        })

        return http.request.render("smartedu_notice_board.view_page", values)

    @http.route(['/free/download/<int:attachment_id>', ], type='http', auth='public')
    def download_attachment_free(self, attachment_id):
        # Restrict User Login to Download
        if not request.session.uid:
            return werkzeug.utils.redirect('/web/login')

        # Check if this is a valid attachment id
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "mimetype", "res_model", "res_id", "type", "url"]
        )

        if attachment:
            attachment = attachment[0]
        else:
            return redirect(self.orders_page)

        # The client has bought the product, otherwise it would have been blocked by now
        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
            filename = attachment['name']
            return http.send_file(data, filename=filename, as_attachment=True)
        else:
            return request.not_found()
