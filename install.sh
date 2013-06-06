#!/bin/bash

# Create file containing the required vars...
export OWD_TEST_TOOLKIT_DIR=$(pwd)
cat >  $HOME/.OWD_TEST_TOOLKIT_LOCATION << EOF
export OWD_TEST_TOOLKIT_DIR=$OWD_TEST_TOOLKIT_DIR
export PATH=$PATH:$OWD_TEST_TOOLKIT_DIR/bin
EOF

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
[ ! -d ./gaia-ui-tests ] && ./bin/setup_gaiatest.sh "$BRANCH"

#
# Install me.
#
printf "\n\nCompleting install of OWD_TEST_TOOLKIT..." | tee -a $LOGFILE
printf "\n=========================================\n" | tee -a $LOGFILE
printf "\n* Switching to branch $BRANCH of OWD_TEST_TOOLKIT ...\n\n" | tee -a $LOGFILE
git checkout $BRANCH 2> >( tee -a $LOGFILE)
printf "\n* Now using OWD_TEST_TOOLKIT branch \"$(git branch | grep '*')\".\n\n" | tee -a $LOGFILE

printf "\n* Installing OWD_TEST_TOOLKIT...\n\n" | tee -a $LOGFILE
x=$(dirname $(sudo python setup.py install --dry-run | grep Writing | awk '{print $2}'))
if [ "$x" ]
then
    # Deleting as root, so be paranoid about where you are!!
    cd /tmp
    cd $x
    sudo rm -rf OWDTestToolkit OWD_TEST_TOOLKIT*egg*
fi
cd $HOME/projects/OWD_TEST_TOOLKIT
sudo python setup.py install >> $LOGFILE


#
# Install the owd test cases.
#
printf "\n\nInstalling owd_test_cases..." | tee -a $LOGFILE
printf "\n============================\n" | tee -a $LOGFILE
cd $HOME/projects
rm -rf owd_test_cases 2>/dev/null

git clone https://github.com/roydude/owd_test_cases.git >> $LOGFILE 2>> $LOGFILE
cd $HOME/projects/owd_test_cases

printf "\n* Switching to branch $BRANCH of owd_test_cases ...\n\n" | tee -a $LOGFILE
git checkout $BRANCH  2> >( tee -a $LOGFILE)
printf "\n* Now using owd_test_cases branch \"$(git branch | grep '*')\".\n\n"
