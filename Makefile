# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
# Copyright (C) 2016, 2017 DigitalGlobe (http://www.digitalglobe.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Default commands for Docker and Vagrant.
DOCKER ?= docker
VAGRANT ?= vagrant

## Macro functions.

# All versions use a YAML reference so they only have to be defined once,
# just grep for this reference and print it out.
config_reference = $(shell cat config.yml | grep '\&$(1)' | awk '{ print $$3 }' | tr -d "'")
config_version = $(call config_reference,$(1)_version)

# Where Vagrant puts the Docker container id after it's been created.
container_id = .vagrant/machines/$(1)/docker/id

# Follows the docker logs for the given container.
docker_logs = $(DOCKER) logs --follow $$(cat $(call container_id,$(1)))

# Returns the version tag reference from HOOT_VERSION_GEN, for example:
#  $(call hoot_version_tag,0.2.38_23_gdadada1) -> 0.2.38
hoot_version_tag = $(shell echo $(1) | awk -F_ '{ print $$1 }')

# Returns the extra version information from HOOT_VERSION_GEN, which indicates
# how many commits away from the latest release tag the git commit is:
#  $(call hoot_extra_version,0.2.38_23_gdadada1) -> 23
hoot_extra_version = $(shell echo $(1) | awk -F_ '{ print $$2 }')

# Returns git commit from HOOT_VERSION_GEN.  For example:
#  $(call hoot_extra_version,0.2.38_23_gdadada1) -> dadada1
hoot_git_revision = $(shell echo $(1) | awk -F_ '{ print substr($$3, 2) }')

# Returns the full RPM version, including a release that's pre-release and
# and includes Fedora-standard VCS snapshot information, for example:
#   $(call hoot_devel_version,0.2.38_23_gdadada1) -> 0.2.39-0.23.20180222.dadada1
hoot_devel_version = $(shell echo $(shell echo $(call hoot_version_tag,$(1)) | awk -F. '{ print $$1 "." $$2 "." ($$3 + 1) }')-0.$(call hoot_extra_version,$(1)).$(shell date -u +%Y%m%d).$(call hoot_git_revision,$(1)))

# Uses `find`, instead of `ls` (errors when no files are found) to get the
# latest file from the directory in the first parameter and matches the
# pattern in the second parameter.
latest_file = $(shell find $(1) -type f -name $(2) -printf '%T+\t%p\n' | sort -r | awk '{ print $$2 }' | head -n 1)

# Gets the latest Hootenanny archive.
latest_hoot_archive = $(call latest_file,SOURCES,hootenanny-[0-9]\*.tar.gz)
latest_hoot_version_gen = $(subst SOURCES/hootenanny-,,$(subst .tar.gz,,$(call latest_hoot_archive)))

# Variants for getting RPM file names.
RPMBUILD_DIST := $(call config_reference,rpmbuild_dist)
rpm_file = RPMS/$(2)/$(1)-$(call config_version,$(1))$(RPMBUILD_DIST).$(2).rpm
rpm_file2 = RPMS/$(3)/$(1)-$(call config_version,$(2))$(RPMBUILD_DIST).$(3).rpm

# Gets the RPM package name from the filename.
rpm_package = $(shell echo $(1) | awk '{ split($$0, a, "-"); l = length(a); pkg = a[1]; for (i=2; i<l-1; ++i) pkg = pkg "-" a[i]; print pkg }')

## RPM variables.

PG_DOTLESS := $(shell echo $(call config_version,pg) | tr -d '.')

DUMBINIT_RPM := $(call rpm_file2,dumb-init,dumbinit,x86_64)
GEOS_RPM := $(call rpm_file,geos,x86_64)
GDAL_RPM := $(call rpm_file2,hoot-gdal,gdal,x86_64)
GLPK_RPM := $(call rpm_file,glpk,x86_64)
FILEGDBAPI_RPM := $(call rpm_file,FileGDBAPI,x86_64)
LIBGEOTIFF_RPM := $(call rpm_file,libgeotiff,x86_64)
LIBKML_RPM := $(call rpm_file,libkml,x86_64)
NODEJS_RPM := $(call rpm_file,nodejs,x86_64)
OSMOSIS_RPM := $(call rpm_file,osmosis,noarch)
POSTGIS_RPM := $(call rpm_file2,hoot-postgis24_$(PG_DOTLESS),postgis,x86_64)
STXXL_RPM := $(call rpm_file,stxxl,x86_64)
SUEXEC_RPM := $(call rpm_file2,su-exec,suexec,x86_64)
TOMCAT8_RPM := $(call rpm_file,tomcat8,noarch)
WAMERICAN_RPM := $(call rpm_file2,wamerican-insane,wamerican,noarch)
WORDS_RPM := $(call rpm_file2,hoot-words,words,noarch)

