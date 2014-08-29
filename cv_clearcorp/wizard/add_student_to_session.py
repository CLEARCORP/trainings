# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import osv, fields

class Wizard (osv.TransientModel):
    _name = 'cv_clearcorp.course.session.wizard'
    
    _columns = {
        'student_ids': fields.one2many('cv_clearcorp.course.session.wizard.students', 'wizard_id', string="Students"),
        'session_ids': fields.one2many('cv_clearcorp.course.session.wizard.sessions', 'wizard_id', string="Sessions"),
        }
    
class WizardStudents (osv.TransientModel):
    _name = "cv_clearcorp.course.session.wizard.students"
    
    _columns = {
        'wizard_id': fields.many2one('cv_clearcorp.course.session.wizard', 'Wizard'),
        'student_id': fields.many2one('res.partner', 'Student'),
        }
    
class WizardSessions (osv.TransientModel):
    _name = "cv_clearcorp.course.session.wizard.sessions"
    
    _columns = {
        'wizard_id': fields.many2one('cv_clearcorp.course.session.wizard', 'Wizard'),
        'session_id': fields.many2one('cv_clearcorp.course.session', 'Session'),
        }