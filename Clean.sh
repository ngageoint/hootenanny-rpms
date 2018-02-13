#!/bin/sh

docker images -q hoot/rpmbuild* | xargs docker image rm -f
docker images -q hoot/run* | xargs docker image rm -f
