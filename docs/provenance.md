# Provenance

This repository is an aggregate work of existing open source archives, released
under different open source licenses.  While this aggregate is licensed under the
[GPLv3](../LICENSE), it does not supersede the the original licensing of
Hootenanny's dependencies.

The licensing provenance of source archives
([`SOURCES`](../SOURCES)) and `.spec` files ([`SPECS`](../SPECS)) in this
repository are explained in this document.  Most `.spec` files and patches
were sourced from Fedora or the PostgreSQL Development Group (PGDG), which
use the [MIT license](./licenses/Fedora-LICENSE) or the
[PostgreSQL license](./licenses/PostgreSQL-LICENSE) (BSD-like).

## dumb-init

The [dumb-init](https://github.com/Yelp/dumb-init) source archive was obtained
directly from [GitHub](https://github.com/Yelp/dumb-init/releases) and
is [MIT licensed](https://github.com/Yelp/dumb-init/blob/master/LICENSE).

## FileGDBAPI

The File Geodatabase API source archives are obtained from
[ESRI's GitHub repository](https://github.com/Esri/file-geodatabase-api/tree/master/FileGDB_API_1.5.1)
and is released under the [Apache 2 license](http://www.apache.org/licenses/LICENSE-2.0).

## GEOS

The [GEOS](https://trac.osgeo.org/geos) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/geos/) and licensed under the
[GNU LGPL v2.1](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).

The [`geos.spec`](../SPECS/geos.spec) originates from
[PGDG's GEOS 3.5.0 Source RPM](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/)
and is released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE).

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

## NodeJS

The [NodeJS](https://nodejs.org/) source archives are obtained
directly from [Node's download page](https://nodejs.org/en/download/).

The following packaging files originate from
[Fedora's NodeJS RPM](https://src.fedoraproject.org/cgit/rpms/nodejs.git)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`nodejs.spec`](../SPECS/nodejs.spec)
* [`nodejs_native.attr.patch`](../SOURCES/nodejs_native.attr)
* [`nodejs-0001-Disable-running-gyp-files-for-bundled-deps.patch.patch`](../SOURCES/nodejs-0001-Disable-running-gyp-files-for-bundled-deps.patch)
* [`nodejs-0002-Fix-aarch64-debug.patch`](../SOURCES/nodejs-0002-Fix-aarch64-debug.patch)
* [`nodejs-0003-hoot-value-json-object.patch`](../SOURCES/nodejs-0003-hoot-value-json-object.patch)

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
[PGDG's PostGIS 2.3.3 source RPM](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/)
and are released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE):

* [`hoot-postgis23.spec`](../SPECS/hoot-postgis23.spec)
* [`postgis-filter-requires-perl-Pg.sh`](../SOURCES/postgis-filter-requires-perl-Pg.sh)
* [`postgis-gdalfpic.patch`](../SOURCES/postgis-gdalfpic.patch)

## stxxl

The [stxxl](http://stxxl.org/) source archives are obtained
directly from their [SourceForge downloads](https://sourceforge.net/projects/stxxl/files/stxxl/1.3.1/stxxl-1.3.1.tar.gz/download)
and is under the [Boost Software License, Version 1.0](http://www.boost.org/LICENSE_1_0.txt).

The [`stxxl.spec`](../SPECS/stxxl.spec) originates from
[Fedora's `stxxl` RPM](https://src.fedoraproject.org/cgit/rpms/stxxl.git)
packaging repository and is [MIT licensed](./licenses/Fedora-LICENSE).

## su-exec

The [su-exec](https://github.com/ncopa/su-exec) source archive was obtained
directly from [GitHub](https://github.com/ncopa/su-exec/releases) and
is [MIT licensed](https://github.com/ncopa/su-exec/blob/master/LICENSE).

## Tomcat
