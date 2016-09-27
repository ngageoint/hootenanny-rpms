#!/bin/bash

if ! sudo grep -i --quiet HOOT /var/lib/pgsql/9.2/data/postgresql.conf; then
    echo "Tuning PostgreSQL"
    sudo -u postgres sed -i.bak s/^max_connections/\#max_connections/ /var/lib/pgsql/9.2/data/postgresql.conf
    sudo -u postgres sed -i.bak s/^shared_buffers/\#shared_buffers/ /var/lib/pgsql/9.2/data/postgresql.conf
    sudo -u postgres bash -c "cat >> /var/lib/pgsql/9.2/data/postgresql.conf" <<EOT
#--------------
# Hoot Settings
#--------------
max_connections = 1000
shared_buffers = 1024MB
max_files_per_process = 1000
work_mem = 16MB
maintenance_work_mem = 256MB
checkpoint_segments = 20
autovacuum = off
EOT

sudo /etc/init.d/postgresql-9.2 restart
fi

