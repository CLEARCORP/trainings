# -*- coding: utf-8 -*-

import xmlrpclib

username = 'admin'
password = 'admin'
database = 'trainings'
server = 'localhost'
port = '8069'

sock_common = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/common' % (server,port))
uid = sock_common.login(database, username, password)
print uid


