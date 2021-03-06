#!/bin/bash
#
# Handles all dependencies etc... related to installing gaiatest.
#
export BRANCH=${1:-"v2.1"}
LOGFILE=${LOGFILE:-/tmp/gaiatest_setup.log}

printf "\n\nInstalling gaiatest (for $BRANCH) and Marionette ..." | tee -a $LOGFILE
printf "\n====================================================\n" | tee -a $LOGFILE

#
# Now re-install everything.
#
printf "\n* Installing the latest gaiatest from github: " | tee -a $LOGFILE
#git clone https://github.com/mozilla/gaia-ui-tests.git >> $LOGFILE 2>&1

export GAIATEST_PATH=$HOME/gaia/tests/python/gaia-ui-tests/gaiatest

if [ ! -d "$GAIATEST_PATH" ]
then
    printf "(need to clone all of 'gaia' - this will take about 10-15 minutes ...)\n\n" | tee -a $LOGFILE
    cd $HOME
	git clone https://github.com/mozilla-b2g/gaia.git --depth 1 >> $LOGFILE 2>&1
	
    printf "\nSwitching to branch \"$BRANCH\" of gaiatest ...\n\n" | tee -a $LOGFILE
	cd $HOME/gaia
	git checkout $BRANCH  2> >( tee -a $LOGFILE)
else
    printf "(refreshing 'gaia' - this will take just a minute or so ...)\n\n" | tee -a $LOGFILE
    cd $HOME/gaia
    sudo git stash -u && git stash drop
    user=`whoami`
    printf "Resetting gaia ownership to user $user\n"
    sudo chown $user:$user .git -R
    sudo git checkout -f $BRANCH  2> >( tee -a $LOGFILE)
    sudo git pull 2> >( tee -a $LOGFILE)
fi


# Remove previous installation of marionette python packages to prevent errors in python packages resolution
pip freeze|grep marionette|sudo xargs pip uninstall -y

#
# Install gaiatest and dependencies.
#
cd $GAIATEST_PATH/..
printf "\nInstalling gaiatest for branch \"$BRANCH\" ... \n\n" | tee -a $LOGFILE
sudo python setup.py develop > $LOGFILE.tmp 2>&1


#
# Sometimes a bad network connection causes an error in this installation.
# If this happens, wait 1 minute then try again.
#
x=$(grep -i error $LOGFILE.tmp)
if [ "$x" ]
then
	printf "\nERRORS detected while setting up gaiatest dependencies! Trying once more in 1 minute ...\n\n" | tee -a $LOGFILE
	sleep 2
	sudo python setup.py develop > $LOGFILE.tmp

	x=$(grep -i error $LOGFILE.tmp)
    cat $LOGFILE.tmp >>$LOGFILE
    rm $LOGFILE.tmp
	if [ "$x" ]
	then
		#
		# This one failed too - exit with an error code, so the test run knows the situation.
		#
		echo "ERROR: Failed 2nd attempt to install gaiatest properly! See $LOGFILE for details." | tee -a $LOGFILE
		exit 1
	else
		#
		# The 2nd attempt succeeded.
		#
		echo "2nd attempt succeeded!" | tee -a $LOGFILE
	fi
else
    cat $LOGFILE.tmp >> $LOGFILE
    rm $LOGFILE.tmp
fi
