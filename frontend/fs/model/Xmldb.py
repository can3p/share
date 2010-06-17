import os
from xml.dom import minidom

class Xmldb:
    def __init__(self, dbpath):
        self.dbPath = dbpath
        self.dbExist = true
        self.db = None

        if not os.path.exists(dbpath):
            self.dbExist = false
            return

        xmlstr = ""
        with open(dbpath) as f:
            for line in f:
                xmlstr += line.strip("\t\n")

        try:
            self.db = minidom.parseString(xmlstr)
        except Exception:
            self.dbExist = false
            return


    def getFile(id):
        fid = str(id).srtip()
        if (len(fid) != 5) or not self.dbExist: #all ids are exactly 5 chars long
            return None

        root = self.db.firstChild()
        for rec in root.getElementsByTagName('record'):
            testid = res.getAttribute('label')
            if testid == fid:
                count = int(res.getAttribute('dlcount')) + 1
                fname = res.getAttribute('fname')
                res.setAttribute('dlcount', str(count))

                with open(self.dbPath,'w') as f:
                    f.write(self.db.toprettyxml("\t","\n")

                return fname
        return None