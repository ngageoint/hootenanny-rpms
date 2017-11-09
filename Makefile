
# Default branch of hoot to build
GIT_COMMIT?=origin/develop

TARBALLS := $(wildcard src/SOURCES/hootenanny*.tar.gz)
DOCBALLS := $(wildcard src/SOURCES/hootenanny*-documentation.tar.gz)
HOOTBALL := $(filter-out $(DOCBALLS), $(TARBALLS))

all: copy-rpms

# a convenience target for building hoot RPMs and no others.
hoot-rpms:
	cd src; $(MAKE) hoot

force:

# Clean out all the RPMs
clean: clean-hoot
	cd src; $(MAKE) clean

# Clean out everything
clean-all: vagrant-clean clean

# Cleans out the RPM el7 stash, archive hoot, and all the hoot source/rpms
clean-hoot:
	rm -rf el7
	rm -rf tmp/hootenanny
	cd src; $(MAKE) clean-hoot

ValidHootTarball:
	test $(words $(HOOTBALL)) != 1 && (echo "Did not find exactly one hoot tarball in SOURCES. Too many? Do you need to download one? https://github.com/ngageoint/hootenanny/releases"; exit -1) || true

vagrant-build-up:
	vagrant up

vagrant-build: vagrant-build-up vagrant-build-deps vagrant-build-archive
	vagrant ssh -c "cd hootenanny-rpms && make -j$$((`nproc` + 2))"

vagrant-build-deps: vagrant-build-up
	vagrant ssh -c "cd hootenanny-rpms && ./BuildDeps.sh"

vagrant-build-archive: vagrant-build-up
	vagrant ssh -c "export GIT_COMMIT=$(GIT_COMMIT) ; cd hootenanny-rpms && ./BuildArchive.sh"

vagrant-clean:
	vagrant halt
	vagrant destroy -f
	mkdir -p el7
	cd test && vagrant halt && vagrant destroy -f
	rmdir --ignore-fail-on-non-empty el7 || true
	rm -f src/tmp/*-install

vagrant-test:
	# Adding this in so we always have a clean test VM.
	cd test && vagrant halt && vagrant destroy -f
	cd test; vagrant up
	cd test; vagrant ssh -c "cd /var/lib/hootenanny && sudo HootTest --diff --slow"

# This spawns a small VM to update the main repo so we can copy it to S3
vagrant-repo:
	cd update-repo; vagrant up
	cd update-repo; vagrant destroy -f

#el7: el7-src/* custom-rpms
el7: custom-rpms

copy-rpms: el7
	rm -rf el7
	mkdir -p el7
	#cp -l el7-src/* el7/
	cp src/RPMS/noarch/* el7/
	cp src/RPMS/x86_64/* el7/
	createrepo el7

custom-rpms:
	cd src; $(MAKE)

