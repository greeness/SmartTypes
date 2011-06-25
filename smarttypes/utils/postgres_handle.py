#import psycopg2
from smarttypes.utils.sql_converters import sqlrepr


class PostgresHandle(object):
    
    def __init__(self, database_name):
        self.database_name = database_name
        self.conn_st = "host=localhost dbname='%s' user='timmyt' password='urllib2'" % self.database_name        
        
    @property
    def conn(self):        
        if '_conn' in self.__dict__:
            return self._conn
        else:
            self._conn = psycopg2.connect(self.conn_st)
            return self._conn

        
    def execute_query(self, query_string, params={}, return_results=True):
        
        cursor = self.conn.cursor()        
        sqlrepr_params = {}
        for key, value in params.items():
            sqlrepr_params[key] = sqlrepr(value)    
            
        cursor.execute(query_string % sqlrepr_params)        
        column_names = cursor.description 
        cursor_results = []
        if return_results:
            cursor_results = cursor.fetchall()
        cursor.close()

        #if results have two columns with the same name, for
        #example you join two tables that both have id columns
        #this thang will raise an Exception
        if cursor_results:
            if len(column_names) != len(cursor_results[0]):
                raise Exception("PostgresHandle.execute_query has some dup column names in the select clause.")
         
        rows = []        
        for cursor_result in cursor_results:
            row = {}
            for i in range(len_column_names):
                name = column_names[i][0]
                value = cursor_result[i]
                row[name] = value
            rows.append(row)
            
        return rows
    
    

        