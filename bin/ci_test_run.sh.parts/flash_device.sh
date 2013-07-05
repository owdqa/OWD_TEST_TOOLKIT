#
# Flash device.
#
flash_device.sh $DEVICE eng $BRANCH NODOWNLOAD >/tmp/flash_device 2>&1

buildname=$(egrep "^Unpacking " /tmp/flash_device | awk '{print $2}' | sed -e "s/^\(.*\).tgz$/\1/")
cp /tmp/flash_device ${INSTALL_LOG}@Build_name@${buildname}

# (for the CI output)
printf "\n\nTests running against build: $buildname\n"
