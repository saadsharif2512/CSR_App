# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Enrollment(models.Model):
    _name = "enrollment.enrollment"
    _description = "Enrollment"
    _order = "create_date desc"

    name = fields.Char(compute="_compute_name", store=True)
    student_id = fields.Many2one('student.student', required=True)
    course_id = fields.Many2one('course.course', required=True)
    date_enrolled = fields.Date(default=fields.Date.context_today)
    
    status = fields.Selection(
        [('draft','Draft'),('confirmed','Confirmed'),('completed','Completed'),('dropped','Dropped')],
        default='draft'
    )
    grade = fields.Selection(
        [('na','N/A'),('a','A'),('b','B'),('c','C'),('d','D'),('f','F')],
        default='na'
    )
    @api.depends('student_id', 'course_id')
    def _compute_name(self):
        for rec in self:
            if rec.student_id and rec.course_id:
                rec.name = f"{rec.student_id.name} - {rec.course_id.code}"
            else:
                rec.name = "New Enrollment"

    @api.constrains('student_id', 'course_id')
    def _check_duplicate(self):
        for rec in self:
            if rec.student_id and rec.course_id:
                existing = self.search_count([
                    ('id', '!=', rec.id),
                    ('student_id', '=', rec.student_id.id),
                    ('course_id', '=', rec.course_id.id),
                    ('status', '!=', 'dropped')
                ])
                if existing:
                    raise ValidationError(_('This student is already enrolled in this course.'))
