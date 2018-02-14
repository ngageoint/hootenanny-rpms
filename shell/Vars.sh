# The rpm apt package is required when on Ubuntu because we treat the
# *.spec files as a source of truth for version information and
# `rpm` and `rpmspec` are necessary to intrepret them from macros.
if ! test -x /usr/bin/rpm; then
    echo "This script requires the 'rpm' package."
    exit 1
fi

## Important variables needed for functions.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# Directories used in RPM process.
SPECS=$SCRIPT_HOME/SPECS
SOURCES=$SCRIPT_HOME/SOURCES
RPMS=$SCRIPT_HOME/RPMS

# Mocha version
MOCHA_VERSION=3.5.3

# PostgreSQL version
PG_VERSION=9.5
PG_DOTLESS=$(echo $PG_VERSION | tr -d '.')

## Utility functions.

function latest_hoot_archive() {
    echo $(ls -1t $SOURCES/hootenanny-[0-9]*.tar.gz | head -n1)
}

# Returns the output of Hootenanny's `HOOT_VERSION_GEN`, embedded
# in the archive's filename.
function latest_hoot_version_gen() {
    local hoot_archive=$( latest_hoot_archive )
    local hoot_version_gen=${hoot_archive##$SOURCES/hootenanny-}
    echo ${hoot_version_gen%%.tar.gz}
}

# Get version from YAML file.
function config_version() {
    cat $SCRIPT_HOME/config.yml | grep "\\&${1}" | awk '{ print $3 }' | tr -d "'" | awk -F- '{ print $1 }'
}

function config_release() {
    cat $SCRIPT_HOME/config.yml | grep "\\&${1}" | awk '{ print $3 }' | tr -d "'" | awk -F- '{ print $2 }'
}

# Get build requirement packages from spec file.
function spec_requires() {
    # Parse the spec file with `rpmspec` so that conditional packages won't
    # be included in the build containers.
    rpmspec \
        --define "_topdir ${SCRIPT_HOME}" \
        --define 'hoot_version_gen 0.0.0' \
        --define "pg_dotless ${PG_DOTLESS}" \
        --define 'rpmbuild_version 0.0.0' \
        --define 'rpmbuild_release 1' \
        -q --buildrequires $SPECS/$1.spec | \
        awk '{ for (i = 1; i <= NF; ++i) if ($i ~ /^[[:alpha:]]/) print $i }' ORS=' '
}

## Package versioning variables.
RPMBUILD_DIST=.el7

# Where binary RPMs are placed.
RPM_X86_64=$RPMS/x86_64
RPM_NOARCH=$RPMS/noarch

DUMBINIT_VERSION=$( config_version dumbinit )
DUMBINIT_RELEASE=$( config_release dumbinit )
DUMBINIT_RPM=dumb-init-$DUMBINIT_VERSION-$DUMBINIT_RELEASE$RPMBUILD_DIST.x86_64.rpm

FILEGDBAPI_VERSION=$( config_version filegdbapi )
FILEGDBAPI_RELEASE=$( config_release filegdbapi )
FILEGDBAPI_RPM=FileGDBAPI-$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE$RPMBUILD_DIST.x86_64.rpm

GDAL_VERSION=$( config_version gdal )
GDAL_RELEASE=$( config_release gdal )
GDAL_RPM_SUFFIX=$GDAL_VERSION-$GDAL_RELEASE$RPMBUILD_DIST.x86_64.rpm
GDAL_RPM=hoot-gdal-$GDAL_RPM_SUFFIX

GEOS_VERSION=$( config_version geos )
GEOS_RELEASE=$( config_release geos )
GEOS_RPM=geos-$GEOS_VERSION-$GEOS_RELEASE$RPMBUILD_DIST.x86_64.rpm
GEOS_DEVEL_RPM=geos-devel-$GEOS_VERSION-$GEOS_RELEASE$RPMBUILD_DIST.x86_64.rpm

LIBGEOTIFF_VERSION=$( config_version libgeotiff )
LIBGEOTIFF_RELEASE=$( config_release libgeotiff )
LIBGEOTIFF_RPM=libgeotiff-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE$RPMBUILD_DIST.x86_64.rpm
LIBGEOTIFF_DEVEL_RPM=libgeotiff-devel-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE$RPMBUILD_DIST.x86_64.rpm

LIBKML_VERSION=$( config_version libkml )
LIBKML_RELEASE=$( config_release libkml )
LIBKML_RPM=libkml-$LIBKML_VERSION-$LIBKML_RELEASE$RPMBUILD_DIST.x86_64.rpm
LIBKML_DEVEL_RPM=libkml-devel-$LIBKML_VERSION-$LIBKML_RELEASE$RPMBUILD_DIST.x86_64.rpm

NODE_VERSION=$( config_version node )
NODE_RELEASE=$( config_release node )
NODE_RPM=nodejs-$NODE_VERSION-$NODE_RELEASE$RPMBUILD_DIST.x86_64.rpm
NODE_DEVEL_RPM=nodejs-devel-$NODE_VERSION-$NODE_RELEASE$RPMBUILD_DIST.x86_64.rpm

OSMOSIS_VERSION=$( config_version osmosis )
OSMOSIS_RELEASE=$( config_release osmosis )
OSMOSIS_RPM=osmosis-$OSMOSIS_VERSION-$OSMOSIS_RELEASE$RPMBUILD_DIST.noarch.rpm

POSTGIS_VERSION=$( config_version postgis )
POSTGIS_RELEASE=$( config_release postgis )
POSTGIS_RPM=hoot-postgis23_$PG_DOTLESS-$POSTGIS_VERSION-$POSTGIS_RELEASE$RPMBUILD_DIST.x86_64.rpm

STXXL_VERSION=$( config_version stxxl )
STXXL_RELEASE=$( config_release stxxl )
STXXL_RPM=stxxl-$STXXL_VERSION-$STXXL_RELEASE$RPMBUILD_DIST.x86_64.rpm
STXXL_DEVEL_RPM=stxxl-devel-$STXXL_VERSION-$STXXL_RELEASE$RPMBUILD_DIST.x86_64.rpm

SUEXEC_VERSION=$( config_version suexec )
SUEXEC_RELEASE=$( config_release suexec )
SUEXEC_RPM=su-exec-$SUEXEC_VERSION-$SUEXEC_RELEASE$RPMBUILD_DIST.x86_64.rpm

TOMCAT8_VERSION=$( config_version tomcat8 )
TOMCAT8_RELEASE=$( config_release tomcat8 )
TOMCAT8_RPM=tomcat8-$TOMCAT8_VERSION-$TOMCAT8_RELEASE$RPMBUILD_DIST.noarch.rpm

WAMERICAN_VERSION=$( config_version wamerican )
WAMERICAN_RELEASE=$( config_release wamerican )
WAMERICAN_RPM=wamerican-insane-$WAMERICAN_VERSION-$WAMERICAN_RELEASE$RPMBUILD_DIST.noarch.rpm

WORDS_VERSION=$( config_version words )
WORDS_RELEASE=$( config_release words )
WORDS_RPM=hoot-words-$WORDS_VERSION-$WORDS_RELEASE$RPMBUILD_DIST.noarch.rpm


## Docker build functions.

# Builds all the base RPM compilation images.
function build_base_images() {
    # Foundation image that creates unprivileged user for RPM tasks
    # with the same uid as invoking user (for ease of use with
    # shared folders).
    docker build \
           --build-arg rpmbuild_dist=$RPMBUILD_DIST \
           --build-arg rpmbuild_uid=$(id -u) \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild \
           -t hootenanny/rpmbuild \
           $SCRIPT_HOME

    # Base image that has basic development and RPM building packages.
    docker build \
       -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-base \
       -t hootenanny/rpmbuild-base \
       $SCRIPT_HOME

    # Generic image for building RPMS without any other prerequisites.
    docker build \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hootenanny/rpmbuild-generic \
           $SCRIPT_HOME

    # Base image with PostgreSQL develop libraries from PGDG at the
    # requested version.
    docker build \
           --build-arg pg_version=$PG_VERSION \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-pgdg \
           -t hootenanny/rpmbuild-pgdg:$PG_VERSION \
           $SCRIPT_HOME
}

# Build images for creating and signing the RPM repository.
function build_repo_images() {
    docker build \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-repo \
           -t hootenanny/rpmbuild-repo \
           $SCRIPT_HOME
}


# Runs a dependency build image.
function run_dep_image() {
    local OPTIND opt
    local image=hootenanny/rpmbuild-generic
    local sources_mode=ro
    local user=rpmbuild
    local usage=no

    while getopts ":i:s:u:" opt; do
        case "${opt}" in
            i)
                image="${OPTARG}"
                ;;
            s)
                sources_mode="${OPTARG}"
                ;;
            u)
                user="${OPTARG}"
                ;;
            *)
                usage=yes
                ;;
        esac
    done
    shift $((OPTIND-1))

    if [ "${usage}" = "yes" ]; then
        echo "run_dep_image: [-i <image>] [-u <user>] [-s <SOURCES mode>]"
    else
        mkdir -p $RPMS
        docker run \
               -v $SOURCES:/rpmbuild/SOURCES:$sources_mode \
               -v $SPECS:/rpmbuild/SPECS:ro \
               -v $RPMS:/rpmbuild/RPMS:rw \
               -u $user \
               -it --rm \
               $image "$@"
    fi
}

