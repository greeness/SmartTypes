from smarttypes.model.mongo_base_model import MongoBaseModel
from datetime import datetime, timedelta
from smarttypes.utils import time_utils

class TwitterGroup(MongoBaseModel):
        
    collection_name = 'twitter_groups'
    properties = {
        'group_index':{'ok_types':[int]},
        'followers':{'ok_types':[list]}, #list of tups: (score, id)
        'following':{'ok_types':[list]},
        'following_groups':{'ok_types':[list]},
        'followedby_groups':{'ok_types':[list]},
    }
    
    FOLLOWING = "following" #group is following these people
    FOLLOWERS = "followers" #group is followed by these people
    FOLLOWING_GROUPS = "following" #group is following these groups
    FOLLOWEDBY_GROUPS = "followedby" #group is followedby these groups
    HYBRID = "hybrid"
    
    def top_users(self, relationship, significance_level=.4, num_users=0):
        from smarttypes.model.twitter_user import TwitterUser
        
        if relationship == self.FOLLOWING:
            search_these_users = self.following
        if relationship == self.FOLLOWERS:
            search_these_users = self.followers
        if relationship == self.HYBRID:
            following_dict = dict([(y,x) for x,y in self.following])
            search_these_users = []
            for score, user_id in self.followers:
                hybrid_score = (following_dict[user_id] + score) / 2
                search_these_users.append((hybrid_score, user_id))
        
        return_list = []
        i = 0
        for score, user_id in sorted(search_these_users, reverse=True):
            if score >= significance_level or (num_users and i <= num_users):
                return_list.append((score, TwitterUser.get_by_id(user_id)))
            else:
                break
            i += 1
        return return_list
        
    def top_groups(self, relationship, significance_level=.4, num_groups=0):
        if relationship == self.FOLLOWING_GROUPS:
            search_these_groups = self.following_groups
        if relationship == self.FOLLOWEDBY_GROUPS:
            search_these_groups = self.followedby_groups
        if relationship == self.HYBRID:
            following_groups_dict = dict([(y,x) for x,y in self.following_groups])
            search_these_groups = []
            for score, group_id in self.followedby_groups:
                hybrid_score = (following_groups_dict[group_id] + score) / 2
                search_these_groups.append((hybrid_score, group_id))            
            
        return_list = []
        i = 0
        for score, group_id in sorted(search_these_groups, reverse=True):
            if score >= significance_level or (num_groups and i <= num_groups):
                return_list.append((score, TwitterGroup.get_by_index(group_id)))
            else:
                break
            i += 1
        return return_list
    
    def group_inferred_top_users(self, relationship, significance_level=.4, num_users=0):
        users_dict = {}
        for score_group_tup in self.top_groups(relationship, significance_level, 5):
            for score_user_tup in self.top_users(relationship, significance_level, num_users):
                inferred_score = score_group_tup[0] * score_user_tup[0]
                user_id = score_user_tup[1].twitter_id
                if user_id in users_dict:
                    users_dict[user_id] += inferred_score
                else:
                    users_dict[user_id] = inferred_score
    
        search_these_users = [(y,x) for x,y in users_dict.items()]
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
            'following_groups':group_adjacency[0],
            'followedby_groups':group_adjacency[1],
        }
        twitter_group = cls(**properties)
        twitter_group.save()


            
            

                
            
            
        