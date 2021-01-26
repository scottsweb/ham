#!/bin/bash

# make sure we are running the latest version of jotta-cli
apt-get update
apt-get install jotta-cli

# set the jottad user and group id
usermod -u $PUID jottad
usermod --gid $PGID jottad
usermod -a -G jottad jottad

# start the service
/etc/init.d/jottad start

# wait for service to fully start
sleep 5

if [[ "$(jotta-cli status)" =~ ERROR.* ]]; then

  echo "First time login"

  # Login user
  /usr/bin/expect -c "
  set timeout 20
  spawn jotta-cli login
  expect \"accept license (yes/no): \" {send \"yes\n\"}
  expect \"Personal login token: \" {send \"$JOTTA_TOKEN\n\"}
  expect \"Devicename*: \" {send \"$JOTTA_DEVICE\n\"}
  expect eof
  "

else

echo "User is logged in"

fi

# set scan interval
echo "Setting scan interval"
jotta-cli config set scaninterval $JOTTA_SCANINTERVAL

# add folders in /backup
for folder in /backup/*; do
#  jotta-cli add "$folder"
  echo "$folder"
done

# put tail in the foreground, so docker does not quit
tail -f /dev/null

exec "$@"
