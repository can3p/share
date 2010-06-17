import site
#site.addsitedir('/opt/pylonsdev/lib/python2.6')
#site.addsitedir('/opt/pylonsdev/lib/python2.6/site-packages')

import os, sys


WORKING_ENV = "/home/dpetroff/code/python/fileshare/frontend"
APP_CONFIG = "/home/dpetroff/code/python/fileshare/frontend/development.ini"

sys.path.append(WORKING_ENV)

from paste.deploy import loadapp
application = loadapp("config:" + APP_CONFIG)
