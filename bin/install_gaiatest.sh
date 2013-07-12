#!/bin/bash
#
# Handles all dependencies etc... related to installing gaiatest.
#

. $HOME/.OWD_TEST_TOOLKIT_LOCATION

export MYPATH=$(dirname $0)
export CURRPATH=$(pwd)

export BRANCH=${1:-"v1-train"}
LOGFILE=${LOGFILE:-/tmp/gaiatest_setup.log}

printf "\n\nInstalling gaiatest (for $BRANCH) and Marionette ..." | tee -a $LOGFILE
printf "\n====================================================\n" | tee -a $LOGFILE



# Leaving this here for a little while in case we need it again, but after some
# testing it seems that gaiatest handles this (and it perhaps means that if there's
# a problem, then the tests will still run).
#
# Remove everything relating to gaiatest ...
#
# (NOTE: using 'sudo', so be paranoid about "rm -rf"!!!).
#
#install_dir=$($OWD_TEST_TOOLKIT_BIN/get_python_dist_path.sh marionette)
#if [ "$install_dir" ]
#then
#	sudo rm -rf $install_dir/moz*  2> /dev/null
#	sudo rm -rf $install_dir/marionette*  2> /dev/null
#	sudo rm -rf $install_dir/ManifestDestiny*  2> /dev/null
#	sudo rm -rf $install_dir/gaiatest* 2> /dev/null
#	sudo rm gaiatest* 2>/dev/null
#fi
#
#x=$(which marionette 2>/dev/null)
#[ "$x" ] && sudo rm $x
#x=$(which gaiatest 2>/dev/null)
#[ "$x" ] && sudo rm $x
#
#sudo rm -rf gaia-ui-tests 2>/dev/null




#
# Now re-install everything.
#
printf "\n* Cloning gaiatest from github - this make take a few minutes, please wait ...\n\n" | tee -a $LOGFILE
git clone https://github.com/mozilla/gaia-ui-tests.git >> $LOGFILE 2>&1


#
# Install gaiatest.
#
cd gaia-ui-tests

#
# Switch to correct branch.
#
printf "\n* Switching to branch \"$BRANCH\" of gaiatest ...\n\n" | tee -a $LOGFILE
git checkout $BRANCH  2> >( tee -a $LOGFILE)

#
# Install gaiatest and dependencies.
#
printf "\n* Installing gaiatest for branch \"$(git branch | grep '*')\" ...\n\n" | tee -a $LOGFILE
sudo python setup.py develop >> $LOGFILE 2>&1


#
# Sometimes a bad network connection causes an error in this installation.
# If this happens, wait 1 minute then try again.
#
x=$(grep -i error $LOGFILE)
if [ "$x" ]
then
	printf "\n* ERRORS detected while setting up gaiatest dependencies! Trying once more in 1 minute ...\n\n" | tee -a $LOGFILE
	sleep 60
	sudo python setup.py develop >> $LOGFILE.tmp

	x=$(grep -i error $LOGFILE.tmp)
    cat $LOGFILE.tmp >>$LOGFILE
    rm $LOGFILE.tmp
	if [ "$x" ]
	then
		#
		# This one failed too - exit with an error code, so the test run knows the situation.
		#
		echo "ERROR: Failed 2nd attempt to install gaiatest properly! See $LOGFILE for details."
		exit 1
	else
		#
		# The 2nd attempt succeeded.
		#
		echo "2nd attempt succeeded!"
	fi
fi