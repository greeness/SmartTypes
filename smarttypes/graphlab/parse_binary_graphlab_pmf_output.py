
import sys, site
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import numpy, pickle

import smarttypes
from smarttypes.utils.mongo_handle import MongoHandle
from smarttypes.model.mongo_base_model import MongoBaseModel
mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
MongoBaseModel.mongo_handle = mongo_handle

from smarttypes.model.twitter_user import TwitterUser
from smarttypes.model.twitter_group import TwitterGroup

num_users = 11
num_items = 11
num_features = 2

users_shape = (num_features, num_users)
users_file = open('/home/timmyt/graphlabapi/release/demoapps/pmf/smarttypes_pmf_%s_binary_users.out' % num_features, 'rb')
users_data = numpy.fromfile(file=users_file, dtype=float).reshape(users_shape)

items_shape = (num_features, num_items)
items_file = open('/home/timmyt/graphlabapi/release/demoapps/pmf/smarttypes_pmf_%s_binary_items.out' % num_features, 'rb')
items_data = numpy.fromfile(file=items_file, dtype=float).reshape(items_shape)

twitter_id_map_file = open('twitter_id_map.pickle', 'r')
twitter_id_map = pickle.load(twitter_id_map_file)
twitter_id_map_inv = dict((v,k) for k, v in twitter_id_map.iteritems())

test_file = open('after', 'w')
A = numpy.dot(numpy.transpose(users_data), items_data)
for i in range(len(A)):
    for j in range(len(A[i])):
        write_this = str(int(round(A[i][j])))
        test_file.write(write_this+',')
    test_file.write('\n')


#following_these_groups and followed_by_these_groups
if num_users == num_items:
    
    twitter_users = []
    for i in range(0, num_users):
        twitter_user = TwitterUser.get_by_id(twitter_id_map_inv[i])
        twitter_user.following_these_groups = list(users_data[:,i])
        twitter_user.followed_by_these_groups = list(items_data[:,i])
        twitter_users.append(twitter_user)
        #twitter_user.save()
        
    #for i in range(0, num_features):
        #following_group = TwitterGroup()
        #following_group.group_type = TwitterGroup.GROUP_TYPE_FOLLOWING
        #following_group.group_index = i
        
        #followed_by_group = TwitterGroup()
        #followed_by_group.group_type = TwitterGroup.GROUP_TYPE_FOLLOWED_BY
        #followed_by_group.group_index = i
        
        ##data
        #following_group_data = users_data[i]
        #followed_by_group_data = items_data[i]
        
        ##map
        #following_group_map = {}
        #followed_by_group_map = {}
        #for j in range(0, num_users):
            #following_group_map[str(twitter_id_map_inv[j])] = following_group_data[j]
            #followed_by_group_map[str(twitter_id_map_inv[j])] = followed_by_group_data[j]

        #following_group.user_score_map = following_group_map
        #followed_by_group.user_score_map = followed_by_group_map

        ##following_group.save()
        ##followed_by_group.save()
        
        
        