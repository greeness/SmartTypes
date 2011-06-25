

class PostgresBaseModel(object):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def insert_sql_str(self):

        qry = """
        insert into %(table_name)s (%(table_columns)s)
        values (%(place_holder)s)
        returning id;
        """

        place_holder = ','.join(['%%(%s)s' % x for x in self.table_columns])
        
        params = {'table_name':self.table_name,
                  'table_columns':','.join(self.table_columns),
                  'place_holder':place_holder}
        
        return qry % params
    
    @property
    def update_sql_str(self):
        
        qry = """
        update %(table_name)s
        set %(place_holder)s
        where %(key_name)s = %(key_value)s
        returning id;
        """

        place_holder = ','.join(["%s = %%(%s)s" % (x,x) for x in self.table_columns])
        
        params = {'table_name':self.table_name,
                  'place_holder':place_holder,
                  'key_name':self.table_key,
                  'key_value':getattr(self, self.table_key, None)}
        
        return qry % params  
        
    
    def save(self):     
        key_value = getattr(self, self.table_key, None)

        if not key_value:
            qry = self.insert_sql_str        
        else:
            qry = self.update_sql_str

        params = {self.table_key:key_value}
        
        for prop_name in self.table_columns:            
            params[prop_name] = getattr(self, prop_name, None)
            
        results = self.postgres_handle.execute_query(qry, params, True)
        
        #set the key
        if not key_value:
            setattr(self, self.table_key, results[0][self.table_key])
            
        return self
    
    
    @classmethod
    def get(cls, key_value):
    
        qry = """
        select * 
        from %(table_name)s
        where %(key_name)s = %(key_value)s;
        """
        
        params = {'table_name':cls.table_name,
                         'key_name':cls.table_key,
                         'key_value':'%(key_value)s'}
        
        results = cls.postgres_handle.execute_query(qry % params, {'key_value':key_value})
        
        if len(results) == 1:
            
            return cls(**results[0])
        
        else:
            
            raise Exception('BaseModel.get did not return just one result.')
    
    