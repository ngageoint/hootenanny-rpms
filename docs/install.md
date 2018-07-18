# Installing Hootenanny RPMs

The following provides instructions for installing Hootenanny from
locally (RPMS built by the user) or from repositories hosted in
S3.

## Local RPMs

To install from RPMs produced locally, you'll first need to install
`yum-utils` and configure the EPEL, PGDG, and Hootenanny dependency
repositories:

```
sudo yum install -y epel-release yum-utils
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/pgdg95.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/deps/hoot-deps.repo
sudo yum makecache -y
```

After building the RPMs with `make rpm`, identify the version number.

Install the `core-deps` first, followed by the `core`, `services-ui`, and
finishing with the `autostart` RPM.

```
sudo yum install -y `RPMS/noarch/hootenanny-core-deps-$HOOT_VERSION.el7.noarch.rpm`
sudo yum install -y `RPMS/x86_64/hootenanny-core-$HOOT_VERSION.el7.x86_64.rpm`
sudo yum install -y `RPMS/x86_64/hootenanny-services-ui-$HOOT_VERSION.el7.x86_64.rpm`
sudo yum install -y `RPMS/noarch/hootenanny-autostart-$HOOT_VERSION.el7.noarch.rpm`
```

## S3

Amazon's [S3](https://aws.amazon.com/s3/) is used to host Hootenanny's
Yum repositories.  The bucket is `hoot-repo`,

* `el7/release`: Signed repository of tagged Hootenanny releases.
* `el7/develop`: Unsigned development snapshot RPMs of Hootenanny,
  built daily.
* `el7/deps/release`: Signed release dependencies from RPMs generated here.

### Release

Hootenanny releases correspond to tagged revisions.  The RPMs are signed and
may be installed using the following commands:

```
sudo yum install -y epel-release yum-utils
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/pgdg95.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/release/hoot.repo
sudo yum makecache -y
sudo yum install -y hootenanny-autostart
```

### Development

Hootenanny development releases are built daily from the latest commits pushed to
the [`develop`](https://github.com/ngageoint/hootenanny/tree/develop) branch.
Development releases are *not* signed, and may be installed with these
commands:

```
sudo yum install -y epel-release yum-utils
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/pgdg95.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/develop/hoot.repo
sudo yum makecache -y
sudo yum install -y hootenanny-autostart
```
