#!/bin/bash
set -e

## Important variables needed for functions.

SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# NodeJS
NODE_VERSION=0.10.46

# PostgreSQL
PG_VERSION=9.5
PG_DOTLESS=$(echo $PG_VERSION | tr -d '.')

# Get version from spec file.
function get_version() {
    rpm -q --specfile --qf='%{version}\n' \
        --define "%_topdir ${SCRIPT_HOME}/src" \
        $SCRIPT_HOME/src/SPECS/$1.spec | head -n 1
}

# Get release number from spec file.
function get_release() {
    rpm -q --specfile --qf='%{release}\n' \
        --define "%_topdir ${SCRIPT_HOME}/src" \
        $SCRIPT_HOME/src/SPECS/$1.spec | head -n 1
}

# Get build requirement packages from spec file.
function get_requires() {
    # Parse the spec file with `rpmspec` so that conditional packages won't
    # be included in the build containers.
    rpmspec \
        --define "%pg_dotless ${PG_DOTLESS}" \
        -P $SCRIPT_HOME/src/SPECS/$1.spec | \
        grep '^BuildRequires:' | \
        awk '{ for (i = 2; i <= NF; ++i) if ($i ~ /^[[:alpha:]]/) print $i }' ORS=' '
}

## Package versioning variables.

# Where binary RPMs are placed.
RPM_X86_64=$SCRIPT_HOME/src/RPMS/x86_64
RPM_NOARCH=$SCRIPT_HOME/src/RPMS/noarch
RPMBUILD_DIST=.el7

FILEGDBAPI_VERSION=$( get_version FileGDBAPI )
FILEGDBAPI_RELEASE=$( get_release FileGDBAPI )
FILEGDBAPI_RPM=FileGDBAPI-$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE$RPMBUILD_DIST.x86_64.rpm

GDAL_VERSION=$( get_version hoot-gdal )
GDAL_RELEASE=$( get_release hoot-gdal )
GDAL_RPM_SUFFIX=$GDAL_VERSION-$GDAL_RELEASE$RPMBUILD_DIST.x86_64.rpm
GDAL_RPM=hoot-gdal-$GDAL_RPM_SUFFIX

GEOS_VERSION=$( get_version geos )
GEOS_RELEASE=$( get_release geos )
GEOS_RPM=geos-$GEOS_VERSION-$GEOS_RELEASE$RPMBUILD_DIST.x86_64.rpm
GEOS_DEVEL_RPM=geos-devel-$GEOS_VERSION-$GEOS_RELEASE$RPMBUILD_DIST.x86_64.rpm

LIBGEOTIFF_VERSION=$( get_version libgeotiff )
LIBGEOTIFF_RELEASE=$( get_release libgeotiff )
LIBGEOTIFF_RPM=libgeotiff-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE$RPMBUILD_DIST.x86_64.rpm
LIBGEOTIFF_DEVEL_RPM=libgeotiff-devel-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE$RPMBUILD_DIST.x86_64.rpm

LIBKML_VERSION=$( get_version libkml )
LIBKML_RELEASE=$( get_release libkml )
LIBKML_RPM=libkml-$LIBKML_VERSION-$LIBKML_RELEASE$RPMBUILD_DIST.x86_64.rpm
LIBKML_DEVEL_RPM=libkml-devel-$LIBKML_VERSION-$LIBKML_RELEASE$RPMBUILD_DIST.x86_64.rpm

OSMOSIS_VERSION=$( get_version osmosis )
OSMOSIS_RELEASE=$( get_release osmosis )
OSMOSIS_RPM=osmosis-$OSMOSIS_VERSION-$OSMOSIS_RELEASE$RPMBUILD_DIST.noarch.rpm

POSTGIS_VERSION=$( get_version hoot-postgis23 )
POSTGIS_RELEASE=$( get_release hoot-postgis23 )
POSTGIS_RPM=hoot-postgis23_$PG_DOTLESS-$POSTGIS_VERSION-$POSTGIS_RELEASE$RPMBUILD_DIST.x86_64.rpm

STXXL_VERSION=$( get_version stxxl )
STXXL_RELEASE=$( get_release stxxl )
STXXL_RPM=stxxl-$STXXL_VERSION-$STXXL_RELEASE$RPMBUILD_DIST.x86_64.rpm
STXXL_DEVEL_RPM=stxxl-devel-$STXXL_VERSION-$STXXL_RELEASE$RPMBUILD_DIST.x86_64.rpm

TOMCAT8_VERSION=$( get_version tomcat8 )
TOMCAT8_RELEASE=$( get_release tomcat8 )
TOMCAT8_RPM=tomcat8-$TOMCAT8_VERSION-$TOMCAT8_RELEASE$RPMBUILD_DIST.noarch.rpm

WAMERICAN_VERSION=$( get_version wamerican-insane )
WAMERICAN_RELEASE=$( get_release wamerican-insane )
WAMERICAN_RPM=wamerican-insane-$WAMERICAN_VERSION-$WAMERICAN_RELEASE$RPMBUILD_DIST.noarch.rpm

WORDS_VERSION=$( get_version hoot-words )
WORDS_RELEASE=$( get_release hoot-words )
WORDS_RPM=hoot-words-$WORDS_VERSION-$WORDS_RELEASE$RPMBUILD_DIST.noarch.rpm
