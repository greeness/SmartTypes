"""
run from cron
"""
import sys, site
from datetime import datetime, timedelta
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import smarttypes
from smarttypes.config import *

#from smarttypes.utils.log_handle import LogHandle
#log_handle = LogHandle('get_twitter_friends.log')

from smarttypes.utils.postgres_handle import PostgresHandle
from smarttypes.model.postgres_base_model import PostgresBaseModel
postgres_handle = PostgresHandle(smarttypes.connection_string)
PostgresBaseModel.postgres_handle = postgres_handle

import tweepy
from tweepy import TweepError
from smarttypes.model.twitter_user import TwitterUser
from smarttypes.utils.twitter_api_utils import get_rate_limit_status

MAX_FOLLOWING_COUNT = TwitterUser.MAX_FOLLOWING_COUNT
AVG_PEOPLE_RETURNED_PER_QUERY = 80
REMAINING_HITS_THRESHOLD = 20
if (MAX_FOLLOWING_COUNT / AVG_PEOPLE_RETURNED_PER_QUERY) > REMAINING_HITS_THRESHOLD:
    raise Exception("get_twitter_friends script error: the code assumes this wont happen.")


def continue_or_exit(api_handle):
    remaining_hits, reset_time = get_rate_limit_status(api_handle)
    if remaining_hits < REMAINING_HITS_THRESHOLD:
        raise Exception("remaining_hits less than threshold")
        
def load_user_and_maybe_the_people_they_follow(api_handle, screen_name):
    print "Attempting to load %s" % screen_name
    continue_or_exit(api_handle)
    
    try:    
        api_user = api_handle.get_user(screen_name=screen_name)
    except TweepError, ex:
        print "Got a TweepError: %s." % ex  
        if str(ex) == "Not found":
            print "Setting caused_an_error for %s " % screen_name
            model_user = TwitterUser.by_screen_name(screen_name)
            model_user.caused_an_error = datetime.now()
            model_user.save()
            return model_user
    
    model_user = TwitterUser.upsert_from_api_user(api_user)        
    
    if api_user.protected:
        print "\t %s is protected" % screen_name
        return     
    
    if api_user.friends_count > MAX_FOLLOWING_COUNT:
        print "\t %s follows too many people, %s" % (screen_name, api_user.friends_count)
        model_user.save_following_ids([])
        return model_user
    
    if model_user.last_loaded_following_ids >= (datetime.now() - TwitterUser.RELOAD_FOLLOWING_IDS_THRESHOLD):
        print "\t %s already loaded recently" % screen_name
        return model_user
    
    print "Loading the people %s follows" % screen_name    
    following_ids = []
    try:
        api_following_list = list(tweepy.Cursor(api_handle.friends, screen_name).items())
    except TweepError, ex:
        print "Got a TweepError: %s." % ex  
        if str(ex) == "Not authorized":
            print "Setting caused_an_error for %s " % screen_name
            model_user.caused_an_error = datetime.now()
            model_user.save()
            return model_user
    
    for api_following in api_following_list:
        if api_following.protected:
            continue 
        model_following = TwitterUser.upsert_from_api_user(api_following)
        following_ids.append(model_following.twitter_id)
        
    model_user.save_following_ids(following_ids)
    postgres_handle.connection.commit()
    return model_user


if __name__ == "__main__":
    
    if not len(sys.argv) > 1:
        args_dict = {'screen_name':'SmartTypes'}
    else:
        args_dict = eval(sys.argv[1])
    screen_name = args_dict['screen_name']
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api_handle = tweepy.API(auth)
    
    twitter_user = load_user_and_maybe_the_people_they_follow(api_handle, screen_name)
    load_this_user = twitter_user.get_someone_in_my_network_to_load()
    while load_this_user:
        load_user_and_maybe_the_people_they_follow(api_handle, load_this_user.screen_name)
        load_this_user = twitter_user.get_someone_in_my_network_to_load()
        #load_this_user = None
        
    print "Finshed loading all related users for %s!" % screen_name
    
            