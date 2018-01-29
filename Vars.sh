# The rpm apt package is required when on Ubuntu because we treat the
# *.spec files as a source of truth for version information and
# `rpm` and `rpmspec` are necessary to intrepret them from macros.
if ! test -x /usr/bin/rpm; then
    echo "This script requires the 'rpm' package."
    exit 1
fi

## Important variables needed for functions.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Directories used in RPM process.
SPECS=$SCRIPT_HOME/SPECS
SOURCES=$SCRIPT_HOME/SOURCES
RPMS=$SCRIPT_HOME/RPMS

# Mocha/NodeJS versions
MOCHA_VERSION=3.5.3
NODE_VERSION=0.10.48

# PostgreSQL
PG_VERSION=9.5
PG_DOTLESS=$(echo $PG_VERSION | tr -d '.')

# Get version from spec file.
function spec_version() {
    rpm -q --specfile --qf='%{version}\n' \
        --define "%_topdir ${SCRIPT_HOME}" \
        $SPECS/$1.spec | head -n 1
}

# Get release number from spec file.
function spec_release() {
    rpm -q --specfile --qf='%{release}\n' \
        --define "%_topdir ${SCRIPT_HOME}" \
        $SPECS/$1.spec | head -n 1
}

# Get build requirement packages from spec file.
function spec_requires() {
    # Parse the spec file with `rpmspec` so that conditional packages won't
    # be included in the build containers.
    rpmspec \
        --define "%_topdir ${SCRIPT_HOME}" \
        --define "%pg_dotless ${PG_DOTLESS}" \
        -P $SPECS/$1.spec | \
        grep '^BuildRequires:' | \
        awk '{ for (i = 2; i <= NF; ++i) if ($i ~ /^[[:alpha:]]/) print $i }' ORS=' '
}

## Package versioning variables.
RPMBUILD_DIST=.el7

# Where binary RPMs are placed.
RPM_X86_64=$RPMS/x86_64
RPM_NOARCH=$RPMS/noarch

DUMBINIT_VERSION=$( spec_version dumb-init )
DUMBINIT_RELEASE=$( spec_release dumb-init )
DUMBINIT_RPM=dumb-init-$DUMBINIT_VERSION-$DUMBINIT_RELEASE$RPMBUILD_DIST.x86_64.rpm

FILEGDBAPI_VERSION=$( spec_version FileGDBAPI )
FILEGDBAPI_RELEASE=$( spec_release FileGDBAPI )
FILEGDBAPI_RPM=FileGDBAPI-$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE$RPMBUILD_DIST.x86_64.rpm

GDAL_VERSION=$( spec_version hoot-gdal )
GDAL_RELEASE=$( spec_release hoot-gdal )
GDAL_RPM_SUFFIX=$GDAL_VERSION-$GDAL_RELEASE$RPMBUILD_DIST.x86_64.rpm
GDAL_RPM=hoot-gdal-$GDAL_RPM_SUFFIX

GEOS_VERSION=$( spec_version geos )
GEOS_RELEASE=$( spec_release geos )
GEOS_RPM=geos-$GEOS_VERSION-$GEOS_RELEASE$RPMBUILD_DIST.x86_64.rpm
GEOS_DEVEL_RPM=geos-devel-$GEOS_VERSION-$GEOS_RELEASE$RPMBUILD_DIST.x86_64.rpm

LIBGEOTIFF_VERSION=$( spec_version libgeotiff )
LIBGEOTIFF_RELEASE=$( spec_release libgeotiff )
LIBGEOTIFF_RPM=libgeotiff-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE$RPMBUILD_DIST.x86_64.rpm
LIBGEOTIFF_DEVEL_RPM=libgeotiff-devel-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE$RPMBUILD_DIST.x86_64.rpm

LIBKML_VERSION=$( spec_version libkml )
LIBKML_RELEASE=$( spec_release libkml )
LIBKML_RPM=libkml-$LIBKML_VERSION-$LIBKML_RELEASE$RPMBUILD_DIST.x86_64.rpm
LIBKML_DEVEL_RPM=libkml-devel-$LIBKML_VERSION-$LIBKML_RELEASE$RPMBUILD_DIST.x86_64.rpm