BASE_CONTAINERS := \
	rpmbuild \
	rpmbuild-base \
	rpmbuild-generic \
	rpmbuild-pgdg

DEPENDENCY_CONTAINERS := \
	$(BASE_CONTAINERS) \
	rpmbuild-gdal \
	rpmbuild-geos \
	rpmbuild-glpk \
	rpmbuild-libgeotiff \
	rpmbuild-libkml \
	rpmbuild-postgis \
	rpmbuild-nodejs

OTHER_CONTAINERS := \
	rpmbuild-lint \
	rpmbuild-repo \
	rpmbuild-sonarqube

DEPENDENCY_RPMS := \
	dumb-init \
	FileGDBAPI \
	geos \
	glpk \
	libgeotiff \
	libkml \
	hoot-gdal \
	hoot-postgis24_$(PG_DOTLESS) \
	hoot-words \
	nodejs \
	osmosis \
	stxxl \
	su-exec \
	tomcat8 \
	wamerican-insane

# Hootenanny RPM variables.
BUILD_CONTAINERS := \
	rpmbuild-hoot-devel \
	rpmbuild-hoot-release

RUN_CONTAINERS := \
	run \
	run-base \
	run-base-devel \
	run-base-release

# These may be overridden with environment variables.
BUILD_IMAGE ?= rpmbuild-hoot-release
RUN_IMAGE ?= run-base-release

# Are there any archives?
HOOT_VERSION_GEN ?= $(call latest_hoot_version_gen)
DEFAULT_ARCHIVE := SOURCES/hootenanny-archive.tar.gz

ifeq ($(strip $(HOOT_VERSION_GEN)),)
# Setup a dummy archive file that will force making of an archive
# from the revision specified in GIT_COMMIT.
HOOT_ARCHIVE := $(DEFAULT_ARCHIVE)
# don't define `HOOT_VERSION`, or `HOOT_RPM`.
$(warning HOOT_VERSION_GEN is not defined)
else
HOOT_ARCHIVE := SOURCES/hootenanny-$(HOOT_VERSION_GEN).tar.gz
ifeq ($(strip $(call hoot_extra_version,$(HOOT_VERSION_GEN))),)
# Release version (HOOT_VERSION_GEN=0.2.38).
HOOT_RELEASE ?= 1
HOOT_VERSION := $(call hoot_version_tag,$(HOOT_VERSION_GEN))-$(HOOT_RELEASE)
else
# Development version (HOOT_VERSION_GEN=0.2.38_23_gdadada1)
HOOT_VERSION := $(call hoot_devel_version,$(HOOT_VERSION_GEN))
ifeq ($(origin HOOT_VERSION_GEN),environment)
GIT_COMMIT := $(call hoot_git_revision,$(HOOT_VERSION_GEN))
endif
endif
HOOT_RPM := RPMS/x86_64/hootenanny-core-$(HOOT_VERSION)$(RPMBUILD_DIST).x86_64.rpm
endif

# Default to develop branch when making archive.
GIT_COMMIT ?= develop

## Main targets.

.PHONY: \
	all \
	archive \
	base \
	clean \
	deps \
	hoot-archive \
	hoot-rpm \
	latest-archive \
	rpm \
	validate \
	$(BUILD_CONTAINERS) \
	$(DEPENDENCY_CONTAINERS) \
	$(DEPENDENCY_RPMS) \
	$(OTHER_CONTAINERS) \
	$(RUN_CONTAINERS)

all: $(BUILD_CONTAINERS)

archive: $(BUILD_IMAGE) $(HOOT_ARCHIVE)

base: $(BASE_CONTAINERS)

clean:
	$(VAGRANT) destroy -f --no-parallel || true
	rm -fr RPMS/noarch RPMS/x86_64 SOURCES/hootenanny-[0-9]*.tar.gz

deps: \
	$(DEPENDENCY_CONTAINERS) \
	$(DEPENDENCY_RPMS)

hoot-archive: archive

latest-archive: $(DEFAULT_ARCHIVE)

# Only allow building an RPM when an archive already exists corresponding
# to the HOOT_VERSION_GEN.
ifdef HOOT_RPM
rpm: $(BUILD_IMAGE) $(HOOT_RPM)
else
rpm:
	$(error Cannot build RPM without an input archive.  Run 'make archive' first)
endif

hoot-rpm: rpm

## Container targets.

rpmbuild: .vagrant/machines/rpmbuild/docker/id

rpmbuild-base: \
	rpmbuild \
	.vagrant/machines/rpmbuild-base/docker/id

rpmbuild-lint: \
	rpmbuild \
	.vagrant/machines/rpmbuild-lint/docker/id

rpmbuild-generic: \
	rpmbuild-base \
	.vagrant/machines/rpmbuild-generic/docker/id

