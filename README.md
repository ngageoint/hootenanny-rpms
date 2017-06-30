
This repository contains both 3rd-party RPMs that are required by Hootenanny as
well as source RPMs that are custom built for Hootenanny.

The easiest and quickest way to install and run Hootenanny is by installing from RPMs in CentOS 6.7.  A public facing repository exists that includes the latest stable release as well as many previous versions.  To install from RPMs, perform the following steps:

* Create the following file: ```/etc/yum.repos.d/hoot.repo```
* Add the following content to that file:
```
[hoot]
name=hoot
baseurl=https://s3.amazonaws.com/hoot-rpms/stable/el6/
gpgcheck=0
```
* Run ```sudo yum install hootenanny-autostart```

Once installed, the UI can be accessed via a browser at ```http://localhost:8080/hootenanny-id/```.  NOTE: If accessing from a remote computer, use the hostname in place of 'localhost'.

It is also possible to build RPMs from source code by performing the following steps:
```
# As of 2016-02-12 the develop branch works for building RPMs.
# a different compatible branch/tag/revision can be specified.
export GIT_COMMIT=develop

# Install local deps for running vagrant
sudo apt-get install nfs-kernel-server vagrant
git clone https://github.com/ngageoint/hootenanny-rpms.git
cd hootenanny-rpms

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

