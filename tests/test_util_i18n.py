from bee.util.i18n import new

all = new("./samples").all()
print(all.get("zh").format("title", "郝文超"))
print(all.get("en").format("title", "awen"))