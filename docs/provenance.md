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

## armadillo

The [armadillo](http://arma.sourceforge.net/) source archive was obtained from
[SourceForge](https://sourceforge.net/projects/arma/files/) and is released
under the [Apache 2 license](http://arma.sourceforge.net/license.html).

The [`armadillo.spec`](../SPECS/aramadillo.spec) file was sourced from
[Fedora's armadillo RPM](https://src.fedoraproject.org/rpms/armadillo/tree/master)
repository (master branch) and is [MIT licensed](./licenses/Fedora-LICENSE).

## dumb-init

The [dumb-init](https://github.com/Yelp/dumb-init) source archive was obtained
directly from [GitHub](https://github.com/Yelp/dumb-init/releases) and
is [MIT licensed](https://github.com/Yelp/dumb-init/blob/master/LICENSE).

## FileGDBAPI

The File Geodatabase API source archives are obtained from
[ESRI's GitHub repository](https://github.com/Esri/file-geodatabase-api/tree/master/FileGDB_API_1.5.1)
and released under the [Apache 2 license](http://www.apache.org/licenses/LICENSE-2.0).

## GEOS

The [GEOS](https://trac.osgeo.org/geos) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/geos/) and licensed under the
[GNU LGPL v2.1](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).

The [`geos.spec`](../SPECS/geos.spec) originates from
[PGDG's GEOS 3.5.0 Source RPM](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/)
and is released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE).

## proj

The [proj](https://github.com/OSGeo/proj.4/releases) source archives are obtained
directly from [OSGeo's GitHub releases](https://github.com/OSGeo/proj.4/releases).
The proj source code archives are [MIT licensed](https://github.com/OSGeo/proj.4/blob/master/COPYING),
and the datumgrid archives are under
[public domain, MIT, BSD, and Creative Commons licenses](https://github.com/OSGeo/proj-datumgrid/blob/master/README.DATUMGRID).

The [`proj.spec`](../SPECS/proj.spec) file originates from
[Fedora's proj RPM](https://src.fedoraproject.org/rpms/proj/tree/master)
repository (master branch) and is [MIT licensed](./licenses/Fedora-LICENSE).

## GDAL

The [GDAL](https://trac.osgeo.org/gdal) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/gdal/) and is mostly
[MIT/X11](https://trac.osgeo.org/gdal/wiki/FAQGeneral#WhatexactlywasthelicensetermsforGDAL)
licensed.

The following packaging files originate from
[Fedora's GDAL RPM](https://src.fedoraproject.org/rpms/gdal/tree/f25)
repository (Fedora 25 release) and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`hoot-gdal.spec`](../SPECS/hoot-gdal.spec)
* [`gdal-1.9.0-java.patch`](../SOURCES/gdal-1.9.0-java.patch)
* [`gdal-2.1.0-zlib.patch`](../SOURCES/gdal-2.1.0-zlib.patch)
* [`gdal-g2clib.patch`](../SOURCES/gdal-g2clib.patch)
* [`gdal-completion.patch`](../SOURCES/gdal-completion.patch)
* [`gdal-jni.patch`](../SOURCES/gdal-jni.patch)
* [`gdal-uchar.patch`](../SOURCES/gdal-uchar.patch)

## GLPK

The [GLPK](https://www.gnu.org/software/glpk/glpk.html) source archives were
obtained directly from [GNU](https://ftp.gnu.org/gnu/glpk/) and licensed under
the [GPLv3](https://www.gnu.org/licenses/gpl.html).

The following packaging files originate from
[Fedora's GLPK RPM](https://src.fedoraproject.org/cgit/rpms/glpk.git)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`glpk.spec`](../SPECS/glpk.spec)
* [`glpk-alias.patch`](../SOURCES/glpk-alias.patch)
* [`glpk-unbundle-suitesparse-zlib.patch`](../SOURCES/glpk-unbundle-suitesparse-zlib.patch)

## gpsbabel

The [gpsbabel](https://www.gpsbabel.org/) source archive was obtained directly
from their website.  The [`gpsbabel.spec`](../SPECS/gpsbabel.spec) and all
patches from [`SOURCES`](../SOURCES) starting with `gpsbabel` are from
[Fedora's `gpsbabel` RPM](https://src.fedoraproject.org/rpms/gpsbabel/tree/master)
repository and are [MIT licensed](./licenses/Fedora-LICENSE).

## libgeotiff

The [GeoTIFF](https://trac.osgeo.org/geotiff/) library source archives are
obtained directly from [OSGeo](https://download.osgeo.org/geotiff/) and is
mostly [MIT/X11](https://trac.osgeo.org/geotiff/browser/trunk/libgeotiff/LICENSE)
licensed.

The [`libgeotiff.spec`](../SPECS/libgeotiff.spec) originates from
[PGDG's `libgeotiff` 1.4.0 source RPM](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/)
and is released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE).

## libkml

The [libkml](https://github.com/libkml/libkml) source archives were obtained
directly from [GitHub](https://github.com/libkml/libkml/releases) and are
[BSD](https://github.com/libkml/libkml/blob/master/LICENSE) licensed.

The following packaging files originate from
[Fedora's `libkml` RPM](https://src.fedoraproject.org/cgit/rpms/libkml.git)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`libkml.spec`](../SPECS/libkml.spec)
* [`libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch`](../SOURCES/libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch)
* [`libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch`](../SOURCES/libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch)
* [`libkml-0003-Fix-python-tests.patch`](../SOURCES/libkml-0003-Fix-python-tests.patch)
* [`libkml-0004-Correctly-build-and-run-java-test.patch`](../SOURCES/libkml-0004-Correctly-build-and-run-java-test.patch)
* [`libkml-fragile_test.patch`](../SOURCES/libkml-fragile_test.patch)
* [`libkml-dont-bytecompile.patch`](../SOURCES/libkml-dont-bytecompile.patch)

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
directly from [Node's download page](https://nodejs.org/en/download/).
NodeJS includes bundled copy of [Unicode ICU](https://github.com/unicode-org/icu);
its [source code archive](../SOURCES/icu4c-67_1-src.tgz) is under the
[Unicode License](https://github.com/unicode-org/icu/blob/main/icu4c/LICENSE).

The following packaging files originate from
[Fedora's NodeJS RPM](https://src.fedoraproject.org/cgit/rpms/nodejs.git)
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
comes from [Debian's GIS Project](https://salsa.debian.org/debian-gis-team/osmosis/blob/master/debian/patches/01-fix_launcher.patch)
and is licensed under the GPLv3.

## PostGIS

The [PostGIS](https://trac.osgeo.org/postgis) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/postgis/) and licensed
under the [GPLv2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

The following packaging files originate from
[PGDG's PostGIS 2.3.3 and 2.4.4 source RPMs](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/),
released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE):

* [`hoot-postgis23.spec`](../SPECS/hoot-postgis23.spec)
* [`hoot-postgis24.spec`](../SPECS/hoot-postgis24.spec)
* [`postgis-filter-requires-perl-Pg.sh`](../SOURCES/postgis-filter-requires-perl-Pg.sh)
* [`postgis-gdalfpic.patch`](../SOURCES/postgis-gdalfpic.patch)

## stxxl

The [stxxl](http://stxxl.org/) source archives are obtained
directly from their [SourceForge downloads](https://sourceforge.net/projects/stxxl/files/stxxl/1.3.1/stxxl-1.3.1.tar.gz/download)
and is released under the
[Boost Software License, Version 1.0](http://www.boost.org/LICENSE_1_0.txt).

The [`stxxl.spec`](../SPECS/stxxl.spec) file originates from
[Fedora's `stxxl` RPM](https://src.fedoraproject.org/cgit/rpms/stxxl.git)
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
[Fedora's Tomcat RPM](https://src.fedoraproject.org/cgit/rpms/tomcat.git)
repository.

These additional packaging files originate from
[Fedora's Tomcat RPM](https://src.fedoraproject.org/cgit/rpms/tomcat.git)
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
