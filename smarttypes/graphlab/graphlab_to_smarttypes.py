
import sys, site
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import numpy, pickle, struct

import smarttypes
from smarttypes.utils.mongo_handle import MongoHandle
from smarttypes.model.mongo_base_model import MongoBaseModel
mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
MongoBaseModel.mongo_handle = mongo_handle
from smarttypes.model.twitter_group import TwitterGroup

graphlab_output_file = open('smarttypes_pmf.out', 'rb')

num_users = struct.unpack('i', graphlab_output_file.read(4))[0]
num_items = struct.unpack('i', graphlab_output_file.read(4))[0]
num_times = struct.unpack('i', graphlab_output_file.read(4))[0]
num_features = struct.unpack('i', graphlab_output_file.read(4))[0]

users_data = numpy.fromfile(file=graphlab_output_file, dtype=float, count=num_features*num_users).reshape((num_features, num_users))
items_data = numpy.fromfile(file=graphlab_output_file, dtype=float, count=num_features*num_items).reshape((num_features, num_items))

#testing; should look close to the initial adjacency matrix
if False:
    test_file = open('after', 'w')
    A = numpy.dot(numpy.transpose(users_data), items_data) #the other way gives you a group adjacency graph i think
    for i in range(len(A)):
        for j in range(len(A[i])):
            write_this = str(int(round(A[i][j])))
            test_file.write(write_this+',')
        test_file.write('\n')

#group_adjacency
group_adjacency = []
A = numpy.dot(users_data, numpy.transpose(items_data))
for i in range(num_features):
    group_is_following = []
    for j in range(num_features):
        group_is_following.append(A[i][j])
    group_adjacency.append(group_is_following)
        
#save group info
index_to_twitter_id_dict = pickle.load(open('index_to_twitter_id.pickle', 'r'))
users_following_groups = []
groups_following_users = []
for i in range(num_features):
    users_following = []
    groups_following = []
    for j in range(num_items):
        user_id = index_to_twitter_id_dict[j]
        users_following.append((user_id, users_data[i][j]))
        groups_following.append((user_id, items_data[i][j]))
    users_following_groups.append(users_following)
    groups_following_users.append(groups_following)

TwitterGroup.upsert_twitter_groups(1, users_following_groups, groups_following_users, group_adjacency)