# Runs a hootenanny build image.
function run_hoot_build_image() {
    local OPTIND opt
    local entrypoint=/docker-entrypoint.sh
    local image=hootenanny/rpmbuild-hoot-release
    local sources_mode=ro
    local user=root
    local usage=no

    while getopts ":e:i:s:u:" opt; do
        case "${opt}" in
            e)
                entrypoint="${OPTARG}"
                ;;
            i)
                image="${OPTARG}"
                ;;
            s)
                sources_mode="${OPTARG}"
                ;;
            u)
                user="${OPTARG}"
                ;;
            *)
                usage=yes
                ;;
        esac
    done
    shift $((OPTIND-1))

    if [ "${usage}" = "yes" ]; then
        echo "run_hoot_build_image: [-e <entrypoint>] [-i <image>] [-u <user>]"
    else
        mkdir -p $SCRIPT_HOME/hootenanny $SCRIPT_HOME/m2 $SCRIPT_HOME/npm
        docker run \
               -v $SOURCES:/rpmbuild/SOURCES:$sources_mode \
               -v $SPECS:/rpmbuild/SPECS:ro \
               -v $RPMS:/rpmbuild/RPMS:rw \
               -v $SCRIPT_HOME/hootenanny:/rpmbuild/hootenanny:rw \
               -v $SCRIPT_HOME/m2:/rpmbuild/.m2:rw \
               -v $SCRIPT_HOME/npm:/rpmbuild/.npm:rw \
               -v $SCRIPT_HOME/scripts:/rpmbuild/scripts:ro \
               --entrypoint $entrypoint \
               -u $user \
               -it --rm \
               $image "${@:-/bin/bash}"
    fi
}
