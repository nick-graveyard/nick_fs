#!/usr/bin/env python

import zkDirClient
from zkDirClient import *

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn






from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time


class nickFs(LoggingMixIn,Operations):
    'Example memory filesystem. Supports only one level of files.'

    def __init__(self):
      #zookeeperDirectory =  zkDirClient()
      pass



    def chmod(self, path, mode):
        print path + " " + "chmod"
       

    def chown(self, path, uid, gid):
        print path + " " + "chown"
       

    def create(self, path, mode):
        print path + " " + "create"
      
  

    def getattr(self, path, fh=None):
        print path + " " + "getattr"
  

    def getxattr(self, path, name, position=0):
        print path + " " + "getXattr"


    def listxattr(self, path):
        print path + " " + "listXattr"
     
    def mkdir(self, path, mode):
        print path + " " + "mkdir"
      

    def open(self, path, flags):
        print path + " " + "open"
        

    def read(self, path, size, offset, fh):
        print path + " " + "read"

    def readdir(self, path, fh):
        print path + " " + "readdir"

    def readlink(self, path):
        print path + " " + "readlink"

    def removexattr(self, path, name):
        print path + " " + "removexattr"

    def rename(self, old, new):
        print path + " " + "rename"

    def rmdir(self, path):
        print path + " " + "rmdir"

    def setxattr(self, path, name, value, options, position=0):
        print path + " " + "sexXattr"
 
    """
    def statfs(self, path):
        print path + " " + "statfs"
    """
    def symlink(self, target, source):
        print path + " " + "symlink"

    def truncate(self, path, length, fh=None):
        print path + " " + "truncate"
  
    def unlink(self, path):
        print path + " " + "unlink"
   
    def utimens(self, path, times=None):
        print path + " " + "utimens"
     
    def write(self, path, data, offset, fh):
        print path + " " + "write"
 


if __name__ == '__main__':
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    #logging.getLogger().setLevel(logging.DEBUG)
    fuse = FUSE(nickFs(), argv[1], foreground=True)
