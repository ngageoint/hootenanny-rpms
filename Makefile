DOCKER ?= docker
VAGRANT ?= vagrant
RPMBUILD_DIST := .el7


## Macro functions.

config_version = $(shell cat config.yml | grep '\&$(1)_version' | awk '{ print $$3 }' | tr -d "'")
container_id = .vagrant/machines/$(1)/docker/id
docker_logs = $(DOCKER) logs --follow $$(cat $(call container_id,$(1)))
rpm_file = RPMS/$(2)/$(1)-$(call config_version,$(1))$(RPMBUILD_DIST).$(2).rpm
rpm_file2 = RPMS/$(3)/$(1)-$(call config_version,$(2))$(RPMBUILD_DIST).$(3).rpm
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


## Main targets.

.PHONY: \
	all \
	base \
	deps \
	clean \
	$(DEPENDENCY_CONTAINERS) \
	$(DEPENDENCY_RPMS) \
	$(REPO_CONTAINERS)

all: base

base: $(BASE_CONTAINERS)

deps: \
	$(DEPENDENCY_CONTAINERS) \
	$(DEPENDENCY_RPMS)

clean:
	$(VAGRANT) destroy -f --no-parallel || true
	rm -fr RPMS/noarch RPMS/x86_64

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
su-exec: rpmbuild-generic $(SUEXEC_RPM)
tomcat8: rpmbuild-generic $(TOMCAT8_RPM)
wamerican-insane: rpmbuild-generic $(WAMERICAN_RPM)

## Build patterns.

# Vagrant creates a file with the Docker UUID in it.
.vagrant/machines/%/docker/id:
	$(VAGRANT) up $*

# Runs container and follow logs until it completes.
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	$(VAGRANT) up $(call rpm_package,$*)
	$(call docker_logs,$(call rpm_package,$*))
