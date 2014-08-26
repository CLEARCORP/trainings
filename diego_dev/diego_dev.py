# -*- coding: utf-8 -*

from openerp.osv import osv, fields 

class Course (osv.Model):
    _name = 'diego_dev.course'
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'description': fields.text('Description'),   
        'session_ids': fields.one2many('diego_dev.course.session','course_id', string='Session'),   
        'student_ids': fields.many2many('diego_dev.student', string='Students'), 
        'teacher_id' : fields.many2one('res.users', string='Teacher', ondelete='set null', select=True)       
                }
    
class Student (osv.Model):
    _name = 'diego_dev.student'
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'birthday': fields.date ('Birthday'), 
        'course_ids': fields.many2many('diego_dev.course', string='Courses')               
                }
    
class CourseSession(osv.Model):
    _name = 'diego_dev.course.session'
    _columns = {
        'subject': fields.char('Subject', size=128, required=True, select=True),
        'start_time': fields.datetime('Start Time', required=True),
        'end_time': fields.datetime('End Time'),
        'course_id':fields.many2one('diego_dev.course', string='Course', required=True, select=True, ondelete='cascade'),
                }
    _rec_name = 'subject'
    _order = 'start_time'