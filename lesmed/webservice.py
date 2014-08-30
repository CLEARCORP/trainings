import xmlrpclib

username = 'admin'
password = 'admin'
database = 'trainings'
server = 'localhost'
port = '8069'

sock_common = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/common' % (server,port))
uid = sock_common.login(database, username, password)
print uid

sock = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/object' % (server,port))
# COn dominio para el filtro
course_ids = sock.execute(database, uid, password, 'lesmed.course', 'search', [('code','=','IC-997')])
# SIn dominio para el filtro
# course_ids = sock.execute(database, uid, password, 'jornamon.course', 'search', [])
print course_ids
courses = sock.execute(database, uid, password, 'lesmed.course', 'read', course_ids, ['code','name'])
print courses
res = sock.execute(database, uid, password, 'lesmed.course', 'check_seats', course_ids)
print res



