#!/bin/sh

#
# Initialize database for phyapps-gateway service.
# Only do once after phyapps-gateway is up for the first time.
#

d=$(dirname $FLASK_APP)/migrations
[ -e $d ] && /bin/rm -rf $d

flask db init && \
    flask db migrate -m "Initialize database" && \
    flask db upgrade

# set up admin account:
# config_admin_account.py