NODEJS_VERSION=$( spec_version nodejs )
NODEJS_RELEASE=$( spec_release nodejs )
NODEJS_RPM=nodejs-$NODEJS_VERSION-$NODEJS_RELEASE$RPMBUILD_DIST.x86_64.rpm
NODEJS_DEVEL_RPM=nodejs-devel-$NODEJS_VERSION-$NODEJS_RELEASE$RPMBUILD_DIST.x86_64.rpm

OSMOSIS_VERSION=$( spec_version osmosis )
OSMOSIS_RELEASE=$( spec_release osmosis )
OSMOSIS_RPM=osmosis-$OSMOSIS_VERSION-$OSMOSIS_RELEASE$RPMBUILD_DIST.noarch.rpm

POSTGIS_VERSION=$( spec_version hoot-postgis23 )
POSTGIS_RELEASE=$( spec_release hoot-postgis23 )
POSTGIS_RPM=hoot-postgis23_$PG_DOTLESS-$POSTGIS_VERSION-$POSTGIS_RELEASE$RPMBUILD_DIST.x86_64.rpm

STXXL_VERSION=$( spec_version stxxl )
STXXL_RELEASE=$( spec_release stxxl )
STXXL_RPM=stxxl-$STXXL_VERSION-$STXXL_RELEASE$RPMBUILD_DIST.x86_64.rpm
STXXL_DEVEL_RPM=stxxl-devel-$STXXL_VERSION-$STXXL_RELEASE$RPMBUILD_DIST.x86_64.rpm

SUEXEC_VERSION=$( spec_version su-exec )
SUEXEC_RELEASE=$( spec_release su-exec )
SUEXEC_RPM=su-exec-$SUEXEC_VERSION-$SUEXEC_RELEASE$RPMBUILD_DIST.x86_64.rpm

TOMCAT8_VERSION=$( spec_version tomcat8 )
TOMCAT8_RELEASE=$( spec_release tomcat8 )
TOMCAT8_RPM=tomcat8-$TOMCAT8_VERSION-$TOMCAT8_RELEASE$RPMBUILD_DIST.noarch.rpm

WAMERICAN_VERSION=$( spec_version wamerican-insane )
WAMERICAN_RELEASE=$( spec_release wamerican-insane )
WAMERICAN_RPM=wamerican-insane-$WAMERICAN_VERSION-$WAMERICAN_RELEASE$RPMBUILD_DIST.noarch.rpm

WORDS_VERSION=$( spec_version hoot-words )
WORDS_RELEASE=$( spec_release hoot-words )
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
           -t hoot/rpmbuild \
           $SCRIPT_HOME

    # Base image that has basic development and RPM building packages.
    docker build \
       -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-base \
       -t hoot/rpmbuild-base \
       $SCRIPT_HOME

    # Generic image for building RPMS without any other prerequisites.
    docker build \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hoot/rpmbuild-generic \
           $SCRIPT_HOME

    # Base image with PostgreSQL develop libraries from PGDG at the
    # requested version.
    docker build \
           --build-arg pg_version=$PG_VERSION \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-pgdg \
           -t hoot/rpmbuild-pgdg:$PG_VERSION \
           $SCRIPT_HOME
}

# Build images for creating and signing the RPM repository.
function build_repo_images() {
    docker build \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-repo \
           -t hoot/rpmbuild-repo \
           $SCRIPT_HOME
}


# Runs a dependency build image.
function run_dep_image() {
    local OPTIND opt
    local image=hoot/rpmbuild-generic
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
function run_hoot_image() {
    local OPTIND opt
    local entrypoint=/docker-entrypoint.sh
    local image=hoot/rpmbuild-hoot-release
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
        echo "run_hoot_image: [-e <entrypoint>] [-i <image>] [-u <user>]"
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
