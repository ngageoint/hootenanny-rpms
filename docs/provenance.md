# Provenance

The licensing provenance of source archives
([`SOURCES`](../SOURCES)) and `.spec` files ([`SPECS`](../SPECS)) in this
repository are explained in this document.  In particular, this repository
is an aggregate work of existing open source archives, released
under different open source licenses.  While this aggregate is licensed under the
[GPLv3](../LICENSE), it does not supersede the original licensing of
archives, `.spec` files, or imported patches.

Most `.spec` files and patches
were originally sourced from Fedora or the PostgreSQL Development Group (PGDG),
which use the [MIT license](./licenses/Fedora-LICENSE)
([source](https://fedoraproject.org/wiki/Legal:Licenses/LicenseAgreement))
or the
[PostgreSQL license](./licenses/PostgreSQL-LICENSE)
([source](http://apt.postgresql.org/pub/README)), respectively.

## dumb-init

The [dumb-init](https://github.com/Yelp/dumb-init) source archive was obtained
directly from [GitHub](https://github.com/Yelp/dumb-init/releases) and
is [MIT licensed](https://github.com/Yelp/dumb-init/blob/master/LICENSE).

## GLPK

The [GLPK](https://www.gnu.org/software/glpk/glpk.html) source archives were
obtained directly from [GNU](https://ftp.gnu.org/gnu/glpk/) and licensed under
the [GPLv3](https://www.gnu.org/licenses/gpl.html).

The following packaging files originate from
[Fedora GLPK RPM](https://src.fedoraproject.org/cgit/rpms/glpk.git)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`glpk.spec`](../SPECS/glpk.spec)
* [`glpk-alias.patch`](../SOURCES/glpk-alias.patch)
* [`glpk-unbundle-suitesparse-zlib.patch`](../SOURCES/glpk-unbundle-suitesparse-zlib.patch)

## liboauthcpp

The [liboauthcpp](https://github.com/sirikata/liboauthcpp) source
archives were obtained directly from the `master` branch on
[GitHub](https://github.com/sirikata/liboauthcpp/) and are
[MIT licensed](https://github.com/sirikata/liboauthcpp/blob/master/LICENSE).

## libphonenumber

The [libphonenumber](https://github.com/googlei18n/libphonenumber) source
archives were obtained directly from
[GitHub](https://github.com/googlei18n/libphonenumber/releases) and are
[Apache 2 licensed](https://github.com/googlei18n/libphonenumber/blob/master/LICENSE).

## libpostal

The [libpostal](https://github.com/openvenues/libpostal) source
archives were obtained directly from
[GitHub](https://github.com/openvenues/libpostal/releases) and are
[MIT licensed](https://github.com/openvenues/libpostal/blob/master/LICENSE).

## NodeJS

The [NodeJS](https://nodejs.org/) source archives are obtained
directly from [NodeJs download page](https://nodejs.org/en/download/).
NodeJS includes bundled copy of [Unicode ICU](https://github.com/unicode-org/icu);
its [source code archive](../SOURCES/icu4c-67_1-src.tgz) is under the
[Unicode License](https://github.com/unicode-org/icu/blob/main/icu4c/LICENSE).

The following packaging files originate from
[Fedora NodeJS RPM](https://src.fedoraproject.org/cgit/rpms/nodejs.git)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`nodejs.spec`](../SPECS/nodejs.spec)
* [`macros.nodejs`](../SOURCES/macros.nodejs)
* [`nodejs-0001-Disable-running-gyp-files-for-bundled-deps.patch.patch`](../SOURCES/nodejs-0001-Disable-running-gyp-files-for-bundled-deps.patch)
* [`nodejs-0002-Install-both-binaries-and-use-libdir.patch`](../SOURCES/nodejs-0002-Install-both-binaries-and-use-libdir.patch)
* [`nodejs-0003-src-add-.note.GNU-stack-section.patch`](../SOURCES/nodejs-0003-src-add-.note.GNU-stack-section.patch)
* [`nodejs-btest402.js`](../SOURCES/nodejs-btest402.js)
* [`nodejs_native.attr.patch`](../SOURCES/nodejs_native.attr)
* [`nodejs-tarball.sh`](../SOURCES/nodejs-tarball.sh)
* [`npmrc`](../SOURCES/npmrc)

## Osmosis

The [Osmosis](https://wiki.openstreetmap.org/wiki/Osmosis) source archive was
obtained directly from the [OpenStreetMap(https://bretth.dev.openstreetmap.org/osmosis-build/)
project and was released into the public domain.

The [`osmosis-fix_launcher.patch`](../SOURCES/osmosis-fix_launcher.patch) file
comes from [Debian GIS Project](https://salsa.debian.org/debian-gis-team/osmosis/blob/master/debian/patches/01-fix_launcher.patch)
and is licensed under the GPLv3.

## stxxl

The [stxxl](http://stxxl.org/) source archives are obtained
directly from their [SourceForge downloads](https://sourceforge.net/projects/stxxl/files/stxxl/1.3.1/stxxl-1.3.1.tar.gz/download)
and is released under the
[Boost Software License, Version 1.0](http://www.boost.org/LICENSE_1_0.txt).

The [`stxxl.spec`](../SPECS/stxxl.spec) file originates from
[Fedora `stxxl` RPM](https://src.fedoraproject.org/cgit/rpms/stxxl.git)
packaging repository and is [MIT licensed](./licenses/Fedora-LICENSE).

## su-exec

The [su-exec](https://github.com/ncopa/su-exec) source archive was obtained
directly from [GitHub](https://github.com/ncopa/su-exec/releases) and
is [MIT licensed](https://github.com/ncopa/su-exec/blob/master/LICENSE).

## Tomcat

The [Tomcat](https://tomcat.apache.org/) source archives are obtained
directly from the [Apache Software Foundation](https://www.apache.org/dist/tomcat/)
and released under the [Apache 2 license](http://www.apache.org/licenses/LICENSE-2.0).

The [`tomcat8.spec`](../SPECS/tomcat8.spec) file originates from the
[JPackage Project](http://www.jpackage.org), is BSD licensed and
was later incorporated into
[Fedora Tomcat RPM](https://src.fedoraproject.org/cgit/rpms/tomcat.git)
repository.

These additional packaging files originate from
[Fedora Tomcat RPM](https://src.fedoraproject.org/cgit/rpms/tomcat.git)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`tomcat8.conf`](../SOURCES/tomcat8.conf)
* [`tomcat8.functions`](../SOURCES/tomcat8.functions)
* [`tomcat8.logrotate`](../SOURCES/tomcat8.logrotate)
* [`tomcat8.named-service`](../SOURCES/tomcat8.named-service)
* [`tomcat8.preamble`](../SOURCES/tomcat8.preamble)
* [`tomcat8.server`](../SOURCES/tomcat8.server)
* [`tomcat8.service`](../SOURCES/tomcat8.service)
* [`tomcat8.sysconfig`](../SOURCES/tomcat8.sysconfig)
* [`tomcat8.wrapper`](../SOURCES/tomcat8.wrapper)
