

from smarttypes.model.mongo_base_model import MongoBaseModel
from smarttypes.utils.validation_utils import mk_valid_ascii_str

from datetime import datetime, timedelta
from types import NoneType
import numpy, random, heapq
from sets import Set

class TwitterUser(MongoBaseModel):
        
    collection_name = 'twitter_users'
    primary_key_name = 'twitter_id'
    properties = {
        'twitter_id':{'ok_types':[int]},
        'screen_name':{'ok_types':[str, unicode]},
        'twitter_account_created':{'ok_types':[datetime]},
        'favourites_count':{'ok_types':[int]},
        'protected':{'ok_types':[bool]},
        'following_count':{'ok_types':[int]},
        
        'location_name':{'ok_types':[str, unicode, NoneType]},
        'description':{'ok_types':[str, unicode, NoneType]},
        'url':{'ok_types':[str, unicode, NoneType]},
        
        'last_loaded_following_ids':{'ok_types':[datetime], 'default':datetime(1970,1,1)},
        'following_ids':{'ok_types':[list], 'default':[]},        
        
        'caused_an_error':{'ok_types':[datetime, NoneType]},
        
        'following_groups':{'ok_types':[list, NoneType]},
        'followedby_groups':{'ok_types':[list, NoneType]},
        'hybrid_groups':{'ok_types':[list, NoneType]},
    }
    
    RELOAD_FOLLOWING_IDS_THRESHOLD = timedelta(days=7)
    MAX_FOLLOWING_COUNT = 1000
    TRY_AGAIN_AFTER_FAILURE_THRESHOLD = timedelta(days=31)
    
    FOLLOWING_GROUPS = "following" #user is following these groups
    FOLLOWEDBY_GROUPS = "followedby" #user is followedby these groups
    HYBRID = "hybrid"
    
    @property
    def following(self):
        return self.get_by_ids(self.following_ids)

    ##############################################
    ##related to get_someone_in_my_network_to_load
    ##############################################    
    @property
    def following_and_expired(self):
        return_list = []
        for user in self.following:            
            if user.should_we_query_this_user:
                return_list.append(user)
        return return_list
    
    @property
    def should_we_query_this_user(self):
        return self.is_last_loaded_following_ids_expired and \
               self.following_count <= self.MAX_FOLLOWING_COUNT and \
               self.no_recent_errors and \
               not self.protected
    
    @property
    def is_last_loaded_following_ids_expired(self):
        return self.last_loaded_following_ids < (datetime.now() - self.RELOAD_FOLLOWING_IDS_THRESHOLD)
    
    @property
    def no_recent_errors(self):
        if self.caused_an_error:
            return (datetime.now() - self.caused_an_error) >= self.TRY_AGAIN_AFTER_FAILURE_THRESHOLD
        return True    
    
    def get_random_followie_id(self, not_in_this_list=[]):
        random_index = random.randrange(0, len(self.following_ids)) 
        random_id = self.following_ids[random_index]
        if random_id in not_in_this_list:
            return self.get_random_followie_id(not_in_this_list)
        else:
            return random_id
        
    def get_someone_in_my_network_to_load(self):
        """
        keep in mind that 'loading' a user means storing all the people they follow 
        
        we 'load' self, the people self follows, and the people they follow 
        """
        following_and_expired_list = self.following_and_expired
        if following_and_expired_list:
            return following_and_expired_list[0]
        else:
            tried_to_load_these_ids = []
            for i in range(len(self.following_ids)):
                random_following_id = self.get_random_followie_id(tried_to_load_these_ids)
                random_following = TwitterUser.get_by_id(random_following_id)
                random_following_following_and_expired_list = random_following.following_and_expired
                if random_following_following_and_expired_list:
                    return random_following_following_and_expired_list[0]
                else:
                    tried_to_load_these_ids.append(random_following_id)

    ##############################################
    ##group related stuff
    ##############################################
    def top_groups(self, relationship="hybrid", significance_level=0, num_groups=0):
        from smarttypes.model.twitter_group import TwitterGroup
        
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
    
    def group_inferred_following(self, num_users, just_ids=True):
        from smarttypes.model.twitter_group import TwitterGroup
        user_score_map = {}
        for following_group_score, group_index in self.following_groups:
            for following_user_score, user_id in TwitterGroup.get_by_index(group_index).following:
                if user_id not in user_score_map:
                    user_score_map[user_id] = following_group_score * following_user_score
                else:
                    user_score_map[user_id] += following_group_score * following_user_score
        
        return_list = []
        score_user_list = [(y,x) for x,y in user_score_map.items()]
        for score, user_id in heapq.nlargest(num_users, score_user_list):
            add_this = user_id
            if not just_ids:
                add_this = TwitterUser.get_by_id(user_id)
            return_list.append(add_this)
        return return_list
        
    def who_to_follow(self, num_users):
        return_list = []
        for user_id in self.group_inferred_following(num_users):
            if user_id not in self.following_ids:
                return_list.append(TwitterUser.get_by_id(user_id))
        return return_list
    
    
    ##############################################
    ##state changing methods
    ##############################################    
    def save_following_ids(self, following_ids):
        self.following_ids = list(Set(following_ids))
        self.last_loaded_following_ids = datetime.now()
        self.save()    
        
    ##############################################
    ##class methods
    ##############################################    
    @classmethod
    def by_screen_name(cls, screen_name):
        result = cls.collection().find_one({'screen_name':screen_name})
        if result:
            return cls(**result)
        else:
            return None     
        
    @classmethod
    def upsert_from_api_user(cls, api_user):
        if api_user.protected == None:
            api_user.protected = False
        
        model_user = cls.get_by_id(api_user.id)
        if model_user:
            model_user.screen_name = mk_valid_ascii_str(api_user.screen_name)
            model_user.location_name = mk_valid_ascii_str(api_user.location)
            model_user.description = mk_valid_ascii_str(api_user.description)
            model_user.url = mk_valid_ascii_str(api_user.url)
            model_user.favourites_count = api_user.favourites_count
            model_user.protected = api_user.protected
            model_user.following_count = api_user.friends_count 
        else:
            properties = {
                'twitter_id':api_user.id,
                'screen_name':mk_valid_ascii_str(api_user.screen_name), 
                'twitter_account_created':api_user.created_at,
                'location_name':mk_valid_ascii_str(api_user.location), 
                'description':mk_valid_ascii_str(api_user.description), 
                'url':mk_valid_ascii_str(api_user.url), 
                'favourites_count':api_user.favourites_count,
                'protected':api_user.protected,
                'following_count':api_user.friends_count,
            }
            model_user = cls(**properties)
        model_user.save()
        return model_user
        


        
        
        
        