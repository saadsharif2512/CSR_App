# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date

class Student(models.Model):
    _name = "student.student"
    _description = "Student"
    _order = "create_date desc"
    _rec_name = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    email = fields.Char()
    phone = fields.Char()
    birth_date = fields.Date()
    is_active = fields.Boolean(default=True, tracking=True)
    status = fields.Selection(
        [('new','New'),('enrolled','Enrolled'),('graduated','Graduated')],
        default='new', tracking=True
    )
    gpa = fields.Float(string="GPA", compute="_compute_gpa", store=True)

    # relations
    enrollment_ids = fields.One2many('enrollment.enrollment', 'student_id', string="Enrollments")
    course_count = fields.Integer(compute="_compute_course_count", string="Courses")

    age = fields.Integer(compute="_compute_age", store=True)

    
    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - ((today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
            else:
                rec.age = 0

    @api.depends('enrollment_ids.grade', 'enrollment_ids.status', 'enrollment_ids.course_id.credit_hours')
    def _compute_gpa(self):
        grade_points = {'a': 4.0, 'b': 3.0, 'c': 2.0, 'd': 1.0, 'f': 0.0}
        for student in self:
            total_credit_hours = 0.0
            total_quality_points = 0.0
            completed_enrollments = student.enrollment_ids.filtered(
                lambda e: e.status == 'completed' and e.grade in grade_points
            )
            if not completed_enrollments:
                student.gpa = 0.0
                continue
            for enrollment in completed_enrollments:
                credit_hours = enrollment.course_id.credit_hours
                quality_points = grade_points.get(enrollment.grade, 0.0)
                total_credit_hours += credit_hours
                total_quality_points += credit_hours * quality_points
            if total_credit_hours > 0:
                student.gpa = total_quality_points / total_credit_hours
            else:
                student.gpa = 0.0

    @api.depends('enrollment_ids.course_id')
    def _compute_course_count(self):
        for rec in self:
            rec.course_count = len(rec.enrollment_ids.mapped('course_id'))

    def action_view_enrollments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Enrollments'),
            'res_model': 'enrollment.enrollment',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

