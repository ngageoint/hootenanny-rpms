# Maven Cache

The Maven cache file was created with the following tar command:

```
tar \
  --owner 1000 \
  --group 1000 \
  --numeric-owner \
  --exclude repository/hoot \
  -C ~/hootenanny-rpms/cache/m2 \
  -czvf ~/m2-cache.tar.gz repository
```

Then uploaded as part of a `maven` directory to the `hoot-repo` S3 bucket:

```
mkdir maven
mv m2-cache.tar.gz maven
aws s3 sync maven/ s3://hoot-repo/maven/ --acl public-read
```
