#!/bin/bash

# Create file containing the required vars...
export OWD_TEST_TOOLKIT_DIR=$(pwd)
cat >  $HOME/.OWD_TEST_TOOLKIT_LOCATION << EOF
export OWD_TEST_TOOLKIT_DIR=$OWD_TEST_TOOLKIT_DIR
export OWD_TEST_TOOLKIT_BIN=$OWD_TEST_TOOLKIT_DIR/bin
export PATH=$PATH:$OWD_TEST_TOOLKIT_DIR/bin
EOF

. $HOME/.OWD_TEST_TOOLKIT_LOCATION

# Log file for 'everything'.
export LOGFILE=${1:-"/tmp/owd_setup_$(date +%H%M%Y%m%d).log"}

# Branch for gaiatest etc...1
export BRANCH=${2:-"v1-train"}
[ "$BRANCH" = "1.0.1" ] && export BRANCH="v1.0.1"

#
# CHECK DEPENDENCIES ...
#

# Python 2.7
x=$(which python2.7 2>/dev/null)
if [ ! "$x" ]
then
    echo "Python 2.7 not found - please install and try again!"
    exit 1
fi

# ADB
x=$(which adb 2>/dev/null)
if [ ! "$x" ]
then
    echo "ADB not found - please install and try again!"
    exit 1
fi

# python-setuptools
x=$(which easy_install 2>/dev/null)
if [ ! "$x" ]
then
    echo "'easy_install' (python-setuptools) not found - please install and try again!"
    exit 1
fi



#
# Install gaiatest and marionette.
#
[ ! -d ./gaia-ui-tests ] && $OWD_TEST_TOOLKIT_BIN/setup_gaiatest.sh "$BRANCH"



#
# Install me.
#
printf "\n\nCompleting install of OWD_TEST_TOOLKIT..." | tee -a $LOGFILE
printf "\n=========================================\n" | tee -a $LOGFILE
printf "\n* Switching to branch $BRANCH of OWD_TEST_TOOLKIT ...\n\n" | tee -a $LOGFILE
git checkout $BRANCH 2> >( tee -a $LOGFILE)
printf "\n* Now using OWD_TEST_TOOLKIT branch \"$(git branch | grep '*')\".\n\n" | tee -a $LOGFILE

printf "\n* Installing OWD_TEST_TOOLKIT...\n\n" | tee -a $LOGFILE
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
    sudo rm -rf OWDTestToolkit OWD_TEST_TOOLKIT*egg*
fi

cd $OWD_TEST_TOOLKIT_DIR
sudo python setup.py clean --all >> $LOGFILE 2>/dev/null
sudo python setup.py install >> $LOGFILE



#
# If you're developing the toolkit, this might be the last thing you want,
# so I've defaulted it to not do this! ...
#
if [ "$REINSTALL_OWD_TEST_CASES" ]
then
    #
    # Install the owd test cases.
    #
    printf "\n\nInstalling owd_test_cases..." | tee -a $LOGFILE
    printf "\n============================\n" | tee -a $LOGFILE
    cd $OWD_TEST_TOOLKIT_BIN/..
    rm -rf owd_test_cases 2>/dev/null

    git clone https://github.com/roydude/owd_test_cases.git >> $LOGFILE 2>> $LOGFILE
    cd owd_test_cases

    printf "\n* Switching to branch $BRANCH of owd_test_cases ...\n\n" | tee -a $LOGFILE
    git checkout $BRANCH  2> >( tee -a $LOGFILE)
    printf "\n* Now using owd_test_cases branch \"$(git branch | grep '*')\".\n\n"
else
    printf "\n\n*** NOTE: Not refreshing owd_test_cases! *** \n\n"
fi
