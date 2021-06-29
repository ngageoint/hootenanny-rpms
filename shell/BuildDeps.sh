#!/bin/bash
set -euxo pipefail

## Get variables.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

# Ensure base images are built.
build_base_images

## Build Hootenanny dependencies.

# glpk
if [ ! -f $RPM_X86_64/$GLPK_RPM ]; then
    echo "#### Building RPM: glpk"

    # Build image for glpk.
    docker build \
           --build-arg "packages=$( spec_requires glpk )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hootenanny/rpmbuild-glpk \
           $SCRIPT_HOME

    # Generate glpk RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-glpk \
        rpmbuild \
        --define "rpmbuild_version $GLPK_VERSION" \
        --define "rpmbuild_release $GLPK_RELEASE" \
        -bb SPECS/glpk.spec
fi

# liboauthcpp
if [ ! -f "$RPM_X86_64/$LIBOAUTHCPP_RPM" ]; then
    echo "#### Building RPM: liboauthcpp"

    # Build image for building liboauthcpp.
    docker build \
           --build-arg "packages=$( spec_requires liboauthcpp )" \
           -f "$SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic" \
           -t hootenanny/rpmbuild-liboauthcpp \
           "$SCRIPT_HOME"

    # Generate liboauthcpp RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-liboauthcpp \
        rpmbuild \
        --define "rpmbuild_version $LIBOAUTHCPP_VERSION" \
        --define "rpmbuild_release $LIBOAUTHCPP_RELEASE" \
        -bb SPECS/liboauthcpp.spec
fi

# libphonenumber
if [ ! -f "$RPM_X86_64/$LIBPHONENUMBER_RPM" ]; then
    echo "#### Building RPM: libphonenumber"

    # Build image for building libphonenumber.
    docker build \
           --build-arg "packages=$( spec_requires libphonenumber )" \
           -f "$SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic" \
           -t hootenanny/rpmbuild-libphonenumber \
           "$SCRIPT_HOME"

    # Generate libphonenumber RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-libphonenumber \
        rpmbuild \
        --define "rpmbuild_version $LIBPHONENUMBER_VERSION" \
        --define "rpmbuild_release $LIBPHONENUMBER_RELEASE" \
        -bb SPECS/libphonenumber.spec
fi

# libpostal
if [ ! -f "$RPM_X86_64/$LIBPOSTAL_RPM" ]; then
    echo "#### Building RPM: libpostal"

    # Build image for building libpostal.
    docker build \
           -f "$SCRIPT_HOME/docker/Dockerfile.rpmbuild-libpostal" \
           -t hootenanny/rpmbuild-libpostal \
           "$SCRIPT_HOME"

    # Generate libpostal RPM; the SOURCES directory needs to be writable
    # because the data files are too large to store here.
    run_dep_image \
        -i hootenanny/rpmbuild-libpostal \
        -s rw \
        rpmbuild \
        --define "rpmbuild_version $LIBPOSTAL_VERSION" \
        --define "rpmbuild_release $LIBPOSTAL_RELEASE" \
        -bb SPECS/libpostal.spec
fi

# NodeJS
if [ ! -f $RPM_X86_64/$NODEJS_RPM ]; then
    echo "#### Building RPM: NodeJS"

    # Build image for building NodeJS.
    docker build \
           --build-arg "packages=$( spec_requires nodejs )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hootenanny/rpmbuild-nodejs \
           $SCRIPT_HOME

    # Generate NodeJS RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-nodejs \
        rpmbuild \
        --define "rpmbuild_version ${NODEJS_VERSION}" \
        --define "rpmbuild_release ${NODEJS_RELEASE}" \
        -bb SPECS/nodejs.spec
fi

## Simple Dependencies

# dumb-init
if [ ! -f $RPM_X86_64/$DUMBINIT_RPM ]; then
    echo "#### Building RPM: dumb-init"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${DUMBINIT_VERSION}" \
        --define "rpmbuild_release ${DUMBINIT_RELEASE}" \
        -bb SPECS/dumb-init.spec
fi

# hoot-words
if [ ! -f $RPM_NOARCH/$WORDS_RPM ]; then
    echo "#### Building RPM: hoot-words"

    # Generate hoot-words RPM, but make SOURCES writable as the dictionary
    # file is a download and too big for version control.
    run_dep_image \
        -s rw \
        rpmbuild \
        --define "rpmbuild_version ${WORDS_VERSION}" \
        --define "rpmbuild_release ${WORDS_RELEASE}" \
        -bb SPECS/hoot-words.spec
fi

# osmosis
if [ ! -f $RPM_NOARCH/$OSMOSIS_RPM ]; then
    echo "#### Building RPM: osmosis"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${OSMOSIS_VERSION}" \
        --define "rpmbuild_release ${OSMOSIS_RELEASE}" \
        -bb SPECS/osmosis.spec
fi

# stxxl
if [ ! -f $RPM_X86_64/$STXXL_RPM ]; then
    echo "#### Building RPM: stxxl"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${STXXL_VERSION}" \
        --define "rpmbuild_release ${STXXL_RELEASE}" \
        -bb SPECS/stxxl.spec
fi

# su-exec
if [ ! -f $RPM_X86_64/$SUEXEC_RPM ]; then
    echo "#### Building RPM: su-exec"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${SUEXEC_VERSION}" \
        --define "rpmbuild_release ${SUEXEC_RELEASE}" \
        -bb SPECS/su-exec.spec
fi

# tomcat8
if [ ! -f $RPM_NOARCH/$TOMCAT8_RPM ]; then
    echo "#### Building RPM: tomcat8"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${TOMCAT8_VERSION}" \
        --define "rpmbuild_release ${TOMCAT8_RELEASE}" \
        -bb SPECS/tomcat8.spec
fi

# wamerican-insane
if [ ! -f $RPM_NOARCH/$WAMERICAN_RPM ]; then
    echo "#### Building RPM: wamerican-insane"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${WAMERICAN_VERSION}" \
        --define "rpmbuild_release ${WAMERICAN_RELEASE}" \
        -bb SPECS/wamerican-insane.spec
fi
