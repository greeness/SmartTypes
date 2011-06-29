
import sys, site
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import tweepy
from smarttypes.config import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitter_api_handle = tweepy.API(auth)

import smarttypes
from smarttypes.model.mongo_base_model import MongoBaseModel
from smarttypes.model.twitter_user import TwitterUser
from smarttypes.model.twitter_group import TwitterGroup

from smarttypes.utils.mongo_handle import MongoHandle
mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
MongoBaseModel.mongo_handle = mongo_handle
database = mongo_handle.database

twitter_users_coll = database['twitter_users']
twitter_groups_coll = database['twitter_groups']

me = TwitterUser.by_screen_name('SmartTypes')



