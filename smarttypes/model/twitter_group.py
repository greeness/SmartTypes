

from smarttypes.model.mongo_base_model import MongoBaseModel
from smarttypes.utils.validation_utils import mk_valid_ascii_str

from datetime import datetime, timedelta
from types import NoneType
import numpy, random, heapq


class TwitterGroup(MongoBaseModel):
        
    collection_name = 'twitter_groups'
    properties = {
        'group_index':{'ok_types':[int]},
        'group_type':{'ok_types':[str]},
        'user_score_map':{'ok_types':[dict]}
    }
    
    GROUP_TYPE_FOLLOWING = 'following_group'
    GROUP_TYPE_FOLLOWED_BY = 'followed_by_group'

    @property
    def user_score_map_inv(self):
        return [(v,k) for k, v in self.user_score_map.iteritems()]
    
    
    def top_users(self, num_users):
        from smarttypes.model.twitter_user import TwitterUser
        return_list = []
        for score, user_id in heapq.nlargest(num_users, self.user_score_map_inv):
            user = TwitterUser.get_by_id(int(user_id))
            return_list.append((user, score))
        return return_list
    
    

    @classmethod
    def by_index_and_type(cls, group_index, group_type):
        result = cls.collection().find_one({'group_index':group_index, 'group_type':group_type})
        if result:
            return cls(**result)
        else:
            return None

        
        
        
        