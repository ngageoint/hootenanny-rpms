#!/usr/bin/dumb-init /bin/bash
set -euo pipefail

# Start PostgreSQL, suppressing output.
su-exec postgres pg_ctl -D $PGDATA -s start &> /dev/null

# Start desired command as the unprivileged build user.
exec su-exec $RPMBUILD_USER "$@"
