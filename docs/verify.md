# Verify Sources

Prior to adding source tarballs into this repository, they must be verified
with known checksums.  If a cryptographic (GPG) signature is available, then
it must be used.  Below are instructions for verifying some of Hootenanny's
dependencies from upstream sources.

## GLPK

GLPK is [maintained by Andrew Makhorin](https://www.gnu.org/software/glpk/glpk.html#maintainer)
and the tarball may be verified with his key:

```
pushd SOURCES
gpg --keyserver keys.gnupg.net --recv-keys D17BF2305981E818
curl -O https://ftp.gnu.org/gnu/glpk/glpk-$GLPK_VERSION.tar.gz
curl -O https://ftp.gnu.org/gnu/glpk/glpk-$GLPK_VERSION.tar.gz.sig
gpg --verify glpk-$GLPK_VERSION.tar.gz.sig
popd
```

## Tomcat

There are several Tomcat 8 maintainers that have release privileges; all of these
keys are available in a [`KEYS`](https://www.apache.org/dist/tomcat/tomcat-8/KEYS) file
available on their website, and all may be imported with this command:

```
curl https://www.apache.org/dist/tomcat/tomcat-8/KEYS | gpg --import
```

For the paranoid, it seems that only the keys for Mark Thomas is used for the
recent 8.5 releases, thus it's possible to verify with only his key:

```
pushd SOURCES
gpg --keyserver keys.gnupg.net --recv-keys 6FB21E8933C60243
curl -O http://www.apache.org/dist/tomcat/tomcat-8/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz
curl -O http://www.apache.org/dist/tomcat/tomcat-8/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz.asc
gpg --verify apache-tomcat-$TOMCAT_VERSION.tar.gz.asc
popd
```
