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

The resulting tar file is then uploaded to the `hoot-maven` S3 bucket,
created with the following command:

```
aws s3api create-bucket --bucket hoot-maven --acl public-read
```

Finally, copy the cache file to the bucket:

```
aws s3 cp m2-cache.tar.gz s3://hoot-maven/ --acl public-read
```

Please record the URL of the cache file and the SHA1 checksum in `config.yml`:

```yaml
maven:
  cache_url: &maven_cache_url 'https://s3.amazonaws.com/hoot-maven/m2-cache.tar.gz'
  cache_sha1: &maven_cache_sha1 'efbd6edd5a13bf3806780f144b4fe314c34eccfc'
```
