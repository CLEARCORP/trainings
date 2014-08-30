# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import osv, fields

class Wizard (osv.TransientModel):
    _name = 'jornamon.course.session.wizard'
    
    _columns = {
        'student_ids': fields.one2many('jornamon.course.session.wizard.students', 'wizard_id', string="Students"),
        'session_ids': fields.one2many('jornamon.course.session.wizard.sessions', 'wizard_id', string="Sessions") ,        
        }
    
    def add_students (self, cr, uid, ids, context={}):
        session_obj = self.pool.get('jornamon.course.session')
        wizard = self.browse(cr, uid, ids, context=context)[0]
        student_ids = []
        for student in wizard.student_ids:
            student_ids.append((4, student.student_id.id))
        session_ids = []
        for session in wizard.session_ids:
            session_ids.append(session.session_id.id)
        session_obj.write(cr, uid, session_ids, {'student_ids': student_ids})
        return True


class WizardStudents (osv.TransientModel):
    _name = 'jornamon.course.session.wizard.students'
    
    _columns = {
        'wizard_id': fields.many2one('jornamon.course.session.wizard', string="Wizard"),  
        'student_id': fields.many2one('res.partner', string="Student")  ,       
        }
    
class WizardSessions (osv.TransientModel):
    _name = 'jornamon.course.session.wizard.sessions'
    
    _columns = {
        'wizard_id': fields.many2one('jornamon.course.session.wizard', string="Wizard"),  
        'session_id': fields.many2one('jornamon.course.session', string="Student"),       
        }