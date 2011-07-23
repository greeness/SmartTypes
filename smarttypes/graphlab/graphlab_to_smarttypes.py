
"""
We're running this on a remote ec2 instance
"""

#tunnel mongo traffic through ssh
#problem -- http://www.learnosity.com/techblog/index.cfm/2008/2/18/SSH-Portforward--Address-already-in-use--Solved
import subprocess
subprocess.call('ssh timmyt@66.228.60.238 -N -f -L 27017:localhost:27017', shell=True)

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
from smarttypes.model.twitter_user import TwitterUser

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

group_adjacency = []
A = numpy.dot(users_data, numpy.transpose(items_data))
for i in range(num_features):
    membership_scores = []
    for j in range(num_features):
        membership_scores.append((A[i][j] * A[j][i], j))
    group_adjacency.append(membership_scores)
        
index_to_twitter_id_dict = pickle.load(open('index_to_twitter_id.pickle', 'r'))
user_group_map = {} 
TwitterGroup.bulk_delete('all')
for i in range(num_features):
    membership_scores = []
    for j in range(num_items):
        user_id = index_to_twitter_id_dict[j]
        follower_score = users_data[i][j]
        following_score = items_data[i][j]
        membership_score = following_score * following_score
        if membership_score > .001:
            membership_scores.append((membership_score, user_id))
            if user_id not in user_group_map:
                user_group_map[user_id] = [(membership_score, i)]
            else:
                user_group_map[user_id].append((membership_score, i))
    TwitterGroup.upsert_group(i, membership_scores, group_adjacency[i])
print "Done creating groups."

TwitterUser.bulk_update('all', {'scores_groups':None})
i = 0    
for user_id, scores_groups in user_group_map.items():
    twitter_user = TwitterUser.get_by_id(user_id)
    twitter_user.scores_groups = scores_groups
    twitter_user.save()
    if i % 1000 == 0: print "Done with %s users." % i
    i += 1
    
    
    
    
    
