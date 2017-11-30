# The base image depends on the version of PosgreSQL from PGDG.
ARG pg_version
FROM hoot/rpmbuild-pgdg:${pg_version}
LABEL \
  description="Container for building Hootenanny GDAL RPMs" \
  maintainer="justin.bronn@digitalglobe.com"

# Our GDAL package depends on RPMs we build; the desired package
# versions, *including* the release iteration (e.g, '1.0.0-1') are
# required arguments.
ARG filegdbapi_version
ARG geos_version
ARG libgeotiff_version
ARG libkml_version
ARG packages

# Switch to root temporarily for dependency installs.
USER root

# Copy in dependency RPMs.
COPY FileGDBAPI-${filegdbapi_version}${RPMBUILD_DIST}.x86_64.rpm \
     geos-${geos_version}${RPMBUILD_DIST}.x86_64.rpm \
     geos-devel-${geos_version}${RPMBUILD_DIST}.x86_64.rpm \
     libgeotiff-${libgeotiff_version}${RPMBUILD_DIST}.x86_64.rpm \
     libgeotiff-devel-${libgeotiff_version}${RPMBUILD_DIST}.x86_64.rpm \
     libkml-${libkml_version}${RPMBUILD_DIST}.x86_64.rpm \
     libkml-devel-${libkml_version}${RPMBUILD_DIST}.x86_64.rpm \
     /tmp/

# Install GDAL prerequisites first, before installing the package list
# so they take precedence over packages from other repositories.
RUN yum install -y \
    /tmp/FileGDBAPI-${filegdbapi_version}${RPMBUILD_DIST}.x86_64.rpm \
    /tmp/geos-${geos_version}${RPMBUILD_DIST}.x86_64.rpm \
    /tmp/geos-devel-${geos_version}${RPMBUILD_DIST}.x86_64.rpm \
    /tmp/libgeotiff-${libgeotiff_version}${RPMBUILD_DIST}.x86_64.rpm \
    /tmp/libgeotiff-devel-${libgeotiff_version}${RPMBUILD_DIST}.x86_64.rpm \
    /tmp/libkml-${libkml_version}${RPMBUILD_DIST}.x86_64.rpm \
    /tmp/libkml-devel-${libkml_version}${RPMBUILD_DIST}.x86_64.rpm \
    && \
    rm -f /*.rpm

# Install any additionally requested packages.
RUN if [ ! -z "${packages}" ] ; then yum -y install ${packages}; fi

# Switch back to RPM build user.
USER ${RPMBUILD_USER}

# Add in RPM macros necessary for creating the GDAL package.
RUN echo "%pg_version ${PG_VERSION}" >> $RPMBUILD_HOME/.rpmmacros && \
    echo "%pg_dotless %(echo %{pg_version} | tr -d '.')" >> $RPMBUILD_HOME/.rpmmacros && \
    echo "%pginstdir /usr/pgsql-%{pg_version}" >> $RPMBUILD_HOME/.rpmmacros
