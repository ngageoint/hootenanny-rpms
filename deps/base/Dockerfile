FROM centos:centos7.4.1708
LABEL \
  description="Base container for building Hootenanny RPMs" \
  maintainer="justin.bronn@digitalglobe.com"
RUN yum -q -y update && \
    yum -q -y install \
        autoconf \
        automake \
        bzip2 \
        cmake \
        epel-release \
        gcc \
        gcc-c++ \
        gdb \
        git \
        git-core \
        libtool \
        make \
        m4 \
        redhat-lsb-core \
        redhat-rpm-config \
        rpm-build \
        unzip \
        vim \
        wget \
        zip
