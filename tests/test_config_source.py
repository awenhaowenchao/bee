from bee.config.source import ByteDataSource, FileSource

# m = DataSource(d=b'{"name" : "awen"}', t="json").load()
m = ByteDataSource(d=b'name: awen', t="yml").load()
print(m)

fs = FileSource("./samples/app.yml")
opts = fs.load()
print(opts)
