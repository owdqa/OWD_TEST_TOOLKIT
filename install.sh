#!/bin/bash

OWD_TEST_TOOLKIT_DIR=$PWD

export BRANCH=${1:-"master"}

# Install gaiatest and marionette.
. scripts/install_gaiatest.sh $BRANCH

cd $OWD_TEST_TOOLKIT_DIR
#
# Checkout is already made in script from CI (prepare_and_run.sh),
# but it is necesary to maintain (repeat) here, in case of direct installation into local machine
#
printf "\n\nCompleting install of OWD_TEST_TOOLKIT..." | tee -a $LOGFILE
printf "\n=========================================\n" | tee -a $LOGFILE
printf "\nSwitching to branch $INTEGRATION$BRANCH of OWD_TEST_TOOLKIT ...\n\n" | tee -a $LOGFILE
#git checkout $INTEGRATION$BRANCH 2> >( tee -a $LOGFILE)
printf "\nNow using OWD_TEST_TOOLKIT branch \"$(git branch | grep '*')\".\n\n" | tee -a $LOGFILE

printf "\nInstalling OWD_TEST_TOOLKIT...\n\n" | tee -a $LOGFILE
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

if [ ! -d /tmp/tests ]
then
    mkdir /tmp/tests >/dev/null 2>&1
fi

