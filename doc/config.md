# Configuration Reference

The repository's primary configuration comes from `config.yaml`.  In addition, environment variables may be used to modify some behavior.

## `config.yml`

This YAML file holds the all the relevant settings for this repository in dictionaries:

* `versions`: Versions of the dependency RPMs
* `images`: Build arguments, tags, and other settings for container images
* `maven`: Maven cache URL and SHA1 checksum

Because this file is also used by [shell](../shell), any relevant variable should have an anchor property (`&`).  This allows a shell script to easily search for a value without using a YAML library.  For example:

```yaml
versions:
  geos: &geos_version: '3.6.2-1'
```

In addition, using anchors allows reuse of the variable without repeating it, for example:

```yaml
images:
  - rpmbuild-gdal:
      args:
        geos_version: *geos_version
```

## Environment Variables

### `MAVEN_CACHE`

Hootenanny uses Maven for building its Java services code, which requires retrieving assets over HTTP.  To prevent frequent timeouts and race conditions a pre-existing cache is downloaded prior to trying to run the `rpmbuild-hoot-release` or `rpmbuild-hoot-devel` containers.   Setting the `MAVEN_CACHE` environment variable to any value other than `1` disables retrieving this cache file.  Example:

```
MAVEN_CACHE=0 vagrant status
```

### `RPMBUILD_UID_MATCH`

By default, the containers use a UID of 1000 for the non-privileged `rpmbuild` user.  While this is the first-user ID on most Linux distributions, this is not universally true -- and will result in permission errors because the host's UID doesn't match that of the container because [Docker bind mounts](https://docs.docker.com/storage/bind-mounts/) are used .  Thus, if you want the `rpmbuild` container user to match that of the host user invoking `docker`, set the `RPMBUILD_UID_MATCH` environment variable to any value.
