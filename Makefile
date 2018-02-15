RPMBUILD_DIST := .el7

## Macro functions.

config_version = $(shell cat config.yml | grep '\&$(1)_version' | awk '{ print $$3 }' | tr -d "'")
rpm_file = RPMS/$(2)/$(1)-$(call config_version,$(1))$(RPMBUILD_DIST).$(2).rpm
rpm_package = $(shell echo $(1) | awk '{ split($$0, a, "-"); l = length(a); pkg = a[1]; for (i=2; i<l-1; ++i) pkg = pkg "-" a[i]; print pkg}')
container_id = .vagrant/machines/$(1)/docker/id
docker_ps = docker ps -q --filter id=$$(cat $(call container_id,$(1))) --filter status=running

## RPM Versions and locations.

GEOS_RPM := $(call rpm_file,geos,x86_64)
FILEGDBAPI_RPM := $(call rpm_file,FileGDBAPI,x86_64)
LIBGEOTIFF_RPM := $(call rpm_file,libgeotiff,x86_64)
LIBKML_RPM := $(call rpm_file,libkml,x86_64)


.PHONY: all base clean


all:
	@echo $(generic_containers)


base:  rpmbuild-generic


clean:
	vagrant destroy -f --no-parallel || true


## Build Containers

rpmbuild: .vagrant/machines/rpmbuild/docker/id


rpmbuild-base: \
	rpmbuild \
	.vagrant/machines/rpmbuild-base/docker/id


rpmbuild-generic: \
	rpmbuild-base \
	.vagrant/machines/rpmbuild-generic/docker/id

rpmbuild-geos: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-geos/docker/id


rpmbuild-libgeotiff: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-gdal/docker/id


rpmbuild-libkml: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-libkml/docker/id


rpmbuild-gdal: \
	FileGDBAPI \
	rpmbuild-geos \
	rpmbuild-libgeotiff \
	rpmbuild-libkml \
	.vagrant/machines/rpmbuild-gdal/docker/id


rpmbuild-pgdg: \
	rpmbuild-generic \
	.vagrant/machines/rpmbuild-pgdg/docker/id


rpmbuild-repo: \
	rpmbuild \
	.vagrant/machines/rpmbuild-repo/docker/id


## RPMS

geos: rpmbuild-geos $(GEOS_RPM)
libgeotiff: rpmbuild-libgeotiff $(LIBGEOTIFF_RPM)
libkml: rpmbuild-libkml $(LIBKML_RPM)
FileGDBAPI: rpmbuild-generic $(FILEGDBAPI_RPM)


## General patterns.

# Vagrant creates a file with the Docker UUID in it.
.vagrant/machines/%/docker/id:
	vagrant up $*


# Runs container and waits for its container to exit.
RPMS/x86_64/%.rpm RPMS/noarch/%.rpm:
	vagrant up $(call rpm_package,$*)
	@echo -n "Creating the $(call rpm_package,$*) RPM "
	@while test "$$($(call docker_ps,$(call rpm_package,$*)) | wc -l)" != "0"; do echo -n '.' && sleep 1; done
	@echo " done."

#while true; do echo '.'; sleep 1; done


