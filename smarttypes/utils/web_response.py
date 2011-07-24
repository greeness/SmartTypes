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
    
    def __init__(self, return_str="", return_dict=None, content_type='xhtml', template_path=""):
        
        self.return_str = return_str
        self.return_dict = {} if not return_dict else return_dict
        self.content_type = content_type
        self.template_path = template_path

        
    def get_response_headers(self):

        if self.content_type == 'json':
            raise Exception('need to hook up simple json')

        content_type_string = 'html'
        if self.content_type not in ['xhtml']:
            content_type_string = self.content_type
        
        return [('Content-Type', 'text/'+content_type_string + '; charset=utf-8')]
    

    def get_response_str(self, page_name=''):

        #if there's a string we'll just return that
        if self.return_str:
            return [self.return_str]
        
        #using the template
        if not 'title' in self.return_dict: self.return_dict['title'] = smarttypes.default_title
        
        if page_name: 
            if not self.template_path: self.template_path = '%s.html' % page_name
            if not 'active_tab' in self.return_dict: self.return_dict['active_tab'] = page_name
        
        self.return_dict['site_name'] = smarttypes.site_name
        self.return_dict['site_mantra'] = smarttypes.site_mantra 
        self.return_dict['site_description'] = smarttypes.site_description
        
        template = loader.load(self.template_path)
        
        template_with_dict = template.generate(**self.return_dict)
        
        response_str = template_with_dict.render(self.content_type)
        
        return [response_str]
    
    
    
    
    
    
    
    

