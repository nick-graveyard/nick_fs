nickFS
======

This was the beginning of a distributed file system using Fusepy, Zookeeper, and Kazoo.


https://code.google.com/p/fusepy/ <br/>
http://zookeeper.apache.org/  <br/>
http://kazoo.readthedocs.org/en/latest/  <br/>


The idea was to have all of the file system meta-data stored in permanant zookeeper znodes and all 
of the file system data broken up into chunks and stored on dumb chunk servers.
The hashed value of the data is stored in the zookeeper meta-data for retrieval.

The chunk servers register ephemeral nodes with zookeeper as they come and go from the distributed file system. 

The client simply connects to zookeeper and caches all of the emphemeral nodes and the file system meta-data
and registers watches on the zookeeper system for any changes to these. 

Therefore, any changes are propogated to all of the clients.


The Zookeeper server is acting as a Master server and provides failover due to the ability to add 
numerous zookeeper servers to the zookeeper cluster.


There are some neat Kazoo/ZK utilities I made like the recursive caching functionality. 
And recursive watch registration functionality.

