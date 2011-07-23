from smarttypes.model.mongo_base_model import MongoBaseModel
from datetime import datetime, timedelta
from smarttypes.utils import time_utils
import string, heapq
from smarttypes.utils.log_handle import LogHandle
log_handle = LogHandle('twitter_group.log')

class TwitterGroup(MongoBaseModel):
        
    collection_name = 'twitter_groups'
    primary_key_name = 'group_index'
    properties = {
        'group_index':{'ok_types':[int]},
        'scores_users':{'ok_types':[list]}, #list of tups: (score, id)
    }
    
    @property
    def name(self):
        return "blah"
    
        #for top_user in self.top_users(num_users=50):
            #for word in top_user.description.split():
                #if word in word_counts:
                    #word_counts[word] += 1
                #else:
                    #word_counts[word] = 1
        #word_counts = [(y,x) for x,y in word_counts.items()]
        #return heapq.nlargest(10, word_counts)
    
    def top_users(self, num_users=20, just_ids=False):
        from smarttypes.model.twitter_user import TwitterUser
        
        return_list = []
        i = 0
        for score, user_id in sorted(self.scores_users, reverse=True):
            if i <= num_users:
                add_this = (score, user_id)
                if not just_ids:
                    add_this = (score, TwitterUser.get_by_id(user_id))
                return_list.append(add_this)
            else:
                break
            i += 1
        return return_list
        

    ##############################################
    ##class methods
    ############################################## 
    @classmethod
    def get_all_groups(cls):
        return_list = []
        for result in cls.collection().find():
            return_list.append(cls(**result))
        return return_list
    
    @classmethod
    def get_by_index(cls, group_index):
        return cls(**cls.collection().find_one({'group_index':group_index}))
    
    @classmethod
    def upsert_group(cls, group_index, scores_users, scores_groups):
        properties = {
            'group_index': group_index,
            'scores_users':scores_users,
            'scores_groups':scores_groups,
        }
        twitter_group = cls(**properties)
        twitter_group.save()


            
            

                
            
            
        