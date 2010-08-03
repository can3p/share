from xml.dom import minidom
import time
import math
import os
import random
import hashlib

class Xmldb:
    "class to store database information in xml file"

    def __init__(self, fname):
        self.fname = fname
        if not os.path.exists(fname):
            #create document root
            xmlstr = u"<files></files>"
        else:
            #the hack is needed because minidom adds extra whitespaces in file
            xmlstr = ""
            with open(fname,"r") as f:
                for line in f:
                    xmlstr += line.strip("\t\n")

        try:
            self.doc = minidom.parseString(xmlstr)
        except Exception:
            print("found empty xmldb, creating new one")
            self.doc = minidom.parseString(u"<files></files>")

        self.root = self.doc.firstChild

    def close(self):
        with open(self.fname, "w") as f:
            f.write(self.doc.toprettyxml("\t", "\n"))

    def getMaxID(self):
        root_max_id = self.root.getAttribute('maxid')
        if(root_max_id):
            new_id = int(root_max_id)
        else:
            new_id = len(self.doc.getElementsByTagName("record"))
        
        return new_id


    def setMaxID(self, new_id):
        self.root.setAttribute(u'maxid', str(new_id))

    def generateLabel(self):
        timestamp = math.floor(time.time())

        #we suggest that this method always generate unique values
        return hashlib.md5(str(timestamp*random.random())).hexdigest()[-5:]

    def addRecord(self, label, fname, files):
        new_id = self.getMaxID() + 1
        self.setMaxID(new_id)

        timestamp = math.floor(time.time())

        #generate node for new record
        new_node = self.doc.createElement(u"record")
        new_node.setAttribute(u'id', str(new_id))
        new_node.setAttribute(u'date', str(int(timestamp)))
        new_node.setAttribute(u'label', label)
        new_node.setAttribute(u'dlcount', '0')
        new_node.setAttribute(u'fname', fname.decode("utf-8"))

        for fname in files:
            fnode = self.doc.createElement(u"file")
            fnode.setAttribute(u"name", os.path.basename(fname).decode("utf-8"))
            fnode.setAttribute(u"origpath", os.path.dirname(fname).decode("utf-8"))
            new_node.appendChild(fnode)
        
        self.root.appendChild(new_node)

    def delRecord(self, id):
        nodes = self.root.getElementsByTagName('record')

        for el in nodes:
            if(el.getAttribute('id') == id):
                self.root.removeChild(el)
                return

    def delAllRecords(self):
        nodes = self.root.getElementsByTagName('record')

        for el in nodes:
            self.removeChild(el)

    def getRecordsList(self):
        "return dictionary with records"
        res = {}

        for el in self.root.getElementsByTagName("record"):
            id = el.getAttribute("id")

            res[ id ] = {
                    "id" : id,
                    "label" : el.getAttribute("label"),
                    "downloadNum": el.getAttribute("dlcount"),
                    "files": [ fel.getAttribute('origpath') + fel.getAttribute("name") for fel in el.getElementsByTagName("file") ]
            }

        return res

    def getFile(self, id):
        #log.debug("searching for id = %s" % id)
        fid = str(id).strip()
        if (len(fid) != 5): #all ids are exactly 5 chars long
            return None

        for rec in self.root.getElementsByTagName('record'):
            testid = rec.getAttribute('label')
            #log.debug("testid = %s" % testid)
            if testid == fid:
                count = int(rec.getAttribute('dlcount')) + 1
                fname = rec.getAttribute('fname')
                rec.setAttribute('dlcount', str(count))

                return fname
        return None
