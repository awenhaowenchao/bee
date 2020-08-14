# from bee.db.mongo import *
from bee import MongoFactory
factory = MongoFactory()
client = factory.open("theater")
result = client.coll("cinema").find_one({"_id" : 10000})
print(result)