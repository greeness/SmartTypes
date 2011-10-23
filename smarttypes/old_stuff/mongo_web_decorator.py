from exceptions import RedirectException
import smarttypes
from smarttypes.utils.mongo_handle import MongoHandle
from smarttypes.model.mongo_base_model import MongoBaseModel
from smarttypes.model.twitter_user import TwitterUser

def mongo_web_decorator():
    def wrapper0(controller):
        def wrapper1(request):
            try:
                #mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
                #MongoBaseModel.mongo_handle = mongo_handle
                web_response = controller(request)
                response_headers = web_response.get_response_headers()
                response_string = web_response.get_response_str(controller.__name__)
                status_code = '200 OK'
            except RedirectException, (redirect_ex):                
                status_code = '303 See Other'
                response_headers = [('Location', redirect_ex.redirect_url)]
                response_string = [""]
            return (status_code, response_headers, response_string) 
        return wrapper1
    return wrapper0

