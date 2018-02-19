DOCKER ?= docker
VAGRANT ?= vagrant
RPMBUILD_DIST := .el7


## Macro functions.

# All versions use a YAML reference so they only have to be defined once,
# just grep for this reference and print it out.
config_version = $(shell cat config.yml | grep '\&$(1)_version' | awk '{ print $$3 }' | tr -d "'")

# Where Vagrant puts the Docker container id after it's been created.
container_id = .vagrant/machines/$(1)/docker/id

# Follows the docker logs for the given container.
docker_logs = $(DOCKER) logs --follow $$(cat $(call container_id,$(1)))

# Gets the latest Hootenanny archive.
latest_hoot_archive = $(shell ls -1t SOURCES/hootenanny-[0-9]*.tar.gz | head -n1)
latest_hoot_version_gen = $(subst SOURCES/hootenanny-,,$(subst .tar.gz,,$(call latest_hoot_archive)))

# Variants for getting RPM file names.
rpm_file = RPMS/$(2)/$(1)-$(call config_version,$(1))$(RPMBUILD_DIST).$(2).rpm
rpm_file2 = RPMS/$(3)/$(1)-$(call config_version,$(2))$(RPMBUILD_DIST).$(3).rpm

# Gets the RPM package name from the filename.
rpm_package = $(shell echo $(1) | awk '{ split($$0, a, "-"); l = length(a); pkg = a[1]; for (i=2; i<l-1; ++i) pkg = pkg "-" a[i]; print pkg}')

## RPM variables.

PG_DOTLESS := $(shell echo $(call config_version,pg) | tr -d '.')

DUMBINIT_RPM := $(call rpm_file2,dumb-init,dumbinit,x86_64)
GEOS_RPM := $(call rpm_file,geos,x86_64)
GDAL_RPM := $(call rpm_file2,hoot-gdal,gdal,x86_64)
FILEGDBAPI_RPM := $(call rpm_file,FileGDBAPI,x86_64)
LIBGEOTIFF_RPM := $(call rpm_file,libgeotiff,x86_64)
LIBKML_RPM := $(call rpm_file,libkml,x86_64)
NODEJS_RPM := $(call rpm_file,nodejs,x86_64)
OSMOSIS_RPM := $(call rpm_file,osmosis,noarch)
POSTGIS_RPM := $(call rpm_file2,hoot-postgis23_$(PG_DOTLESS),postgis,x86_64)
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
	rpmbuild-libgeotiff \
	rpmbuild-libkml \
	rpmbuild-postgis \
	rpmbuild-nodejs

REPO_CONTAINERS := \
	rpmbuild-repo

DEPENDENCY_RPMS := \
		dumb-init \
		FileGDBAPI \
		geos \
		libgeotiff \
		libkml \
		hoot-gdal \
		hoot-postgis23_$(PG_DOTLESS) \
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
	run-base \
	run-base-release

# These may be overridden with environment variables.
BUILD_IMAGE ?= rpmbuild-hoot-release
GIT_COMMIT ?= develop
RUN_IMAGE ?= run-base-release

HOOT_VERSION_GEN ?= $(call latest_hoot_version_gen)
HOOT_ARCHIVE := SOURCES/hootenanny-$(HOOT_VERSION_GEN).tar.gz

## Main targets.

.PHONY: \
	all \
	base \
	clean \
	deps \
	hoot-archive \
	hoot-rpm \
	$(BUILD_CONTAINERS) \
	$(DEPENDENCY_CONTAINERS) \
	$(DEPENDENCY_RPMS) \
	$(REPO_CONTAINERS) \
	$(RUN_CONTAINERS)

all: $(BUILD_CONTAINERS)

base: $(BASE_CONTAINERS)

clean:
	$(VAGRANT) destroy -f --no-parallel || true
	rm -fr RPMS/noarch RPMS/x86_64

deps: \
	$(DEPENDENCY_CONTAINERS) \
	$(DEPENDENCY_RPMS)

hoot-archive: $(BUILD_IMAGE)
	$(VAGRANT) docker-run $(BUILD_IMAGE) -- \
	/bin/bash -c "/rpmbuild/scripts/hoot-checkout.sh $(GIT_COMMIT) && /rpmbuild/scripts/hoot-archive.sh"

hoot-rpm: $(BUILD_IMAGE)
	$(VAGRANT) docker-run $(BUILD_IMAGE) -- \
	rpmbuild \
	  --define "hoot_version_gen $(HOOT_VERSION_GEN)" \
	  --define "geos_version %(rpm -q --queryformatn '%%{version} geos)" \
	  --define "gdal_version %(rpm -q --queryformat '%%{version}' hoot-gdal)" \
	  --define "glpk_version %(rpm -q --queryformat '%%{version}' glpk)" \
	  --define "nodejs_version %(rpm -q --queryformat '%%{version}' nodejs)" \
	  --define "stxxl_version %(rpm -q --queryformat '%%{version}' stxxl)" \
	  --define "tomcat_version %(rpm -q --queryformat '%%{version}' tomcat8)" \
	  -bb SPECS/hootenanny.spec

#$(call latest_hoot_archive)
## Container targets.

rpmbuild: .vagrant/machines/rpmbuild/docker/id

rpmbuild-base: \
	rpmbuild \
	.vagrant/machines/rpmbuild-base/docker/id

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

rpmbuild-hoot-devel: \
	rpmbuild-pgdg \
	dumb-init \
	FileGDBAPI \
	geos \
	hoot-gdal \
	hoot-postgis23_$(PG_DOTLESS) \
	hoot-words \
	libgeotiff \
	libkml \
	nodejs \
	stxxl \
	su-exec \
	tomcat8 \
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

# Runtime containers
run-base: .vagrant/machines/run-base/docker/id

run-base-release: \
	run-base \
	.vagrant/machines/rpmbuild-base-release/docker/id


## RPM targets.

dumb-init: rpmbuild-generic $(DUMBINIT_RPM)
geos: rpmbuild-geos $(GEOS_RPM)
FileGDBAPI: rpmbuild-generic $(FILEGDBAPI_RPM)
libgeotiff: rpmbuild-libgeotiff $(LIBGEOTIFF_RPM)
libkml: rpmbuild-libkml $(LIBKML_RPM)
nodejs: rpmbuild-nodejs $(NODEJS_RPM)
hoot-gdal: rpmbuild-gdal $(GDAL_RPM)
hoot-words: rpmbuild-generic $(WORDS_RPM)
hoot-postgis23_$(PG_DOTLESS): rpmbuild-postgis $(POSTGIS_RPM)
osmosis: rpmbuild-generic $(OSMOSIS_RPM)
stxxl: rpmbuild-generic $(STXXL_RPM)
su-exec: rpmbuild-generic $(SUEXEC_RPM)
tomcat8: rpmbuild-generic $(TOMCAT8_RPM)
wamerican-insane: rpmbuild-generic $(WAMERICAN_RPM)


## Build patterns.

# Runs container and follow logs until it completes.
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	$(VAGRANT) up $(call rpm_package,$*)
	$(call docker_logs,$(call rpm_package,$*))

.vagrant/machines/%/docker/id:
	$(VAGRANT) up $*
