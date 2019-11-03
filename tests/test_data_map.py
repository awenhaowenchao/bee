from bee.data.map import Map

m1 = Map(('a', 'b', 'c'), (1, 2, 3))

print(m1.keys())
print(m1.values())
print(m1.items())
print(hasattr(m1, 'a'))
print(m1.contains('a'))

# m1.remove("a")

delattr(m1, "a")
print(m1.keys())
m1.empty()
print(m1.values())

# print(m1.get(1))

m2 = Map(a=1, b=2)

print(m2)

# m3 = Map({"a" : 1})
#
# print(m3)
