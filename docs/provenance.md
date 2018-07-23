# Provenance

This repository is an aggregate work of existing open source archives, released
under different open source licenses.  While this aggregate is licensed under the
[GPLv3](../LICENSE), it does not supercede the the original licensing of
Hootenanny's dependencies.

The licensing provenance of source archives
([`SOURCES`](../SOURCES)) and `.spec` files ([`SPECS`](../SPECS)) in this
repository are explained in this document.  Most `.spec` files and patches
were sourced from Fedora or the PostgreSQL Development Group (PGDG), which
use the [MIT license](./licenses/Fedora-LICENSE) or the
[PostgreSQL license](./licenses/PostgreSQL-LICENSE) (BSD-like).

## FileGDBAPI

The File Geodatabase API source archives (e.g.,
`FileGDB_API_$VERSION-64.tar.gz`) are obtained from
[ESRI's GitHub repository](https://github.com/Esri/file-geodatabase-api/tree/master/FileGDB_API_1.5.1)
and is released under the [Apache 2 license](http://www.apache.org/licenses/LICENSE-2.0).

## GEOS

The [GEOS](https://trac.osgeo.org/geos) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/geos/) and licensed under the
[GNU LGPL v2.1](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).

The [`geos.spec`](../SPECS/geos.spec) originates from
[PGDG's GEOS 3.5.0 Source RPM](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/geos-3.5.0-1.rhel7.src.rpm)
and is released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE).

## GLPK

The [GLPK](https://www.gnu.org/software/glpk/glpk.html) source archivse were
obtained directly from [GNU](https://ftp.gnu.org/gnu/glpk/) and licensed under
the [GPLv3](https://www.gnu.org/licenses/gpl.html).

The following packaging files originate from
[Fedora's GLPK RPM]((https://src.fedoraproject.org/cgit/rpms/glpk.git/)
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
* [`gdal-c2clib.patch`](../SOURCES/gdal-c2clib.patch)
* [`gdal-completion.patch`](../SOURCES/gdal-completion.patch)
* [`gdal-jni.patch`](../SOURCES/gdal-jni.patch)
* [`gdal-uchar.patch`](../SOURCES/gdal-uchar.patch)

## libgeotiff

The [GeoTIFF](https://trac.osgeo.org/geotiff/) library source archives are
obtained directly from [OSGeo](https://download.osgeo.org/geotiff/) and is
mostly [MIT/X11](https://trac.osgeo.org/geotiff/browser/trunk/libgeotiff/LICENSE)
licensed.

The [`libgeotiff.spec`](../SPECS/libgeotiff.spec) originates from
[PGDG's libgeotiff source RPM](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/libgeotiff-1.4.0-1.rhel7.src.rpm)
and is released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE).

## libkml

## NodeJS

## Osmosis

## PostGIS

## stxxl

## Tomcat
