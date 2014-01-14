#!/usr/bin/env python

from sys import argv, exit
from time import time


import zkDirClient
from zkDirClient import *

#from paramiko import SSHClient

from fuse import FUSE, Operations, LoggingMixIn,FuseOSError
from stat import S_IFDIR, S_IFLNK, S_IFREG



from errno import ENOENT

class nickFs(LoggingMixIn, Operations):


    def __init__(self):

        #this is the wrapped full zookeeper cache client
        self.zkCacheClient =  zkDirClient()


        #self.files = {}
        #self.files['/'] = dict(st_mode=(S_IFDIR | 0755), st_nlink=2)

    
    

    #simple return a string list of subdirectories.
    def readdir(self, path, fh):
        print "called readdir " + " path: " + path 

        #print self.zkCacheClient.localGetChildrenOf(path)  + [".", ".."]
        
        return self.zkCacheClient.localGetChildrenOf(path)  + [".", ".."]
          

    def getattr(self, path, fh=None):        
        print "called getattr " + " path: " + path
    
        #if path not in self.zkCacheClient.localGetChildrenOf(path):
        #    raise FuseOSError(ENOENT)

        
        now = time()
        return dict(st_mode=(S_IFDIR | 0777), 
                    st_ino = 0,
                    st_dev = 0,
                    st_uid =0,
                    st_gid =0,
                    st_ctime=now,
                    st_mtime=now, 
                    st_atime=now, 
                    st_nlink=2,
                    st_size = 4096)   


    def mkdir(self, path, mode):
        print "mkdir"
        self.zkCacheClient.remoteMakeDirectory(path)



    def rmdir(self, path):
        print "rmdir"
        self.zkCacheClient.remoteDeleteDirectory(path)


    """
    def chmod(self, path, mode):
        #return self.sftp.chmod(path, mode)
        print "chmod"

    def chown(self, path, uid, gid):
        #return self.sftp.chown(path, uid, gid)
        print "chmod"

    def create(self, path, mode):
    
        print "create"

    def destroy(self, path):
     
        print "destroy"   

    def read(self, path, size, offset, fh):
     
        print "read"

    def readlink(self, path):
        print "readlink"

    def rename(self, old, new):
        print "rename"

  

    def symlink(self, target, source):
        print "symlink"

    def truncate(self, path, length, fh=None):
        print "truncate"

    def unlink(self, path):
        print "unlink"

    def utimens(self, path, times=None):
        print "utimens"

    def write(self, path, data, offset, fh):
        print "write"
    """


if __name__ == '__main__':
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    fuse = FUSE(nickFs(), argv[1], foreground=True, nothreads=True)


    if argv[2] == True:
        
        from kazoo.client import KazooClient
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.start()

        self.zkCacheClient.remoteMakeDirectory("/metaData")
        self.zkCacheClient.remoteMakeDirectory("/chunkData")

