import psycopg2
from smarttypes.utils.sql_converters import sqlrepr


class PostgresHandle(object):
    
    def __init__(self, connection_string):
        self.connection_string = connection_string      
        
    @property
    def connection(self):        
        if not '_connection' in self.__dict__:
            self._connection = psycopg2.connect(self.connection_string)
        return self._connection

    
        
    def execute_query(self, query_string, params=None, return_results=True, print_qry=False):
        cursor = self.connection.cursor()
        params = params if params else {}
        #sqlrepr_params = {}
        #for key, value in params.items():
            #sqlrepr_params[key] = sqlrepr(value)
        #query_string = query_string % sqlrepr_params
        
        cursor.execute(query_string, params)        
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
            for i in range(len(column_names)):
                name = column_names[i][0]
                value = cursor_result[i]
                row[name] = value
            rows.append(row)
            
        return rows
    
    

        