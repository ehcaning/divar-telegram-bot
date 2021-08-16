#!/bin/sh

env >> /etc/environment

# start cron in the foreground (replacing the current process)
exec "$@"