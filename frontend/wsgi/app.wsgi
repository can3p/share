import site
import os, sys

frontEndDir = os.path.dirname( os.path.abspath ( os.path.dirname( __file__ )))

WORKING_ENV = frontEndDir
APP_CONFIG = os.path.join( WORKING_ENV, "development.ini" )

sys.path.append(WORKING_ENV)

from paste.script.util.logging_config import fileConfig
fileConfig(APP_CONFIG) 

from paste.deploy import loadapp
application = loadapp("config:" + APP_CONFIG)
