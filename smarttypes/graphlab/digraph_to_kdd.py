
"""
take a twitter user graph and write to yahoo kdd format 

see http://kddcup.yahoo.com/datasets.php for details on yahoo kdd format

then we'll use read_kdd_data_write_graphlab_binary.py to get to graphlab_binary

then we'll use graphlab

then i need to figure out how to read the graphlab output
"""

import sys, site, pickle
from datetime import datetime, timedelta
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

import numpy
from sets import Set

import smarttypes
from smarttypes.utils.mongo_handle import MongoHandle
from smarttypes.model.mongo_base_model import MongoBaseModel
mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
MongoBaseModel.mongo_handle = mongo_handle

from smarttypes.model.twitter_user import TwitterUser


def write_data(following_dict, twitter_id_map, index_map, output_file):
    
    test_file = open('initial', 'w')
    for i in sorted(index_map.keys()):
        output_file.write("%s|%s\n" % (i, len(index_map.keys())))
        following_index_ids = Set([twitter_id_map[x] for x in following_dict[index_map[i]]])
        for j in sorted(index_map.keys()):
            value = 1 if j in following_index_ids else 0
            output_file.write("%s\t%s\t%s\n" % (j, value, 1))
            test_file.write(str(value)+',')
        test_file.write('\n')    


if __name__ == "__main__":
    
    args_dict = eval(sys.argv[1] if len(sys.argv) > 1 else "{'screen_name':'SmartTypes'}")
    screen_name = args_dict['screen_name']

    output_file = open('%s_kdd.txt' % screen_name, 'w')
    twitter_user = TwitterUser.by_screen_name(screen_name)
    
    following_dict = {}
    following_dict[twitter_user.twitter_id] = twitter_user.following_ids
    print "starting collect all followers loop"
    for following_user in twitter_user.following:
        
        if following_user.twitter_id not in following_dict:
            following_dict[following_user.twitter_id] = following_user.following_ids
            
        for following_following_user in following_user.following:
            if following_following_user.following_ids and following_following_user.twitter_id not in following_dict:
                following_dict[following_following_user.twitter_id] = following_following_user.following_ids
                    
        record_count = len(following_dict.keys())
        if record_count % 10000 == 0:
            print record_count
    print "finshed collect all followies loop, %s records" % record_count 
    
    
    we_have_dup_followie_ids = []
    unique_followie_ids = {}
    whittled_following_dict = {}
    print "starting whittle followies loop"
    for twitter_id, followie_ids in following_dict.items():
        
        #check for dups
        if len(followie_ids) != len(Set(followie_ids)):
            we_have_dup_followie_ids.append(twitter_id)
            
        whittled_following_dict[twitter_id] = []
        
        for followie_id in followie_ids:
            #only use followies that are also followers            
            if followie_id in following_dict:
                whittled_following_dict[twitter_id].append(followie_id)
            
                #save for below
                if followie_id not in unique_followie_ids:
                    unique_followie_ids[followie_id] = True
                    
    if we_have_dup_followie_ids:
        raise Exception('%s people have dup followies. %s' % (len(we_have_dup_followie_ids), we_have_dup_followie_ids))
    print "finshed whittle followies loop"

    
    #get rid of any followers that are not also followies
    delete_these_keys = []
    for follower_id in whittled_following_dict.keys():
        if follower_id not in unique_followie_ids:
            delete_these_keys.append(follower_id)
    for delete_this_key in delete_these_keys:
        del whittled_following_dict[delete_this_key]     
        
        
    #now we can map twitter ids to index related ids
    twitter_id_map = {}
    index_map = {}
    i = 0
    for twitter_id in sorted(whittled_following_dict.keys()):
        twitter_id_map[twitter_id] = i
        index_map[i] = twitter_id
        i += 1

    #pickle twitter_id_map, we'll need it later
    twitter_id_map_file = open('twitter_id_map.pickle', 'w')
    pickle.dump(twitter_id_map, twitter_id_map_file)
    
    #write everything
    print "about to write everything"
    write_data(whittled_following_dict, twitter_id_map, index_map, output_file)            
            
    print "All done!"
    print "Wrote %s users!" % len(whittled_following_dict)
    print "Following average: %s." % numpy.average([len(x) for x in whittled_following_dict.values()])
    
    
    
