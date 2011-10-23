
import sys, site, atexit, pprint, pickle
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import smarttypes
from smarttypes.config import *

#from smarttypes.utils.log_handle import LogHandle
#log_handle = LogHandle('get_twitter_retweets.log')

from smarttypes.utils.postgres_handle import PostgresHandle
from smarttypes.model.postgres_base_model import PostgresBaseModel
postgres_handle = PostgresHandle(smarttypes.connection_string)
PostgresBaseModel.postgres_handle = postgres_handle

from smarttypes.model.twitter_user import TwitterUser

import tweepy
from tweepy.streaming import StreamListener, Stream


class Listener(StreamListener):
    
    def __init__(self, monitor_these_user_ids, api=None):
        StreamListener.__init__(self)
        self.monitor_these_user_ids = monitor_these_user_ids
        self.pickle_file = open('/tmp/tweet_status.pickle', 'w')
    
    def on_error(self, status_code):
        print "Error: %s" % status_code
        return False    
    
    def on_status(self, status):
        if status.author.id in self.monitor_these_user_ids:
            pickle.dump(status, self.pickle_file)
            self.pickle_file.close()
            print "done"
        
            return False
        
        #dont forget this
        return True
            
    
if __name__ == "__main__":

    if not len(sys.argv) > 1:
        args_dict = {'screen_name':'SmartTypes'}
    else:
        args_dict = eval(sys.argv[1])
    screen_name = args_dict['screen_name']
    twitter_user = TwitterUser.by_screen_name(screen_name)
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    monitor_these_user_ids = twitter_user.following_following_ids[:4000]
    print "Num of users to monitor: %s" % len(monitor_these_user_ids)
    listener = Listener(monitor_these_user_ids)
    stream = Stream(auth,listener)

    stream.filter(follow=monitor_these_user_ids)







