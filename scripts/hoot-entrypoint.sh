#!/bin/bash
set -e

# Start PostgreSQL, suppressing output.
su-exec postgres pg_ctl -D $PGDATA start &> /dev/null

# Start shell as the build user.
exec su-exec $RPMBUILD_USER:$RPMBUILD_USER "$@"
