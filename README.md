#Bee

**bee** is an all-in-one python framework for simplifying program development.

## Components

* **Config** - Manage configuration for yml, yaml & json
* **RPC** - Lightweight and high performace
    * Serializable
        * ProtoBuf
        * json
        * http to be continued
    * Service Discovery - Automatic registration and name resolution with service discovery
        * etcd3
        * consul
    * Load Balancing - Smart client side load balancing of services built on discovery
        * RandomBalancer
        * RoundRobbinBalancer

* **Web** - Web server with a variety of advanced features, to be continued
* **Database**
    * Psd - A lightweight, fluent SQL data access and ORM library
    * MongoDB - A powerful wrapper for [mongo](https://pypi.org/project/pymongo)
    * Redis - A powerful wrapper for [redis](https://pypi.org/project/redis),[redis-py-cluster](https://pypi.org/project/redis-py-cluster)
* **Utility** - Some useful utility packages..
    * debug
    * i18n
    * guid
    * const
    * map
    * objectpool
    
