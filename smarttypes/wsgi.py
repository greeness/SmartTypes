
import sys, site
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import re, traceback
from webob import Request
import smarttypes

from smarttypes.utils import web_monitor
web_monitor.start(interval=1.0)
web_monitor.track('/home/timmyt/projects/smarttypes/smarttypes/templates')

from smarttypes.utils.mongo_handle import MongoHandle
from smarttypes.model.mongo_base_model import MongoBaseModel

urls = [
    (r'^$', smarttypes.controllers.home),
    (r'about/?$', smarttypes.controllers.about),
    (r'contact/?$', smarttypes.controllers.contact),
]

def application(environ, start_response):
    mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
    MongoBaseModel.mongo_handle = mongo_handle
    
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, controller in urls:
        match = re.search(regex, path)
        if match:
            request = Request(environ)
            try:                
                status_code, response_headers, body = controller(request, mongo_handle)
                start_response(status_code, response_headers)
                return body
            except Exception, ex:
                #can't use print statements with mod_wsgi
                error_string = traceback.format_exc()
                start_response('500 Internal Server Error', 
                               [('Content-Type', 'text/plain')])
                return [error_string]
        
    #couldn't find it        
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return ["Couldn't find the URL specified. %s" % path]