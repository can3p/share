class Xmldb:
    def __init__(self):
        from pylons import config

        self.xmldb = config['xmldb_dir']
