"""
run from cron every hour
"""

import sys, site, atexit
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import smarttypes
from smarttypes.config import *

#from smarttypes.utils.log_handle import LogHandle
#log_handle = LogHandle('get_twitter_retweets.log')

from smarttypes.utils.mongo_handle import MongoHandle
from smarttypes.model.mongo_base_model import MongoBaseModel
mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
MongoBaseModel.mongo_handle = mongo_handle

from smarttypes.model.twitter_user import TwitterUser
from smarttypes.model.twitter_retweet import TwitterRetweet

import tweepy
from tweepy.streaming import StreamListener, Stream


class Listener(StreamListener):
    
    def __init__(self, monitor_these_user_ids, api=None):
        StreamListener.__init__(self)
        self.monitor_these_user_ids = monitor_these_user_ids
    
    def on_error(self, status_code):
        print "Error: %s" % status_code
        return False    
    
    def on_status(self, status):
        if hasattr(status, 'retweeted_status') and status.author.id in self.monitor_these_user_ids:
            retweet = TwitterRetweet.upsert_from_api_status(status)
            print "-" * 20
            print retweet.to_dict()
            
        #dont forget this
        return
            
    
if __name__ == "__main__":

    args_dict = eval(sys.argv[1])
    screen_name = args_dict['screen_name']
    twitter_user = TwitterUser.by_screen_name(screen_name)
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    monitor_these_user_ids = twitter_user.monitor_these_user_ids()
    print "Num of users to monitor: %s" % len(monitor_these_user_ids)
    listener = Listener(monitor_these_user_ids)
    stream = Stream(auth,listener)

    stream.filter(follow=monitor_these_user_ids)







