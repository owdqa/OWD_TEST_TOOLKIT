#!/bin/bash

# Create file containing the required vars...
export OWD_TEST_TOOLKIT_DIR=$(pwd)
cat >  $HOME/.OWD_TEST_TOOLKIT_LOCATION << EOF
export OWD_TEST_TOOLKIT_DIR=$OWD_TEST_TOOLKIT_DIR
export OWD_TEST_TOOLKIT_BIN=$OWD_TEST_TOOLKIT_DIR/bin
export OWD_TEST_TOOLKIT_CONFIG=$OWD_TEST_TOOLKIT_DIR/config
export GAIATEST_PATH=$HOME/gaia/tests/python/gaia-ui-tests/gaiatest
export PATH=$PATH:/usr/android-sdk/platform-tools/adb:$OWD_TEST_TOOLKIT_DIR/bin
EOF


. $HOME/.OWD_TEST_TOOLKIT_LOCATION

# Log file for 'everything'.
export LOGFILE=${LOGFILE:-"/tmp/owd_setup_$(date +%H%M%Y%m%d).log"}

export BRANCH=${1:"sms-blocked-tests"}
[ "$BRANCH" = "1.0.1" ] && export BRANCH="v1.0.1"


#
# CHECK DEPENDENCIES ...
#
# Python 2.7
x=$(which python2.7 2>/dev/null)
if [ ! "$x" ]
then
    echo "<b>Python 2.7 not found - please install and try again!</b>" | tee -a $LOGFILE
    exit 1
fi

# ADB
x=$(which adb 2>/dev/null)
if [ ! "$x" ]
then
    echo "<b>ADB not found - please install and try again!</b>" | tee -a $LOGFILE
    exit 1
fi

# python-setuptools
x=$(which easy_install 2>/dev/null)
if [ ! "$x" ]
then
    echo "<b>'easy_install' (python-setuptools) not found - please install and try again!</b>" | tee -a $LOGFILE
    exit 1
fi



#
# Install gaiatest and marionette.
#
$OWD_TEST_TOOLKIT_BIN/install_gaiatest.sh "$BRANCH"



#
# Install me.
#
printf "\n\n<b>Completing install of OWD_TEST_TOOLKIT...</b>" | tee -a $LOGFILE
printf "\n<b>=========================================</b>\n" | tee -a $LOGFILE
printf "\n<b>Switching to branch $INTEGRATION$BRANCH of OWD_TEST_TOOLKIT ...</b>\n\n" | tee -a $LOGFILE
git checkout $INTEGRATION$BRANCH 2> >( tee -a $LOGFILE)
printf "\n<b>Now using OWD_TEST_TOOLKIT branch \"$(git branch | grep '*')\".</b>\n\n" | tee -a $LOGFILE

printf "\n<b>Installing OWD_TEST_TOOLKIT...</b>\n\n" | tee -a $LOGFILE
install_dir=$(dirname $(sudo python setup.py install --dry-run | grep Writing | awk '{print $2}'))
	
if [ ! "$install_dir" ]
then
	# Couldn't find it for some reason - try getting the marionette folder.
	install_dir=$($MYPATH/get_python_dist_path marionette)
fi

if [ "$install_dir" ]
then
    # Deleting as root, so be paranoid about where you are!!
    cd /tmp
    cd $install_dir
    sudo rm -rf OWDTestToolkit OWD_TEST_TOOLKIT*egg* 2>/dev/null
fi

cd $OWD_TEST_TOOLKIT_DIR
sudo python setup.py clean --all >> $LOGFILE 2>&1
sudo python setup.py install >> $LOGFILE 2>&1

[ ! -d "/tmp/tests" ] && mkdir /tmp/tests >/dev/null 2>&1

# HOTFIX - Avoid gaia_apps.js file to replace with the one from gaia.
#export GAIA_APPS_FILE_PATH=$OWD_TEST_TOOLKIT_CONFIG/gaia_apps.js
#if [ -f $GAIA_APPS_FILE_PATH ]
#then
#    sudo cp $GAIA_APPS_FILE_PATH $GAIATEST_PATH/atoms/
#fi

#export GAIA_TEST_FILE_PATH=$OWD_TEST_TOOLKIT_CONFIG/gaia_test.py
#if [ -f $GAIA_TEST_FILE_PATH ]
#then
#    sudo cp $GAIA_TEST_FILE_PATH $GAIATEST_PATH
#fi

