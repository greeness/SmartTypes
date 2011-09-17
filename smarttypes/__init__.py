"""
====================
Modules
====================

Modules are stored in a global dict, and loaded from the top down. 

Module (x) may load another module (y)

If y then loads x (a cross-reference) it will only have the 
parts of x that were loaded when itself (y) was called by x



====================
This app
====================

mod_wsgi loads wsgi.py 

wsgi.py imports this, which should import everything else
"""

import utils
import model
import controllers
from config import DB_USER, DB_PASSWORD

site_name = 'SmartTypes'
site_mantra = 'a tool for social discovery'
default_title = '%s - %s' % (site_name, site_mantra)
site_description = """
Find, follow, and learn from niche community leaders.
SmartTypes is a tool for social exploration and discovery. Enjoy!! 
"""
site_description = site_description.strip()

connection_string = "host=localhost dbname='smarttypes' user='%s' password='%s'" % (DB_USER, DB_PASSWORD)

#connection_string = "mongodb://localhost"
#database_name = "smarttypes"





