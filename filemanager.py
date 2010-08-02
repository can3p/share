from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import os

class FileManager:
    @staticmethod
    def getDirContents(path):
        if(os.path.isdir(path)):
            lst = os.listdir(path)
            lst = [ path + '/' + el for el in lst ]
            subdirs = []
            for l in lst:
                if( os.path.isdir(l) ):
                    subdirs.extend(FileManager.getDirContents(l))
            lst.extend(subdirs)
            return lst

        return []


    @staticmethod
    def createZipArchive(name, files):
        lst = []
        archive = ZipFile(name, "w", ZIP_DEFLATED)
        for fname in files:
            base = os.path.basename(fname)
            baseDir = os.path.dirname(fname)

            lst.append(os.path.basename(fname))
            archive.write(fname, os.path.basename(fname))
            if(os.path.isdir(fname)):
                for ff in FileManager.getDirContents(fname):
                    lst.append(ff.replace(baseDir, ''))
                    archive.write(ff, os.path.basename(ff))
        archive.close()
        return lst
