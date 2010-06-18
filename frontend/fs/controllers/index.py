import os
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fs.lib.base import BaseController, render
from fs.model.Xmldb import Xmldb

log = logging.getLogger(__name__)

class IndexController(BaseController):

    def index(self, id):
        # Return a rendered template
        #return render('/index.mako')
        # or, return a string
        from pylons import config

        filespath = config['files_dir']
        db = Xmldb(config['xmldb_path'])
        fname = db.getFile(id)
        log.info("1")
        log.debug("1")
        log.debug("1")
        log.debug("1")
        if fname == None:
            self.forbidden()
        else:
            log.debug("fname =  %s", fname)
            return self._send_file( filespath + '/' + id + '/' + fname)


    def forbidden (self):
        abort(403,'')


    def _send_file(self, path):
        user_filename = os.path.basename(path) 
        file_size = os.path.getsize(path)

        import mimetypes
        mtype = mimetypes.guess_type(path)[0]
        if mtype == None:
            mtype = 'text/plain'

        headers = [
                ('Content-Disposition', 'attachment; filename=\"' + str(user_filename) + '\"'),
                ('Content-Type', mtype),
                ('Content-Length', str(file_size))
                ]

        from paste.fileapp import FileApp
        fapp = FileApp(path, headers=headers)

        return fapp(request.environ, self.start_response)

