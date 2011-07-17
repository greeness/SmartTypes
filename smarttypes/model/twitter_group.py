from smarttypes.model.mongo_base_model import MongoBaseModel
from datetime import datetime, timedelta
from smarttypes.utils import time_utils

class TwitterGroup(MongoBaseModel):
        
    collection_name = 'twitter_groups'
    properties = {
        'group_index':{'ok_types':[int]},
        'followers':{'ok_types':[list]}, #list of tups: (score, id)
        'following':{'ok_types':[list]},
        'group_adjacency':{'ok_types':[list]},
    }
    
    FOLLOWING = "following" #group is following these people
    FOLLOWERS = "followers" #group is followed by these people
    
    def top_users(self, ing_or_ers, significance_level=.4, num_users=0):
        from smarttypes.model.twitter_user import TwitterUser
        
        if ing_or_ers == self.FOLLOWING:
            search_these_users = self.following
        if ing_or_ers == self.FOLLOWERS:
            search_these_users = self.followers
        
        return_list = []
        i = 0
        for score, user_id in sorted(search_these_users, reverse=True):
            if score >= significance_level or (num_users and i <= num_users):
                return_list.append((score, TwitterUser.get_by_id(user_id)))
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
        return cls(**cls.collection().find({'group_index':group_index})[0])
    
    @classmethod
    def upsert_group(cls, group_index, followers, following, group_adjacency):
        properties = {
            'group_index': group_index,
            'followers': followers,
            'following': following,
            'group_adjacency':group_adjacency,
        }
        twitter_group = cls(**properties)
        twitter_group.save()


            
            

                
            
            
        