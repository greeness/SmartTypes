from smarttypes.model.mongo_base_model import MongoBaseModel
from datetime import datetime, timedelta
from smarttypes.utils import time_utils
import string, heapq

class TwitterGroup(MongoBaseModel):
        
    collection_name = 'twitter_groups'
    properties = {
        'group_index':{'ok_types':[int]},
        'followers':{'ok_types':[list]}, #list of tups: (score, id)
        'following':{'ok_types':[list]},
        'hybrid':{'ok_types':[list]},
        'following_groups':{'ok_types':[list]},
        'followedby_groups':{'ok_types':[list]},
        'hybrid_groups':{'ok_types':[list]},
    }
    
    FOLLOWING = "following" #group is following these people
    FOLLOWERS = "followers" #group is followed by these people
    FOLLOWING_GROUPS = "following" #group is following these groups
    FOLLOWEDBY_GROUPS = "followedby" #group is followedby these groups
    HYBRID = "hybrid"
    
    @property
    def name(self):
        return "blah"
        word_counts = {}
        #for top_user in self.top_users(num_users=50):
            #for word in top_user.description.split():
                #if word in word_counts:
                    #word_counts[word] += 1
                #else:
                    #word_counts[word] = 1
        #word_counts = [(y,x) for x,y in word_counts.items()]
        #return heapq.nlargest(10, word_counts)
    
    def top_users(self, relationship="hybrid", significance_level=0, num_users=0, just_ids=False):
        from smarttypes.model.twitter_user import TwitterUser
        
        if relationship == self.FOLLOWING:
            search_these_users = self.following
        if relationship == self.FOLLOWERS:
            search_these_users = self.followers
        if relationship == self.HYBRID:
            search_these_users = self.hybrid
        
        return_list = []
        i = 0
        for score, user_id in sorted(search_these_users, reverse=True):
            if (significance_level and score >= significance_level) or (num_users and i <= num_users):
                add_this = (score, user_id)
                if not just_ids:
                    add_this = (score, TwitterUser.get_by_id(user_id))
                return_list.append(add_this)
            else:
                break
            i += 1
        return return_list
        
    def top_groups(self, relationship="hybrid", significance_level=0, num_groups=0):
        if relationship == self.FOLLOWING_GROUPS:
            search_these_groups = self.following_groups
        if relationship == self.FOLLOWEDBY_GROUPS:
            search_these_groups = self.followedby_groups
        if relationship == self.HYBRID:
            search_these_groups = self.hybrid_groups
            
        return_list = []
        i = 0
        for score, group_id in sorted(search_these_groups, reverse=True):
            if (significance_level and score >= significance_level) or (num_groups and i <= num_groups):
                return_list.append((score, TwitterGroup.get_by_index(group_id)))
            else:
                break
            i += 1
        return return_list
    
    def group_inferred_top_users(self, relationship="hybrid", significance_level=0, num_users=0):
        from smarttypes.model.twitter_user import TwitterUser
        compare_w_this_many_groups = 10
        
        #ave scores of related groups
        users_dict = {}
        for score_group_tup in self.top_groups(relationship, num_groups=compare_w_this_many_groups):
            for score_user_tup in score_group_tup[1].top_users(relationship, significance_level, 50, True):
                user_id = score_user_tup[1]
                if user_id in users_dict:
                    users_dict[user_id] += score_user_tup[0]
                else:
                    users_dict[user_id] = score_user_tup[0]

        #what's unique about me?
        search_these_users = []
        for score_user_tup in self.top_users(relationship, significance_level, 40, True):
            user_id = score_user_tup[1]
            compare_to_total = users_dict[user_id] if user_id in users_dict else 0
            compare_to_avg = compare_to_total / compare_w_this_many_groups
            better_score = score_user_tup[0] - compare_to_avg
            search_these_users.append((better_score, user_id))
            
        return_list = []
        i = 0
        for score, user_id in sorted(search_these_users, reverse=True):
            if (significance_level and score >= significance_level) or (num_users and i <= num_users):
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
    def upsert_group(cls, group_index, followers, following, hybrid, group_adjacency):
        properties = {
            'group_index': group_index,
            'followers': followers,
            'following': following,
            'hybrid':hybrid,
            'following_groups':group_adjacency[0],
            'followedby_groups':group_adjacency[1],
            'hybrid_groups':group_adjacency[2],
        }
        twitter_group = cls(**properties)
        twitter_group.save()


            
            

                
            
            
        