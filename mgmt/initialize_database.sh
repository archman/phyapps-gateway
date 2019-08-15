#!/bin/sh

#
# Initialize database for phyapps-gateway service.
# Only do once after phyapps-gateway is up for the first time.
#

flask db init && \
    flask db migrate -m "Initialize database" && \
    flask db upgrade && \
    config_admin_account.py

