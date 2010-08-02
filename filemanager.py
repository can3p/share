from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import os

class FileManager:
    @staticmethod
    def getDirContents(path):
        if(os.isdir(path)):
            lst = os.listdir(path)
            subdirs = []
            for l in lst:
                if( os.isdir(path  + "/" + l) ):
                    subdirs.extend(get_dir_contents(path + "/" + l))
            return subdirs

        return []


    @staticmethod
    def createZipArchive(name, files):
        lst = []
        archive = ZipFile(name, "w", ZIP_DEFLATED)
        for fname in files:
            lst.push(fname)
            archive.write(fname, os.path.basename(fname))
            if(os.isdir(fname)):
                for ff in FileManager.getDirContents(fname):
                    lst.push(ff)
                    archive.write(ff, os.path.basename(ff))
        archive.close()
        return lst
