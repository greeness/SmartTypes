
import logging

class LogHandle(object):
    
    def __init__(self, filepath):
        logging.basicConfig(
            filename=filepath,
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s')
        
    def log(self, msg):
        logging.log(logging.INFO, msg)




