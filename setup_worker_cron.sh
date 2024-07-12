#!/bin/bash

# Define the command to run your Django worker
WORKER_CMD="cd /var/app/current && source /var/app/venv/*/bin/activate && python3 manage.py worker"

# Create a new cron job file
echo "* * * * * $WORKER_CMD >> /var/log/worker.log 2>&1" > /etc/cron.d/worker-cron

# Ensure the cron job file has the correct permissions
chmod 0644 /etc/cron.d/worker-cron

# Apply the cron job
crontab /etc/cron.d/worker-cron

# Restart the cron service to apply changes
service crond restart