
"""
We're running this on a remote ec2 instance
"""

#tunnel mongo traffic through ssh
import subprocess
subprocess.call('ssh timmyt@66.228.60.238 -N -f -L 27017:localhost:27017', shell=True)

import sys, site, pickle
from datetime import datetime, timedelta
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

from numpy import array, vstack, dtype, amax, average  
from sets import Set

import smarttypes
from smarttypes.utils.mongo_handle import MongoHandle
from smarttypes.model.mongo_base_model import MongoBaseModel
mongo_handle = MongoHandle(smarttypes.connection_string, smarttypes.database_name)
MongoBaseModel.mongo_handle = mongo_handle

from smarttypes.model.twitter_user import TwitterUser


def mk_matrix(following_dict, twitter_id_map, index_map, debug=True):
    
    userList, itemList, timeList, rateList = [], [], [], []
    
    #for testing small runs
    if debug: test_file = open('initial', 'w')
    for i in sorted(index_map.keys()):
        following_index_ids = Set([twitter_id_map[x] for x in following_dict[index_map[i]]])
        for j in sorted(index_map.keys()):
            rating = 1 if j in following_index_ids else 0            
            #if rating:
            userList.append(i)
            itemList.append(j)
            timeList.append(1)
            rateList.append(rating)
            if debug: test_file.write(str(rating)+',')
        if debug: test_file.write('\n')    

    del following_dict, twitter_id_map, index_map
        
    user_array = array(userList, dtype=dtype('f4'))
    del userList
    
    item_array = array(itemList, dtype=dtype('f4'))
    del itemList
    
    time_array = array(timeList, dtype=dtype('f4'))
    del timeList
    
    rate_array = array(rateList, dtype=dtype('f4'))
    del rateList
    
    rateMat = vstack((user_array, item_array, time_array, rate_array)).T  
    del user_array, item_array, time_array, rate_array
    
    return rateMat           
            

def saveDataToBin(rateMat, outfile_path):
    
    nUser = int(amax(rateMat[:,0]))+1 # nUser is max user ID read  
    nItem = int(amax(rateMat[:,1]))+1 # nItem is max itemID read  
    nTime = int(amax(rateMat[:,2]))   # nTime is max time read
    nRate = rateMat.shape[0]
      
    # setup size and rateMat  
    size = array([nUser, nItem, nTime, nRate], dtype=dtype('i4'))  
  
    rateMat[:,0] +=1 # user index starts from 0, graphlab pmf expects 1  
    rateMat[:,1] += nUser+1 # item index starts from 0, graphlab pmf expects nUser+1  
    
    filehandle = open(outfile_path,'wb')            
    size.tofile(filehandle)  
    rateMat.tofile(filehandle)  
    filehandle.close()
        
        
if __name__ == "__main__":
    
    args_dict = eval(sys.argv[1] if len(sys.argv) > 1 else "{'screen_name':'SmartTypes'}")
    screen_name = args_dict['screen_name']

    twitter_user = TwitterUser.by_screen_name(screen_name)
    
    following_dict = {}
    following_dict[twitter_user.twitter_id] = twitter_user.following_ids
    print "Collect all followers"
    for following_user in twitter_user.following[:10]:
        
        if following_user.twitter_id not in following_dict:
            following_dict[following_user.twitter_id] = following_user.following_ids
            
        #for following_following_user in following_user.following:
            #if following_following_user.following_ids and following_following_user.twitter_id not in following_dict:
                #following_dict[following_following_user.twitter_id] = following_following_user.following_ids
                
        record_count = len(following_dict.keys())
        if record_count % 10000 == 0:
            print record_count
    print "Finshed collect all followies loop, %s records" % record_count 
    
    
    we_have_dup_followie_ids = []
    unique_followie_ids = {}
    whittled_following_dict = {}
    print "Whittle followies"
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

    #we'll need this later
    index_to_twitter_id_file = open('index_to_twitter_id.pickle', 'w')
    pickle.dump(index_map, index_to_twitter_id_file)
    
    print "Create matrix"
    rateMat = mk_matrix(whittled_following_dict, twitter_id_map, index_map)            
    
    print "Save to disk"
    saveDataToBin(rateMat, "smarttypes_pmf")       
    
    print "All done!"
    print "Wrote %s users!" % len(whittled_following_dict)
    print "Following average: %s." % average([len(x) for x in whittled_following_dict.values()])
    
    
    
