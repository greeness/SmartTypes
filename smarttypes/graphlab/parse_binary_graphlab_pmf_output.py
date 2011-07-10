
import sys, site
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import numpy, pickle, struct

import smarttypes
from smarttypes.utils.mongo_handle import MongoHandle
from smarttypes.model.mongo_base_model import MongoBaseModel
mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
MongoBaseModel.mongo_handle = mongo_handle

from smarttypes.model.twitter_user import TwitterUser
#from smarttypes.model.twitter_group import TwitterGroup

#http://docs.python.org/library/struct.html

#// FORMAT: M N K D (4 x ints = user, movies, time bins, feature width (dimension))
#// MATRIX U ( M x D doubles)
#// MATRIX V ( N x D doubles)
#// MATRIX K ( K x D doubles - optional, only for tensor)
#// TOTAL FILE SIZE: 4 ints + (M+N+K)*D - for tensor
#// 4 ints + (M+N)*D - for matrix
graphlab_output_file = open('smarttypes_pmf.out', 'rb')

num_users = struct.unpack('i', graphlab_output_file.read(4))[0]
num_items = struct.unpack('i', graphlab_output_file.read(4))[0]
num_times = struct.unpack('i', graphlab_output_file.read(4))[0]
num_features = struct.unpack('i', graphlab_output_file.read(4))[0]

users_data = numpy.fromfile(file=graphlab_output_file, dtype=float, count=num_features*num_users).reshape((num_features, num_users))
items_data = numpy.fromfile(file=graphlab_output_file, dtype=float, count=num_features*num_items).reshape((num_features, num_items))

if True:
    test_file = open('after', 'w')
    A = numpy.dot(numpy.transpose(users_data), items_data) #the other way gives you a group adjancey graph i think
    for i in range(len(A)):
        for j in range(len(A[i])):
            write_this = str(int(round(A[i][j])))
            test_file.write(write_this+',')
        test_file.write('\n')

        
        
##fix this stuff        
#index_to_twitter_id_dict = pickle.load(open('index_to_twitter_id.pickle', 'r'))
    
    #twitter_users = []
    #for i in range(0, num_users):
        #twitter_user = TwitterUser.get_by_id(twitter_id_map_inv[i])
        #twitter_user.following_these_groups = list(users_data[:,i])
        #twitter_user.followed_by_these_groups = list(items_data[:,i])
        #twitter_users.append(twitter_user)
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
        
        
        