FROM hoot/rpmbuild-base:latest
LABEL \
  description="Generic container for building Hootenanny dependency RPMs" \
  maintainer="justin.bronn@digitalglobe.com"

ARG packages

# If any package dependencies are needed, install them.
RUN if [ ! -z "${packages}" ] ; then yum -q -y install ${packages}; fi

USER ${RPMBUILD_USER}
WORKDIR ${RPMBUILD_HOME}
