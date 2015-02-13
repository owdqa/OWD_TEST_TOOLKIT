#!/bin/bash

if [ -z "$OWD_TEST_TOOLKIT_DIR" ]
then
    export OWD_TEST_TOOLKIT_DIR=$PWD
fi

export OWD_TEST_TOOLKIT_DIR=$OWD_TEST_TOOLKIT_DIR
export OWD_TEST_TOOLKIT_BIN=$OWD_TEST_TOOLKIT_DIR/scripts
export OWD_TEST_TOOLKIT_CONFIG=$OWD_TEST_TOOLKIT_DIR/config
export GAIATEST_PATH=$HOME/gaia/tests/python/gaia-ui-tests/gaiatest
export PATH=$PATH:/usr/android-sdk/platform-tools/adb:$OWD_TEST_TOOLKIT_DIR/scripts

export BRANCH=${1:"v2.0"}

# Install gaiatest and marionette.
$OWD_TEST_TOOLKIT_BIN/install_gaiatest.sh "$BRANCH"

#
# Checkout is already made in script from CI (prepare_and_run.sh),
# but it is necesary to maintain (repeat) here, in case of direct installation into local machine
#
printf "\n\n<b>Completing install of OWD_TEST_TOOLKIT...</b>" | tee -a $LOGFILE
printf "\n<b>=========================================</b>\n" | tee -a $LOGFILE
printf "\n<b>Switching to branch $INTEGRATION$BRANCH of OWD_TEST_TOOLKIT ...</b>\n\n" | tee -a $LOGFILE
git checkout $INTEGRATION$BRANCH 2> >( tee -a $LOGFILE)
printf "\n<b>Now using OWD_TEST_TOOLKIT branch \"$(git branch | grep '*')\".</b>\n\n" | tee -a $LOGFILE

printf "\n<b>Installing OWD_TEST_TOOLKIT...</b>\n\n" | tee -a $LOGFILE
install_dir=$(dirname $(sudo python setup.py install --dry-run | grep Writing | awk '{print $2}'))
	
if [ "$install_dir" ]
then
    # Deleting as root, so be paranoid about where you are!!
    cd $install_dir
    sudo rm -rf OWDTestToolkit OWD_TEST_TOOLKIT*egg* 2>/dev/null
fi

# If there is a testvars file under $HOME, overwrite the one in the repository
if [ -f $HOME/gaiatest_testvars.json ]
then
    cp $HOME/gaiatest_testvars.json $OWD_TEST_TOOLKIT_DIR/config/gaiatest_testvars.json
fi

cd $OWD_TEST_TOOLKIT_DIR
if [ -z "$LOGFILE" ]
then
    export LOGFILE=${LOGFILE:-"/tmp/owd_setup_$(date +%Y%m%d%H%M).log"}
fi
sudo python setup.py clean --all >> $LOGFILE 2>&1
sudo python setup.py install >> $LOGFILE 2>&1

[ ! -d "/tmp/tests" ] && mkdir /tmp/tests >/dev/null 2>&1
