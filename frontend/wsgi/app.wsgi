WORKING_ENV = "/home/dpetroff/code/python/fileshare/frontend"
APP_CONFIG = "/home/dpetroff/code/python/fileshare/frontend/development.ini"

import site
import os, sys
sys.path.append(WORKING_ENV)


from paste.script.util.logging_config import fileConfig
fileConfig(APP_CONFIG) 

from paste.deploy import loadapp
application = loadapp("config:" + APP_CONFIG)
