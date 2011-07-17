from datetime import datetime


class MongoBaseModel(object):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        
    def to_dict(self):
        """
        validation before a save        
        """
        
        return_dict = {'last_modified':datetime.now()}
        self.last_modified = return_dict['last_modified']
            
        #primary key
        if getattr(self, 'primary_key_name', None):
            if type(None) in self.properties[self.primary_key_name]['ok_types']:
                raise Exception('BaseModel error: primary_key cant allow NoneType.')
            return_dict['_id'] = getattr(self, self.primary_key_name)
            self._id = return_dict['_id']
        
        #check types, maybe a default
        for property_name, options_dict in self.properties.items():
            
            property_value = getattr(self, property_name, None)
            
            #maybe a default
            if property_value == None and 'default' in options_dict:
                property_value = options_dict['default']
                setattr(self, property_name, property_value)
                
            property_type = type(property_value)        
            
            #the right type
            if property_type not in options_dict['ok_types']:
                raise Exception("BaseModel error: %s cant be type %s." % (property_name, property_type))
            
            return_dict[property_name] = property_value
            
        return return_dict
    
        
    def save(self):
        self.collection().save(self.to_dict(), safe=True)
        
    
    @classmethod
    def collection(cls):
        return cls.mongo_handle.database[cls.collection_name]
    
        
    @classmethod
    def get_by_id(cls, id):
        result = cls.collection().find_one({'_id':id})
        if result:
            return cls(**result)
        else:
            return None
    
        
    @classmethod
    def get_by_ids(cls, ids):
        return_list = []
        for result in cls.collection().find({'_id':{'$in':ids}}):
            return_list.append(cls(**result))
        return return_list

    
    @classmethod
    def recently_altered(cls, altered_datetime, just_count=True):
        results = cls.collection().find(
            {'last_modified':{'$gte': altered_datetime}}
        )
        if just_count: 
            return results.count()
        else:
            for result in results:
                return_list.append(cls(**result))
            return return_list
    
    
    @classmethod
    def get_by_has_or_dont_have_attr(cls, attr_name, has_or_dont_have, just_count=False):
        return_list = []
        results = cls.collection().find({attr_name:{'$exists': has_or_dont_have}})
        if just_count: 
            return results.count()
        else:
            for result in results:
                return_list.append(cls(**result))
            return return_list

    
    @classmethod
    def delete_attr(cls, ids, attr_name):
        if ids == 'all':
            cls.collection().update({}, {'$unset':{attr_name:1}}, upsert=False, multi=True)
        else:
            cls.collection().update({'_id':{'$in':ids}}, {'$unset':{attr_name:1}}, upsert=False, multi=True)
            
    
    @classmethod
    def bulk_update(cls, ids, name_value_dict):
        if ids == 'all':
            cls.collection().update({}, {'$set':name_value_dict}, upsert=False, multi=True)
        else:
            cls.collection().update({'_id':{'$in':ids}}, {'$set':name_value_dict}, upsert=False, multi=True)
            
            
    @classmethod
    def bulk_delete(cls, ids, safe=True):
        if ids == 'all':
            cls.collection().remove({}, safe=safe) 
        else:
            cls.collection().remove({'_id':{'$in':ids}}, safe=safe) 
            
      
            
            
            