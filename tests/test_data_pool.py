from bee.data.pool import ObjectPool


class Test():

    def hello(self):
        print("hello world")

object_pool = ObjectPool(Test)

with object_pool.new() as obj:
    obj.hello()

with object_pool.new() as obj:
    obj.hello()

with object_pool.new() as obj:
    obj.hello()

with object_pool.new() as obj:
    obj.hello()

with object_pool.new() as obj:
    obj.hello()

with object_pool.new() as obj:
    obj.hello()



def hello():
    print("hello world 1")

object_pool = ObjectPool(hello)
with object_pool.new() as obj:
    obj