#!/usr/bin/dumb-init /bin/bash
set -euo pipefail

# Create logfiles.
touch /var/log/{node-export,node-mapnik,tomcat8}.log
chown tomcat:tomcat /var/log/{node-export,node-mapnik,tomcat8}.log

# PostgreSQL
su-exec postgres pg_ctl -D $PGDATA -s start &> /dev/null

# Tomcat
su-exec tomcat /usr/libexec/tomcat8/server start &> /var/log/tomcat8.log &

su-exec tomcat bash -c "cd /var/lib/hootenanny/node-export-server && npm start" &> /var/log/node-export.log &
su-exec tomcat bash -c "cd /var/lib/hootenanny/node-mapnik-server && source ../bin/HootEnv.sh && source ../conf/database/DatabaseConfig.sh && npm start" &> /var/log/node-mapnik.log &

# Start command as the Tomcat user.
exec su-exec tomcat $@
