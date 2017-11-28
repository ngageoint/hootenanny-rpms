FROM hoot/rpmbuild-base:latest
LABEL \
  description="PostgreSQL (PGDG) container for building Hootenanny RPMs" \
  maintainer="justin.bronn@digitalglobe.com"

ARG packages
ARG pg_version=9.5
ENV PG_VERSION=${pg_version}

# Install PostgreSQL development files from PGDG for the desired version
# as well as any additional packages.
COPY pgdg-install.sh /tmp/pgdg-install.sh
RUN /tmp/pgdg-install.sh ${pg_version} && \
    rm /tmp/pgdg-install.sh && \
    yum -q -y install postgresql$(echo ${pg_version} | tr -d '.')-devel && \
    alternatives --install /usr/bin/pg_config pgsql-pg_config /usr/pgsql-${pg_version}/bin/pg_config 500 && \
    if [ ! -z "${packages}" ] ; then yum -q -y install ${packages}; fi

# Set default user and work directory.
USER ${RPMBUILD_USER}
WORKDIR ${RPMBUILD_HOME}
