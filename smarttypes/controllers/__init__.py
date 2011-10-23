
import random

from smarttypes.config import *
from smarttypes.utils.postgres_web_decorator import postgres_web_decorator
from smarttypes.utils.web_response import WebResponse
from smarttypes.utils.exceptions import RedirectException
from genshi.core import Markup
from smarttypes.model.twitter_group import TwitterGroup
from smarttypes.model.twitter_user import TwitterUser
import tweepy


@postgres_web_decorator()
def home(request):
    return {}


@postgres_web_decorator()
def blog(request):
    
    #don't lose old urls
    changed_url_map = {
        'blog/graphlab_and_python_vs_complexity':'blog/complexity_probability_social_networks_and_python'
    }
    
    template_path = "blog/home.html"
    if request.path.find('/',1) > 0: #path looks like '/blog/something'
        request_path = request.path[1:]
        template_path = "%s.html" % changed_url_map.get(request_path, request_path)
    
    return {
        'template_path':template_path,
        'active_tab':'blog',
    }


@postgres_web_decorator()
def logged_in_user(request):
    
    screen_name = request.params['screen_name']
    logged_in_user = TwitterUser.by_screen_name(screen_name)
    return {
        'logged_in_user':logged_in_user,
        'TwitterGroup':TwitterGroup,
    }


@postgres_web_decorator()
def user(request):
    
    if 'user_id' in request.params:
        user_id = int(request.params['user_id'])
        twitter_user = TwitterUser.get_by_id(user_id)
    else:
        screen_name = request.params['screen_name']
        twitter_user = TwitterUser.by_screen_name(screen_name)
    
    return {
        'twitter_user':twitter_user,
    }


@postgres_web_decorator()
def group(request):
    
    if 'group_index' in request.params:
        group_index = int(request.params['group_index'])
        twitter_group = TwitterGroup.get_by_index(group_index)
    else:
        twitter_group = TwitterGroup.get_random_group()
        
    return {
        'twitter_group':twitter_group,
    }



@postgres_web_decorator()
def sign_in(request):
    #auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, 'http://www.smarttypes.org/')
    #auth.get_authorization_url()
    #auth.request_token
    return {}

@postgres_web_decorator()
def about(request):
    return {}

@postgres_web_decorator()
def contact(request):
    return {}


    




