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
        if fname == None:
            self.forbidden()
        else:
            self._send_file( filespath + '/' + fname)

    def forbidden (self):
        abort(403,'')


    def _send_file(self, path):
        user_filename = '_'.join(filepath.split('/')[-2:])
        file_size = os.path.getsize(filepath)

        headers = [('Content-Disposition', 'attachment; filename=\"' + user_filename + '\"'),
                    ('Content-Type', 'text/plain'),
                    ('Content-Length', str(file_size))]

        from paste.fileapp import FileApp
        fapp = FileApp(filepath, headers=headers)

        return fapp(request.environ, self.start_response)
