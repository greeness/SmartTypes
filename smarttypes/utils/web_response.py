import os
import smarttypes

from genshi.core import Stream
from genshi.output import encode, get_serializer
from genshi.template import Context, TemplateLoader    

#template loader
loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__), '../templates'),
    auto_reload=True)


class WebResponse(object):
    
    def __init__(self, request, controller_name, response_dict):
        self.request = request
        self.controller_name = controller_name
        self.response_dict = response_dict
        self.return_str = response_dict.get('return_str', None)
        self.content_type = response_dict.get('content_type', 'html')
                
    def get_response_headers(self):
        if self.content_type == 'json':
            raise Exception('TODO: need to hook up simple json.')
        return [('Content-Type', 'text/%s; charset=utf-8' % self.content_type)]

    def get_response_str(self):
        #if there's a string we'll just return that
        if self.return_str:
            return [self.return_str]
        
        #using the template
        self.response_dict['site_name'] = smarttypes.site_name
        self.response_dict['site_mantra'] = smarttypes.site_mantra 
        self.response_dict['site_description'] = smarttypes.site_description
        
        if not 'title' in self.response_dict: 
            self.response_dict['title'] = smarttypes.default_title
        if not 'template_path' in self.response_dict: 
            self.response_dict['template_path'] = '%s.html' % self.controller_name
        if not 'active_tab' in self.response_dict: 
            self.response_dict['active_tab'] = self.controller_name
                
        template = loader.load(self.response_dict['template_path'])
        template_with_dict = template.generate(**self.response_dict)
        response_str = template_with_dict.render(self.content_type)
        
        return [response_str]
    
    
    
    
    
    
    
    

