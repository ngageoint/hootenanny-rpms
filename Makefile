TARBALLS := $(wildcard SOURCES/hootenanny*.tar.gz)
DOCBALLS := $(wildcard SOURCES/hootenanny*-documentation.tar.gz)
HOOTBALL := $(filter-out $(DOCBALLS), $(TARBALLS))

# Synchronizing the make build with rpmbuild parallel flags causes problems. This way we
# spawn at most nproc processes per sub-job and if the load is above nproc + 2 no more
# jobs will be spawned. This is a poor man parallelism, but should avoid killing the
# host.
RPMBUILD_OPTS=--define '%_topdir %(pwd)' --define '%_smp_mflags -j%(nproc) -l%(expr %(nproc) + 2)'

#Trying this
RPM_OPT_FLAGS=--std=c++11

hoottarball=$(lastword $(sort $(HOOTBALL)))

hootversion=$(patsubst SOURCES/hootenanny-%.tar.gz,%,$(hoottarball))

HOOT_RPM=RPMS/x86_64/hootenanny-core-$(hootversion).el7.x86_64.rpm

all: hoot

clean: clean-hoot
	rm -rf tmp BUILD/* BUILDROOT/* SRPMS/* RPMS/*

# Clean out all hoot specific RPMs and build files.
clean-hoot:
	rm -rf BUILD/hoot* BUILDROOT/hoot* SRPMS/hoot* RPMS/x86_64/hoot*
# touch was sometimes cropping down to second resolution
	echo > $@

hoot: $(HOOT_RPM)

# Just run the install part.
hoot-test-install: $(HOOTBALL)
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) --short-circuit -bi SPECS/hootenanny.spec

# Just run the binary package part.
hoot-test-package: $(HOOTBALL)
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) --short-circuit -bb SPECS/hootenanny.spec

$(HOOT_RPM): $(HOOTBALL)
	test $(words $(HOOTBALL)) == 0 && (echo "Did not find a hoot tarball in SOURCES. Do you need to download one? https://github.com/ngageoint/hootenanny/releases"; exit 1) || true
	test $(words $(HOOTBALL)) == 1 || (echo "Found more than 1 hoot tarball please remove the extra tarballs. $(HOOTBALL)"; exit 1)
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba SPECS/hootenanny.spec