# GDAL container requires GEOS, FileGDBAPI, libgeotiff, and libkml RPMs.
rpmbuild-gdal: \
	rpmbuild-pgdg \
	FileGDBAPI \
	geos \
	libgeotiff \
	libkml \
	.vagrant/machines/rpmbuild-gdal/docker/id

rpmbuild-geos: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-geos/docker/id

rpmbuild-glpk: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-glpk/docker/id

rpmbuild-hoot-devel: \
	rpmbuild-pgdg \
	$(DEPENDENCY_RPMS) \
	.vagrant/machines/rpmbuild-hoot-devel/docker/id

rpmbuild-hoot-release: \
	rpmbuild-pgdg \
	.vagrant/machines/rpmbuild-hoot-release/docker/id

rpmbuild-libgeotiff: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-libgeotiff/docker/id

rpmbuild-libkml: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-libkml/docker/id

rpmbuild-nodejs: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-nodejs/docker/id

rpmbuild-pgdg: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-pgdg/docker/id

# PostGIS container requires GDAL RPMs.
rpmbuild-postgis: \
	hoot-gdal \
	.vagrant/machines/rpmbuild-postgis/docker/id

rpmbuild-repo: \
	rpmbuild \
	.vagrant/machines/rpmbuild-repo/docker/id

rpmbuild-sonarqube: \
	rpmbuild-hoot-release \
	.vagrant/machines/rpmbuild-sonarqube/docker/id

# Runtime containers
run-base: .vagrant/machines/run-base/docker/id

run-base-devel: \
	run-base \
	$(DEPENDENCY_RPMS) \
	.vagrant/machines/run-base-devel/docker/id

run-base-release: \
	run-base \
	.vagrant/machines/run-base-release/docker/id

run: $(RUN_IMAGE)
	$(DOCKER) build \
	--build-arg from_image=hootenanny/$(RUN_IMAGE) \
	--build-arg hoot_version=$(HOOT_VERSION) \
	--build-arg hoot_dist=$(RPMBUILD_DIST) \
	-f docker/Dockerfile.run \
	-t hootenanny/run:$(HOOT_VERSION) \
	.

validate:
	MAVEN_CACHE=0 $(VAGRANT) validate

## Dependency RPM targets.

dumb-init: rpmbuild-generic $(DUMBINIT_RPM)
geos: rpmbuild-geos $(GEOS_RPM)
FileGDBAPI: rpmbuild-generic $(FILEGDBAPI_RPM)
libgeotiff: rpmbuild-libgeotiff $(LIBGEOTIFF_RPM)
libkml: rpmbuild-libkml $(LIBKML_RPM)
nodejs: rpmbuild-nodejs $(NODEJS_RPM)
glpk: rpmbuild-glpk $(GLPK_RPM)
hoot-gdal: rpmbuild-gdal $(GDAL_RPM)
hoot-words: rpmbuild-generic $(WORDS_RPM)
hoot-postgis24_$(PG_DOTLESS): rpmbuild-postgis $(POSTGIS_RPM)
osmosis: rpmbuild-generic $(OSMOSIS_RPM)
stxxl: rpmbuild-generic $(STXXL_RPM)
su-exec: rpmbuild-generic $(SUEXEC_RPM)
tomcat8: rpmbuild-generic $(TOMCAT8_RPM)
wamerican-insane: rpmbuild-generic $(WAMERICAN_RPM)

## Build patterns.

# Builds a container with Vagrant.
.vagrant/machines/%/docker/id:
	$(VAGRANT) up $*

# Builds a Hootenanny RPM from the HOOT_ARCHIVE.
RPMS/x86_64/hootenanny-%.rpm: .vagrant/machines/$(BUILD_IMAGE)/docker/id
	$(VAGRANT) docker-run $(BUILD_IMAGE) -- \
	rpmbuild \
	  --define "hoot_version_gen $(HOOT_VERSION_GEN)" \
	  --define "geos_version %(rpm -q --queryformat '%%{version}' geos)" \
	  --define "glpk_version %(rpm -q --queryformat '%%{version}' glpk)" \
	  --define "gdal_version %(rpm -q --queryformat '%%{version}' hoot-gdal)" \
	  --define "nodejs_version %(rpm -q --queryformat '%%{version}' nodejs)" \
	  --define "stxxl_version %(rpm -q --queryformat '%%{version}' stxxl)" \
	  --define "tomcat_version %(rpm -q --queryformat '%%{version}' tomcat8)" \
	  -bb SPECS/hootenanny.spec

# Runs container and follow logs until it completes.
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	$(VAGRANT) up $(call rpm_package,$*)
	$(call docker_logs,$(call rpm_package,$*))

# Build an archive using the build image.
SOURCES/hootenanny-%.tar.gz:
	$(VAGRANT) docker-run $(BUILD_IMAGE) -- \
	/bin/bash -c "/rpmbuild/scripts/hoot-checkout.sh $(GIT_COMMIT) && /rpmbuild/scripts/hoot-archive.sh"
