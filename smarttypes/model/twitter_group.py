from smarttypes.model.mongo_base_model import MongoBaseModel
from datetime import datetime, timedelta
from smarttypes.utils import time_utils
import re, string, heapq, random, collections, numpy
#from smarttypes.utils.log_handle import LogHandle
#log_handle = LogHandle('twitter_group.log')

class TwitterGroup(MongoBaseModel):
        
    collection_name = 'twitter_groups'
    primary_key_name = 'group_index'
    properties = {
        'group_index':{'ok_types':[int]},
        'scores_users':{'ok_types':[list]}, #list of tups: (score, id)
        'tag_cloud':{'ok_types':[list]}, #list of tups: (score, word)
    }        
    
    
    def tag_cloud_display(self):
        return ' '.join([x[1] for x in self.tag_cloud])
    
    def top_users(self, num_users=20, just_ids=False):
        from smarttypes.model.twitter_user import TwitterUser
        
        return_list = []
        i = 0
        for score, user_id in sorted(self.scores_users, reverse=True):
            if i <= num_users and score > .001:
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
    def get_all_groups(cls, count=False):
        results = cls.collection().find()
        if count:
            return results.count()
        else:
            return_list = []
            for result in results:
                return_list.append(cls(**result))
            return return_list
    
    @classmethod
    def get_active_groups(cls, count=False):
        results = cls.collection().find({'scores_users':{'$ne':[]}})
        if count:
            return results.count()
        else:
            return_list = []
            for result in results:
                return_list.append(cls(**result))
            return return_list        
        
        
    @classmethod
    def get_by_index(cls, group_index):
        return cls(**cls.collection().find_one({'group_index':group_index}))
    
    @classmethod
    def get_random_group(cls):
        num_groups = cls.get_all_groups(count=True)
        random_index = random.randrange(0, num_groups) 
        random_group = cls.get_by_index(random_index)
        if random_group.scores_users:
            return random_group
        else:
            return cls.get_random_group()
    
    @classmethod
    def upsert_group(cls, group_index, scores_users, scores_groups):
        properties = {
            'group_index': group_index,
            'scores_users':scores_users,
            'scores_groups':scores_groups,
        }
        twitter_group = cls(**properties)
        twitter_group.save()

    @classmethod
    def mk_tag_clouds(cls):
        
        print "starting group_wordcounts loop"
        group_wordcounts = {} #{group_index:{word:count}}
        all_words = set()
        for group in cls.get_active_groups():
            group_wordcounts[group.group_index] = (group, collections.defaultdict(int))
            for score, user in group.top_users(num_users=20):
                if not user.description:
                    continue
                regex = re.compile(r'[%s\s]+' % re.escape(string.punctuation))
                for word in regex.split(user.description.strip()):
                    word = string.lower(word)
                    if len(word) > 2:
                        all_words.add(word)
                        group_wordcounts[group.group_index][1][word] += 1
                        
        print "starting avg_wordcounts loop"            
        avg_wordcounts = {} #{word:avg}
        for word in all_words:
            group_usage = []
            for group_index in group_wordcounts:
                group_usage.append(group_wordcounts[group_index][1][word])
            avg_wordcounts[word] = numpy.average(group_usage)
                
        print "starting groups_unique_words loop"
        groups_unique_words = {} #{group_index:[(score, word)]}
        for group_index in group_wordcounts:
            groups_unique_words[group_index] = []
            for word, times_used in group_wordcounts[group_index][1].items():
                usage_diff = times_used - avg_wordcounts[word]
                groups_unique_words[group_index].append((usage_diff, word))
        
        print "starting save tag_cloud loop"
        for group_index, unique_scores in groups_unique_words.items():
            group = group_wordcounts[group_index][0]
            group.tag_cloud = heapq.nlargest(10, unique_scores)
            group.save()
        
        return "All done!"

                
            
            
        