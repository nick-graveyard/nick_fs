import kazoo
import zkDirectory
from zkDirectory import *
from kazoo.client import *
from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
from kazoo.recipe.watchers import ChildrenWatch
import logging

class zkDirClient:

    def __init__(self):


        #create a kazoo instance
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.zk.start()

        #create a zkDirectory node structure that will serve as a zookeeper cache(this is located in zkDirectory.py)
        self.localCache = zkDirectory()
        
        logging.basicConfig()
        print "Please Wait Loading File System"
        
        #populates zkDirectory datastructure with nodes from the remote Zookeeper directory
        print "Fetching Directory Structure"
        self.remoteRecursiveFetch("/")
        #sets watches on every node in Zookeeper remote directory
        "Registering Watches"
        self.remoteRecursiveWatch("/")

        print "File System Loaded"



    #ENFORCE READ ONLY METHODS FROM THE LOCAL CACHE. 
    #IF YOU NEED TO WRITE OR CHANGE ANYTHING--->WRITE TO ZOOKEEPER AND LET IT PROPOGATE TO LOCAL CACHE AUTOMATICALLY 
    #BECAUSE OF WATCHES.
`   #----------------------------------------------
    #gets everynode from the local cache
    def localGetAll(self):
        return self.localCache.getAll()
    #gets the children of the path from the Local Cache-not recursive returns only single level below the path
    def localGetChildrenOf(self, inPath):
        return self.localCache.getChildren(inPath) 
    #gets the children of the path recursively-returning EVERY child node beneath the path.
    def localRecursiveGetChildrenOf(self, inPath):
        return self.localCache.getRecursiveChildren(inPath)






    #THESE METHODS ARE ALL TO THE ZOOKEEPER SERVERS
    #DO ALL DATA MANIPULATION THROUGH HERE
    #--------------------------------------------
    #this makes a new directory on the remote zookeeper store WHICH is then propogated down to the local cache because of watches
    def remoteMakeDirectory(self, inPath):
        self.zk.create(inPath)
    #this deletes a directory on the remote zookeeper store WHICH is then mirrored to the localCache by watches
    #Note: need to figure out how to cancel watches!!! 
    #Keep getting no node error from the watches on the deleted directories
    def remoteDeleteDirectory(self, inPath):
        if(inPath == "/"):
            print "You can't delete the root directory fool! Dont even try it."
            return

        self.zk.delete(inPath ,recursive=True)
          
        """
        try:
            #get the children from zookeeper
            children = self.zk.get_children(inPath)

           

            for child in children: 
                childPath = inPath + "/" + child                
                self.remoteDeleteDirectory(childPath)
            

        except NoNodeError:
            #if no children return -base case 

            self.zk.delete(inPath)       
            return
        """         
    #recursively download [parameter:inPath] directory structure into self.localCache 
    #(i.e. the localCache of the zookeeper directory structure)
    def remoteRecursiveFetch(self, inPath):
        #get the node from zookeeper
        newData, newStat = self.zk.get(inPath)
        #create a new localnode
        newNode = localNode(inPath, newStat, newData)
        
        if(inPath != "/"):
            self.localCache.addNode(newNode)

        try:
            #get the children from zookeeper
            children = self.zk.get_children(inPath)

           

            for child in children: 

                 #take account of  the root directory because it's added again in child loop           
                if (inPath == "/"):
                    childPath="/" + child
                else:
                    childPath = inPath + "/" + child                 
                
                self.remoteRecursiveFetch(childPath)
            
        #if no children return -base case 
        except NoNodeError:                   
            return
    #sets a watch on every directory and subdirectory specified by the [parameter:inPath]
    def remoteRecursiveWatch(self,inPath="/"):
    
        #watch declaration according to kazoo. It's a decorator class that calls the class directly under it.
        #From here:
        #http://kazoo.readthedocs.org/en/latest/api/recipe/watchers.html#kazoo.recipe.watchers.ChildrenWatch

        @self.zk.ChildrenWatch(inPath)
        def my_func(children):
            self.watchHandler(inPath,children)



        try:
            #get the children from zookeeper
            children = self.zk.get_children(inPath)

            for child in children:                 
                 #account for the root directory because it's added again in child loop           
                if (inPath == "/"):
                    childPath="/" + child
                else:
                    childPath = inPath + "/" + child 

                self.remoteRecursiveWatch(childPath)

        except NoNodeError:
            #if no children return  -base case        
            return
    #this is the event handler for when a REMOTE node is changed. It will propogate the changes to the localCache.
    #it compares the localCache children with the remote zookeeper Children and adds or subtracts nodes as needed.
    def watchHandler(self, parentPath, children):

    
        #build the live children string- makes all paths absolute because thats all the localCache works with and they come into this
        #method as relative paths. so we add the parent path to each child then append eash to an list
        liveChildren = []
        for child in children:                 
            #account for the root directory because it's added again in child loop           
            if (parentPath == "/"):
                liveChildren.append("/" + child)
            else:
                 liveChildren.append(parentPath + "/" + child)

        print "live: " 
        print liveChildren

        #compares localCache with the remote zookeeper directory and subtracts nodes if theres a difference.
        cacheChildren = self.localCache.getChildren(parentPath)

        print "cache: " 
        print cacheChildren

        subtractions  = list(set(cacheChildren) - set(liveChildren))

        print "subs: " 
        print subtractions

        for child in subtractions:
            self.localCache.deleteNode(child)


        #compares the remote zookeeper with local zookeeper cache and gets any additions that have been made to the remote 
        #cache. It then recursively obtains that addition and any children beneath it.  Then it recursively sets 
        #watches on the addition and its children
        additions  = list(set(liveChildren) - set(cacheChildren))
        for child in additions:
            self.remoteRecursiveFetch(child)
            self.remoteRecursiveWatch(child)

        print parentPath + " cache changed"
        cacheChildren = self.localCache.getChildren(parentPath)





  
