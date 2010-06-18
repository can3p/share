import os
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fs.lib.base import BaseController, render
from fs.model.Xmldb import Xmldb

log = logging.getLogger(__name__)

class IndexController(BaseController):

    def index(self, id):
        from pylons import config

        filespath = config['files_dir']
        db = Xmldb(config['xmldb_path'])
        fname = db.getFile(id)
        if fname == None:
            self.forbidden()
        else:
            log.debug("fname =  %s", fname)
            filepath = u"%s/%s/%s" % (filespath, id, fname)
            return self._send_file( filepath)


    def forbidden (self):
        abort(403,'')


    def _send_file(self, path):
        user_filename = os.path.basename(path) 
        file_size = os.path.getsize(path.encode("utf-8"))

        import mimetypes
        mtype = mimetypes.guess_type(path)[0]
        if mtype == None:
            mtype = 'text/plain'

        headers = [
                ('Content-Disposition', 'attachment; filename=\"%s\"' % user_filename.encode("utf-8")),
                ('Content-Type', mtype),
                ('Content-Length', str(file_size))
                ]

        from paste.fileapp import FileApp
        fapp = FileApp(path.encode("utf-8"), headers=headers)

        return fapp(request.environ, self.start_response)

