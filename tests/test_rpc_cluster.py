from bee.net.rpc.client import Cluster

cluster = Cluster()
client = cluster.get_client("test")
# result = client.call(service="Test", method="hello", args=["awen"])
# print("result=" + str(result.value))
# result = client.call(service="Test", method="hello", args=["zhangsan"])
# print("result=" + str(result.value))
# result = client.call(service="Test", method="hello", args=["lizi"])
# print("result=" + str(result.value))
# result = client.call(service="Test", method="hello", args=["wangwu"])
# print("result=" + str(result.value))

result = client.call(service="Test", method="test", args=[])
print("result=" + str(result.value))

