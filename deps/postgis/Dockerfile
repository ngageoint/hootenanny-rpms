FROM hoot/rpmbuild-gdal:latest

# GDAL version, including release iteration (e.g., '2.1.4-1') is
# a required argument.
ARG gdal_version
ARG packages

LABEL \
  description="Container for building Hootenanny PostGIS RPMs with GDAL ${gdal_version}" \
  maintainer="justin.bronn@digitalglobe.com" \
  name="Hootenanny PostGIS RPM Build Image" \
  vendor="Radiant Solutions"

# Temporarily switch to root for package installation.
USER root

# Copy in GDAL dependency RPMs.
COPY src/RPMS/x86_64/hoot-gdal-${gdal_version}${RPMBUILD_DIST}.x86_64.rpm \
     src/RPMS/x86_64/hoot-gdal-devel-${gdal_version}${RPMBUILD_DIST}.x86_64.rpm \
     src/RPMS/x86_64/hoot-gdal-libs-${gdal_version}${RPMBUILD_DIST}.x86_64.rpm \
     /tmp/

# Install GDAL prerequisites first, before installing the package list
# so they take precedence over packages from other repositories.
RUN yum install -y \
    /tmp/hoot-gdal-${gdal_version}${RPMBUILD_DIST}.x86_64.rpm \
    /tmp/hoot-gdal-devel-${gdal_version}${RPMBUILD_DIST}.x86_64.rpm \
    /tmp/hoot-gdal-libs-${gdal_version}${RPMBUILD_DIST}.x86_64.rpm \
    && \
    rm -f /*.rpm

# Install any other extra packages.
RUN if [ ! -z "${packages}" ] ; then yum -q -y install ${packages}; fi

# Switch back to default RPM building user.
USER ${RPMBUILD_USER}

# Disable use of the SFCGAL library.
RUN echo "%sfcgal 0" >> $RPMBUILD_HOME/.rpmmacros
