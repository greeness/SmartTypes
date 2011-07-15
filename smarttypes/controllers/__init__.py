
from smarttypes.utils.mongo_web_decorator import mongo_web_decorator
from smarttypes.utils.web_response import WebResponse
from smarttypes.utils.exceptions import RedirectException
from smarttypes.utils.validation_utils import is_valid_email
from smarttypes import model

from genshi.core import Markup


@mongo_web_decorator()
def home(request):
    return WebResponse()

@mongo_web_decorator()
def explore(request):
    return WebResponse()

@mongo_web_decorator()
def sign_in(request):
    return WebResponse()

@mongo_web_decorator()
def about(request):
    return WebResponse()

@mongo_web_decorator()
def contact(request):
    return WebResponse()


    




