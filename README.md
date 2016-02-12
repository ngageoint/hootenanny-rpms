
This repository contains both 3rd-party RPMs that are required by Hootenanny as
well as source RPMs that are custom built for Hootenanny.

At some point in the future we'll host a RPM repo where you can simply install
hoot, but until then you can use the following to create your own RPM repo.

```
# As of 2016-02-12 this is the only branch that works, in the future you can specify
# a different compatible branch/tag/revision
export GIT_COMMIT=r6921

# Install local deps for running vagrant
sudo apt-get install nfs-kernel-server vagrant
git clone https://github.com/ngageoint/hootenanny-rpms.git
cd hootenanny-rpms
git checkout r6921

# Clean out any old vagrant machine that is laying around from a previous
# attempt. You should run this before building if you try a build and it
# fails.
make vagrant-clean
# Build the Hoot RPMs and all supporting RPMs
make vagrant-build
# Test the new Hoot RPMs
make vagrant-test
```

* You'll have a new set of RPMS built in `hootenanny-rpms/el6`
* The RPMs can be served out using your favorite web server and accessed via
  yum.
* After yum is configured properly, to install hootenanny:
```
sudo yum install hootenanny-core
```

