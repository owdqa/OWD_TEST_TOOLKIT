#!/bin/bash

export MYPATH=$(dirname $0)
export CURRPATH=$(pwd)

export BRANCH=${1:-"v1-train"}

printf "\n\nInstalling gaiatest (for $BRANCH) and Marionette ..." | tee -a $LOGFILE
printf "\n====================================================\n" | tee -a $LOGFILE

#
# Remove any previous marionette
# (using 'sudo', so be paranoid about "rm -rf"!!!).
#

# Use PYTHONPATH to get the location of Marionette etc...
x=$(python <<!
import sys
print sys.path
exit()
!
)
IFS=', ' read -a array <<< "$x"
for element in "${array[@]}"
do
    el=$(echo $element | sed -e "s/'//g")
    ck=$(basename $el | egrep "^marionette")
    if [ "$ck" ]
    then
    	install_dir=$(dirname $el)
    	if [ "$install_dir" ]
    	then
			sudo rm -rf $install_dir/moz*  2> /dev/null
			sudo rm -rf $install_dir/marionette*  2> /dev/null
			sudo rm -rf $install_dir/ManifestDestiny*  2> /dev/null
			sudo rm -rf $install_dir/gaiatest* 2> /dev/null
			sudo rm gaiatest* 2>/dev/null
    	fi
    fi
done

# Remove the exec files too.
x=$(which marionette 2>/dev/null)
[ "$x" ] && sudo rm $x
x=$(which gaiatest 2>/dev/null)
[ "$x" ] && sudo rm $x

# ...and the current dir (if it's there)
sudo rm -rf gaia-ui-tests 2>/dev/null
	
#
# Now re-install everything.
#
printf "\n\n- Cloning gaiatest - this make take a few minutes, please wait ...\n\n" | tee -a $LOGFILE
git clone https://github.com/mozilla/gaia-ui-tests.git >> $LOGFILE 2>>$LOGFILE

# Install gaiatest.
cd gaia-ui-tests
printf "\n\n- Switching to branch \"$BRANCH\" of gaiatest ...\n\n" | tee -a $LOGFILE
git checkout $BRANCH  2> >( tee $LOGFILE)
printf "\n\n- Installing gaiatest for branch \"$(git branch | grep '*')\" ...\n\n" | tee -a $LOGFILE
sudo python setup.py develop | tee /tmp/gaiatest_setup.log >> $LOGFILE

#
# Sometimes a bad network connection causes an error in this installation.
# If this happens, try again.
#
x=$(grep -i error /tmp/gaiatest_setup.log)
if [ "$x" ]
then
	printf "\n\nERRORS detected while setting up gaiatest dependencies! Trying again ...\n\n" | tee -a $LOGFILE
	sudo python setup.py develop >> $LOGFILE
fi