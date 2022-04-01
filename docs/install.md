# Installing Hootenanny RPMs

Current version of Hootenanny can be installed from RPMs only on CentOS7. CentOS8 fails due to missing dependencies of liquibase and postgresql.

The following provides instructions for installing Hootenanny from
locally (RPMS built by the user) or from repositories hosted in
S3.

## Local RPMs

To install from RPMs produced locally, you'll first need to install
`yum-utils` and configure the EPEL, PGDG, and Hootenanny dependency
repositories:

```
sudo yum install -y epel-release yum-utils
sudo yum-config-manager --add-repo https://geoint-deps.s3.amazonaws.com/el7/pgdg13.repo
sudo yum-config-manager --add-repo https://geoint-deps.s3.amazonaws.com/el7/stable/geoint-deps.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/deps/stable/hoot-deps.repo
sudo yum makecache -y
```

After building the RPMs with `make rpm`, identify the version number.  This
will be the component of the RPM after the package name but before `.el7`.
For example:

```
# With an RPM of this name:
hootenanny-core-0.2.42-0.2.20180718.4d31c87.el7.x86_64.rpm

# Set HOOT_VERSION as:
HOOT_VERSION=0.2.42-0.2.20180718.4d31c87
```

Once you know the version, install the `core-deps` RPM first, followed by the
`core`, `services-ui`, and finishing with the `autostart` RPM:

```
sudo yum install -y RPMS/noarch/hootenanny-core-deps-$HOOT_VERSION.el7.noarch.rpm
sudo yum install -y RPMS/x86_64/hootenanny-core-$HOOT_VERSION.el7.x86_64.rpm
sudo yum install -y RPMS/x86_64/hootenanny-services-ui-$HOOT_VERSION.el7.x86_64.rpm
sudo yum install -y RPMS/noarch/hootenanny-autostart-$HOOT_VERSION.el7.noarch.rpm
```

## S3

Amazon's [S3](https://aws.amazon.com/s3/) is used to host Hootenanny's
Yum repositories.  The `hoot-repo` bucket has repositories at the following
prefixes:

* `el7/release`: Signed repository of tagged Hootenanny releases.
* `el7/master`: Unsigned master snapshots of Hootenanny built daily.
* `el7/deps/release`: Signed release dependency RPMS.

### Release

Hootenanny releases correspond to tagged revisions.  The RPMs are signed and
may be installed using the following commands:

```
sudo yum install -y epel-release yum-utils
sudo yum-config-manager --add-repo https://geoint-deps.s3.amazonaws.com/el7/pgdg13.repo
sudo yum-config-manager --add-repo https://geoint-deps.s3.amazonaws.com/el7/stable/geoint-deps.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/deps/stable/hoot-deps.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/release/hoot.repo
sudo yum makecache -y
sudo yum install -y hootenanny-autostart
```

### Master

Hootenanny Master releases are built daily from the latest commits pushed to
the [`master`](https://github.com/ngageoint/hootenanny/tree/master) branch.
Master releases are *not* signed, and may be installed with these
commands:

```
sudo yum install -y epel-release yum-utils
sudo yum-config-manager --add-repo https://geoint-deps.s3.amazonaws.com/el7/pgdg13.repo
sudo yum-config-manager --add-repo https://geoint-deps.s3.amazonaws.com/el7/stable/geoint-deps.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/deps/stable/hoot-deps.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/master/hoot.repo
sudo yum makecache -y
sudo yum install -y hootenanny-autostart
```

### OAuth configuration

There is an additional configuration step that needs to be made after the RPM install to set the OAuth redirect URL:

`sudo vi /var/lib/tomcat8/webapps/hoot-services/WEB-INF/classes/conf/hoot-services.conf`

At the bottom of this file, update the line:
>oauthRedirectURL=http://localhost:8080/login.html

to include the proper protocol/host/port of the deployed instance with the `hootenanny-id` URL path.

For example `http://hostname:port/hootenanny-id/login.html`

Save the file and restart tomcat:
`sudo service tomcat8 restart`
