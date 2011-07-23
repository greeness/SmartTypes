
import logging

class LogHandle(object):
    
    base_dir = "/home/timmyt/projects/smarttypes/smarttypes/logs/"
    
    def __init__(self, filepath):
        logging.basicConfig(
            filename=self.base_dir+filepath,
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s')
        
    def log(self, msg):
        logging.log(logging.INFO, msg)




