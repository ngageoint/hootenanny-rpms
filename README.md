
This repository contains both 3rd-party RPMs that are required by Hootenanny as
well as source RPMs that are custom built for Hootenanny.

At some point in the future we'll host a RPM repo where you can simply install
hoot, but until then you can use the following to create your own RPM repo.

* Install a basic CentOS 6.7 instance (other versions may work, but have not been
  tested).
* Clone this repo into your home directory (we'll assume `$HOME/hootenanny-rpms`)
* Run:
```
make deps
make
```

* You'll have a new set of RPMS build int `$HOME/hootenanny-rpms/el6`
* Add a new repo in `/etc/yum.repos.d/`
```
[hoot]
name=hoot
baseurl=file:///<YOUR HOME DIR HERE>/hootenanny-rpms/el6/
enabled=1
gpgcheck=0
```

* Then to install hootenanny:
```
sudo yum install hootenanny-core
```

