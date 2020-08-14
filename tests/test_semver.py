from pipenv.vendor import semver

ver = semver.VersionInfo.parse('1.2.3-pre.2+build.4')
print(ver)
print(ver.major)    #主版本号，做了向下不兼容的功能性修正
print(ver.minor)    #次版本号，做了向下兼容的功能性新增
print(ver.patch)    #修订号|修订号，做了向下兼容的问题修正
print(ver.prerelease)
print(ver.build)

print(semver.match("2.0.0", "==1.0.0"))
