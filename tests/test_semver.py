from pipenv.vendor import semver

ver = semver.VersionInfo.parse('1.2.3-pre.2+build.4')
print(ver)
print(ver.major)
print(ver.minor)
print(ver.patch)
print(ver.prerelease)
print(ver.build)

print(semver.match("2.0.0", "==1.0.0"))
