from bee.db.redis import  RedisFactory

redis_factory = RedisFactory()
client = redis_factory.open("test_single")

result = client.reader().keys("APP_LOGIN_2906*")
print(result)

cluster_client = redis_factory.open("test_cluster")

result1 = cluster_client.reader().get("h")

print(result1)

sentinel_client = redis_factory.open("test_sentinel")

sentinel_client.writer().set("title", "test_sentinel")

result2 = sentinel_client.reader().keys("*")
for x in result2:
    print(sentinel_client.reader().get(x))
