
from pymongo import Connection


class MongoHandle(object):

    """
    creates a connection when needed and then stores it for future reference
    
    connection_string format see: http://www.mongodb.org/display/DOCS/Connections
    """
    
    def __init__(self, connection_string, database_name):
        self.connection_string = connection_string
        self.database_name = database_name
    
    _connection = None
    @property
    def connection(self):
        if self._connection == None: 
            self._connection = Connection(host=self.connection_string, tz_aware=False)
        return self._connection
        
    @property
    def database(self):
        return self.connection[self.database_name]
    
    
    
    