# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Course(models.Model):
    _name = "course.course"
    _description = "Course"
    _order = "name asc"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    credit_hours = fields.Integer(default=3)
    is_active = fields.Boolean(default=True)
    level = fields.Selection([('ug','Undergrad'),('pg','Postgrad')], default='ug')

    # relations
    enrollment_ids = fields.One2many('enrollment.enrollment', 'course_id', string="Enrollments")
    student_count = fields.Integer(compute="_compute_student_count", string="Students")

    @api.depends('enrollment_ids.student_id')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.enrollment_ids.mapped('student_id'))

    def action_view_students(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Students'),
            'res_model': 'student.student',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.enrollment_ids.mapped('student_id').ids)],
        }
