
"""
Data structure for a local cache of zookeeper Nodes.
This requires python earlier than 3 b/c of the getAll method(easy enough to fix at a later date)

localNode is an replica of a single zookeeper node, with stat,data,and childNode fields.

zkDirectory class is a mirror of a remote zookeeper store.
It functions fully with absolute paths.
This allows both a hashtable and tree data structure to operate inside of it in tandem.

This gives you speed of a hash table lookup with the directory heirarchy of a tree.

When you add a node its path is added absolutely to the hashtable.
/test : localNode
/test/2 : localNode
/test/3 : localNode
.....

Also the parent of the node being added to the hashtable is found and this child is added to the parents list of child nodes.
This gives a binary tree structure as well. 


Note: 
The only functions that return actual Node object is getNode.
Everyother function returns a string.
"""
import copy
from copy import copy



#replica of the Node object in zookeeper.  What the local zkDirectory class is made out of.
class localNode:
    def __init__(self,inPath, inStat=None, inData=None):        
        self.path=inPath
        self.stat=inStat
        self.data=inData
        self.childNodes = [] #note: add Nodes here or add strings here?
    




class zkDirectory:
    def __init__(self):
        root = localNode("/",None,None)
        self.theDirectory = {"/": root}

    def addNode(self, inNode):
        #passing in a localNode object and you get the path from inside of it
        inPath = inNode.path

        #requires a parent directory to be able to add the new node
        parentPath = self.getParent(inPath)
        if(parentPath not in self.theDirectory):
            print "No parent directory exists to add node"
            return

        #add to hashtable
        self.theDirectory[inPath] = inNode

        #append this path to the parents 'childNodes' object      
        self.theDirectory[parentPath].childNodes.append(inPath)

        #recursively deletes a node and everything under it
    def deleteNode(self, inPath):

        try:

            deleteChildren = self.theDirectory[inPath].childNodes
      
        except NoNodeError:
            #if no children return -base case 
                #delete from parent 
            parentPath = self.getParent(inPath)            
            self.theDirectory[parentPath].childNodes.remove(inPath)
            #del from directory list
            del self.theDirectory[inPath]        
            return


        #recursively iterate throuth all the children
        for child in deleteChildren:
            self.deleteNode(child)

       
        
        #delete from parent 
        parentPath = self.getParent(inPath)            
        self.theDirectory[parentPath].childNodes.remove(inPath)
        #del from directory list
        del self.theDirectory[inPath]


   

    #returns a Node object
    def getNode(self, inPath):
        return self.theDirectory[inPath] 
    #returns list of strings
    def getChildren(self, inPath):
        return self.theDirectory[inPath].childNodes
    #returns a string(the parent)
    def getParent(self, inPath):
        #can call one of the alternative implementations for getParent below
        return self.getParentDir_split(inPath)
    #returns list of strings
    def getAll(self):
        return self.theDirectory.keys()

   


    #Ignore this: Alternative implementations for speed trials and optimization at future date
    #---------------------------------------------------------------------------

    #hash table implelmentation of getNode-to be implemented
    def getNode_HashTable(self, inPath):
        pass
    #tree search implementation of getNode-to be implemented
    def getNode_TreeSearch(self, inPath):
        pass
    #regular expression implementation of getParentDir-to be implemented
    def getParentDir_regEx(self, inPath):
        pass
        #pattern = [^\\]+\\?$
        #return re.match(pattern, inPath)
        #string manipulation implementation of getParentDir

    def getParentDir_split(self, inPath):
        #remove the last character in case it's a forward slash: /
        inPath = inPath[:-1]
        #split up directory structure
        x = inPath.split("/")

        #return a "/" (slash) for anything like: / or /a 
        if(len(x) <= 2):
            return "/"

        #trim off the last path
        trimSize = len( x[len(x)-1]   ) + 1
        return inPath[:-trimSize]


#testing
if __name__ == '__main__':
    z = zkDirectory()
    z.addNode( localNode("/b") )
    z.addNode( localNode("/c") )
    z.addNode( localNode("/b/a") )
    z.addNode( localNode("/b/c") )
    z.addNode( localNode("/c/a") )
    z.addNode( localNode("/c/c") )
    print z.getAll()
    z.deleteNode("/c/a")
    print z.getAll()
    z.deleteNode("/c")
    print z.getAll()


