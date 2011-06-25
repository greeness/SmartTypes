from exceptions import RedirectException

def mongo_web_decorator():
    def wrapper0(controller):
        def wrapper1(request, mongo_handle):
            
            try: 
                web_response = controller(request)
                response_headers = web_response.get_response_headers()
                response_string = web_response.get_response_str(controller.__name__)
                #if getattr(mongo_handle, '_conn', False):
                    #mongo_handle.conn.commit()
                status_code = '200 OK'
                
            except RedirectException, (redirect_ex):                
                #if getattr(mongo_handle, '_conn', False):
                    #mongo_handle.conn.commit()
                status_code = '303 See Other'
                response_headers = [('Location', redirect_ex.redirect_url)]
                response_string = [""]
                
            except:
                #if getattr(mongo_handle, '_conn', False):
                    #mongo_handle.conn.rollback()
                raise
            
            finally:
                s = ""
                #if getattr(mongo_handle, '_conn', False):
                    #mongo_handle.conn.close() 
            
            #send it all back
            return (status_code, response_headers, response_string) 
        return wrapper1
    return wrapper0