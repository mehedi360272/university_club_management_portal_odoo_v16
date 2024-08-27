# -*- coding: utf-8 -*-
import base64
import logging
from odoo import http
from odoo.http import request


class ApplicationSession(http.Controller):
    @http.route(['/recruitment_session', '/recruitment_session/page/<int:page>'], type='http', auth='public', website=True)
    def application_session(self, page=0, **kw):
        my_data = request.env['uniclub.application.session'].sudo().search([('state', '=', 'publish')])
        total = my_data.sudo().search_count([('state', '=', 'publish')])
        pager = request.website.pager(
            url='/recruitment_session',
            total=total,
            page=page,
            step=6,
        )
        offset = pager['offset']
        my_data = my_data[offset: offset + 6]
        return request.render('uniclub_application.recruitment_session_list', {
            'my_data': my_data,
            'pager': pager,
        })


class ApplicationForm(http.Controller):
    @http.route('/application_form', auth="public", website=True)
    def application_form(self, **kw):
        first_name = kw.get('first_name')
        middle_name = kw.get('middle_name')
        last_name = kw.get('last_name')
        phone = kw.get('phone')
        email = kw.get('email')
        date_of_birth = kw.get('date_of_birth')
        blood_group = kw.get('blood_group')
        session = request.env['uniclub.application.session'].sudo().search([])
        gender = kw.get('gender')
        student_id = kw.get('student_id')
        department = kw.get('department')
        year_of_study = kw.get('year_of_study')
        expected_graduation_date = kw.get('expected_graduation_date')
        previous_experience = kw.get('previous_experience')
        why_join_this_club = kw.get('why_join_this_club')

        return http.request.render('uniclub_application.application_form', {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'date_of_birth': date_of_birth,
            'blood_group': blood_group,
            'session': session,
            'gender': gender,
            'student_id': student_id,
            'department': department,
            'year_of_study': year_of_study,
            'expected_graduation_date': expected_graduation_date,
            'previous_experience': previous_experience,
            'why_join_this_club': why_join_this_club,
        })

    @http.route('/application_form/submit', auth='public', website=True)
    def info_redirect(self, **kw):
        first_name = kw.get('first_name')
        middle_name = kw.get('middle_name')
        last_name = kw.get('last_name')
        phone = kw.get('phone')
        email = kw.get('email')
        date_of_birth = kw.get('date_of_birth')
        blood_group = kw.get('blood_group')
        session = kw.get('session')
        gender = kw.get('gender')
        student_id = kw.get('student_id')
        department = kw.get('department')
        year_of_study = kw.get('year_of_study')
        expected_graduation_date = kw.get('expected_graduation_date')
        previous_experience = kw.get('previous_experience')
        why_join_this_club = kw.get('why_join_this_club')

        request.env['uniclub.application'].sudo().create({
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'date_of_birth': date_of_birth,
            'blood_group': blood_group,
            'session': session,
            'gender': gender,
            'student_id': student_id,
            'department': department,
            'year_of_study': year_of_study,
            'expected_graduation_date': expected_graduation_date,
            'previous_experience': previous_experience,
            'why_join_this_club': why_join_this_club,
        })
        return request.render('uniclub_application.submit_confirm')
