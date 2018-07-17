# Installing Hootenanny RPMs

## Local RPMs

## S3

### Release

Hootenanny releases are signed and  may be installed using the following
commands:

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
Development releases are *not* signed, 

```
sudo yum install -y epel-release yum-utils
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/pgdg95.repo
sudo yum-config-manager --add-repo https://s3.amazonaws.com/hoot-repo/el7/develop/hoot.repo
sudo yum makecache -y
sudo yum install -y hootenanny-autostart
```
