# The rpm-build apt package is required when on Ubuntu because we treat the
# *.spec files as a source of truth for version information and
# `rpm` and `rpmspec` are necessary to intrepret them from macros.
if ! test -x /usr/bin/rpmbuild; then
    echo "This script requires the 'rpm' package (Ubuntu) or 'rpm-build' (CentOS)"
    exit 1
fi

## Important variables needed for functions.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# Directories used in RPM process.
SPECS=$SCRIPT_HOME/SPECS
SOURCES=$SCRIPT_HOME/SOURCES
RPMS=$SCRIPT_HOME/RPMS

CACHE=$SCRIPT_HOME/cache
HOOT=$SCRIPT_HOME/hootenanny

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
    cat $SCRIPT_HOME/config.yml | grep "\\&${1}" | awk '{ print $3 }' | tr -d "'" | awk -F"${2:--}" '{ print $1 }'
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
        --define 'tomcat_version 0.0.0' \
        -q --buildrequires $SPECS/$1.spec | \
        awk '{ for (i = 1; i <= NF; ++i) if ($i ~ /^[[:alpha:]]/) print $i }' ORS=' '
}

MAVEN_CACHE_URL=$( config_version maven_cache_url " ")
MAVEN_CACHE_SHA1=$( config_version maven_cache_sha1 )

# Mocha version
MOCHA_VERSION=$( config_version mocha )

# PostgreSQL version
PG_VERSION=$( config_version pg )
PG_DOTLESS=$(echo $PG_VERSION | tr -d '.')

## Package versioning variables.
RPMBUILD_DIST=$( config_version rpmbuild_dist )

# Where binary RPMs are placed.
RPM_X86_64=$RPMS/x86_64
RPM_NOARCH=$RPMS/noarch

DUMBINIT_VERSION=$( config_version dumbinit )
DUMBINIT_RELEASE=$( config_release dumbinit )
DUMBINIT_RPM=dumb-init-$DUMBINIT_VERSION-$DUMBINIT_RELEASE$RPMBUILD_DIST.x86_64.rpm

FILEGDBAPI_VERSION=$( config_version FileGDBAPI )
FILEGDBAPI_RELEASE=$( config_release FileGDBAPI )
FILEGDBAPI_RPM=FileGDBAPI-$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE$RPMBUILD_DIST.x86_64.rpm

GDAL_VERSION=$( config_version gdal )
GDAL_RELEASE=$( config_release gdal )
GDAL_RPM_SUFFIX=$GDAL_VERSION-$GDAL_RELEASE$RPMBUILD_DIST.x86_64.rpm
GDAL_RPM=hoot-gdal-$GDAL_RPM_SUFFIX

GEOS_VERSION=$( config_version geos )
GEOS_RELEASE=$( config_release geos )
GEOS_RPM=geos-$GEOS_VERSION-$GEOS_RELEASE$RPMBUILD_DIST.x86_64.rpm
GEOS_DEVEL_RPM=geos-devel-$GEOS_VERSION-$GEOS_RELEASE$RPMBUILD_DIST.x86_64.rpm

GLPK_VERSION=$( config_version glpk )
GLPK_RELEASE=$( config_release glpk )
GLPK_RPM=glpk-$GLPK_VERSION-$GLPK_RELEASE$RPMBUILD_DIST.x86_64.rpm
GLPK_DEVEL_RPM=glpk-devel-$GLPK_VERSION-$GLPK_RELEASE$RPMBUILD_DIST.x86_64.rpm

LIBGEOTIFF_VERSION=$( config_version libgeotiff )
LIBGEOTIFF_RELEASE=$( config_release libgeotiff )
LIBGEOTIFF_RPM=libgeotiff-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE$RPMBUILD_DIST.x86_64.rpm
LIBGEOTIFF_DEVEL_RPM=libgeotiff-devel-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE$RPMBUILD_DIST.x86_64.rpm

LIBKML_VERSION=$( config_version libkml )
LIBKML_RELEASE=$( config_release libkml )
LIBKML_RPM=libkml-$LIBKML_VERSION-$LIBKML_RELEASE$RPMBUILD_DIST.x86_64.rpm
LIBKML_DEVEL_RPM=libkml-devel-$LIBKML_VERSION-$LIBKML_RELEASE$RPMBUILD_DIST.x86_64.rpm

NODEJS_VERSION=$( config_version nodejs )
NODEJS_RELEASE=$( config_release nodejs )
NODEJS_RPM=nodejs-$NODEJS_VERSION-$NODEJS_RELEASE$RPMBUILD_DIST.x86_64.rpm
NODEJS_DEVEL_RPM=nodejs-devel-$NODEJS_VERSION-$NODEJS_RELEASE$RPMBUILD_DIST.x86_64.rpm

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
           --build-arg rpmbuild_gid=$(id -g) \
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

function build_other_images() {
    # Build image for creating and signing the RPM repository.
    docker build \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-repo \
           -t hootenanny/rpmbuild-repo \
           $SCRIPT_HOME

    # Build image for linting this repository's source code.
    docker build \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-lint \
           -t hootenanny/rpmbuild-lint \
           $SCRIPT_HOME
}

function build_run_images() {
    docker build \
           --build-arg pg_version=$PG_VERSION \
           -f $SCRIPT_HOME/docker/Dockerfile.run-base \
           -t hootenanny/run-base \
           $SCRIPT_HOME
}

function maven_cache() {
    if [ ! -d $CACHE/m2/repository -a "${MAVEN_CACHE:-1}" == "1" ]; then
        echo 'Downloading Maven cache'
        curl -sSL -o /var/tmp/m2-cache.tar.gz $MAVEN_CACHE_URL
        echo 'Extracting Maven cache'
        echo "${MAVEN_CACHE_SHA1}  /var/tmp/m2-cache.tar.gz" | sha1sum -c -
        tar -C $CACHE/m2 -xzf /var/tmp/m2-cache.tar.gz
    fi
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

function run_repo_image() {
    local OPTIND opt
    local image=hootenanny/rpmbuild-repo
    local profile=default
    local usage=no

    while getopts ":i:p:" opt; do
        case "${opt}" in
            i)
                image="${OPTARG}"
                ;;
            p)
                profile="${OPTARG}"
                ;;
            *)
                usage=yes
                ;;
        esac
    done
    shift $((OPTIND-1))

    if [ "${usage}" = "yes" ]; then
        echo "run_repo_image: [-i <image>] [-p <awscli profile>]"
    else
        mkdir -p $RPMS $SCRIPT_HOME/el7
        docker run \
               -e AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile ${profile}) \
               -e AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile ${profile}) \
               -v $RPMS:/rpmbuild/RPMS:ro \
               -v $SCRIPT_HOME/el7:/rpmbuild/el7:rw \
               -v $SCRIPT_HOME/scripts:/rpmbuild/scripts:ro \
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
        mkdir -p $SCRIPT_HOME/hootenanny $RPMS $CACHE/m2 $CACHE/npm
        maven_cache
        docker run \
               -v $SOURCES:/rpmbuild/SOURCES:$sources_mode \
               -v $SPECS:/rpmbuild/SPECS:ro \
               -v $RPMS:/rpmbuild/RPMS:rw \
               -v $SCRIPT_HOME/hootenanny:/rpmbuild/hootenanny:rw \
               -v $CACHE/m2:/rpmbuild/.m2:rw \
               -v $CACHE/npm:/rpmbuild/.npm:rw \
               -v $SCRIPT_HOME/scripts:/rpmbuild/scripts:ro \
               --entrypoint $entrypoint \
               -u $user \
               -it --rm \
               $image "${@:-/bin/bash}"
    fi
}
