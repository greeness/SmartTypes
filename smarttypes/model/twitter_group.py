from smarttypes.model.mongo_base_model import MongoBaseModel
from datetime import datetime, timedelta

class TwitterGroup(MongoBaseModel):
        
    collection_name = 'twitter_groups'
    properties = {
        'root_user_id':{'ok_types':[int]},
        'group_index':{'ok_types':[int]},
        'followers':{'ok_types':[list]}, #list of tups: (score, id)
        'following':{'ok_types':[list]},
        'group_adjacency':{'ok_types':[list]},
    }
    
    def get_significant_followers(self, significance_level=.4, top_users=0):
        from smarttypes.model.twitter_user import TwitterUser
        return_list = []
        i = 0
        for score, user_id in sorted(self.followers, reverse=True):
            if score >= significance_level or (top_users and i <= top_users):
                return_list.append((score, TwitterUser.get_by_id(user_id)))
            else:
                break
            i += 1
        return return_list
        
    def get_significant_following(self, significance_level=.4, top_users=0):
        from smarttypes.model.twitter_user import TwitterUser
        return_list = []
        i = 0
        for score, user_id in sorted(self.following, reverse=True):
            if score >= significance_level or (top_users and i <= top_users):
                return_list.append((score, TwitterUser.get_by_id(user_id)))
            else:
                break
            i += 1
        return return_list
        
    
    @classmethod
    def get_significant_users_for_all_groups(cls):
        """
        return something like this
        """
        from smarttypes.model.twitter_user import TwitterUser
        
        return_dict = {}
        for result in [cls.collection().find_one()]:
            group = cls(**result)
            return_dict[group.group_index] = (group, group.get_significant_following(top_users=5))
        return return_dict
            
    
    @classmethod
    def by_root_id_and_index(cls, root_id, index):
        return cls(**cls.collection().find({'root_user_id':root_id, 'group_index':index})[0])
    
    @classmethod
    def upsert_twitter_groups(cls, root_id, users_following_groups, groups_following_users, group_adjacency):
        #delete everything related to this root_id
        cls.bulk_delete('all')
        
        #save all the groups
        for i in range(len(users_following_groups)):
            followers = []
            for user_id, score in users_following_groups[i]:
                followers.append((score, user_id))
            following = []
            for user_id, score in groups_following_users[i]:
                following.append((score, user_id))
            properties = {
                'root_user_id': root_id,
                'group_index': i,
                'followers': followers,
                'following': following,
                'group_adjacency':group_adjacency[i],
            }
            twitter_group = cls(**properties)
            twitter_group.save()
            
            

                
            
            
        