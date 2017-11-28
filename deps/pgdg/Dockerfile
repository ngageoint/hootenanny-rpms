FROM hoot/rpmbuild-base:latest
LABEL \
  description="PostgreSQL (PGDG) container for building Hootenanny RPMs" \
  maintainer="justin.bronn@digitalglobe.com"

ARG dist=.el7
ARG packages
ARG pg_version=9.5
ARG rpmbuild_uid=1000
ARG rpmbuild_user=rpmbuild
ARG rpmbuild_home=/${rpmbuild_user}

ADD pgdg-install.sh /tmp/pgdg-install.sh

# If any package dependencies are needed, install them.
RUN /tmp/pgdg-install.sh ${pg_version} && \
    rm /tmp/pgdg-install.sh && \
    yum -q -y install postgresql$(echo ${pg_version} | tr -d '.')-devel && \
    if [ ! -z "${packages}" ] ; then yum -q -y install ${packages}; fi

# Create unprivileged user for building RPMs.
RUN useradd -d ${rpmbuild_home} -m -s /bin/bash -u ${rpmbuild_uid} ${rpmbuild_user}
USER ${rpmbuild_user}
WORKDIR ${rpmbuild_home}

# Add basic configuration to build user's RPM macros.
RUN echo "%_smp_mflags -j%(nproc)" >> ${rpmbuild_home}/.rpmmacros && \
    echo "%_topdir ${rpmbuild_home}" >> ${rpmbuild_home}/.rpmmacros && \
    echo "%debug_package %{nil}" >> ${rpmbuild_home}/.rpmmacros && \
    echo "%dist ${dist}" >> ${rpmbuild_home}/.rpmmacros
