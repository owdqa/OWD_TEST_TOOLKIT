#!/bin/bash
#
# Prepare the dependencies for running Selenium tests on the CI server.
#
export BRANCH=${2:-"selenium/tests"}
export TEST_TYPE=${3:-"REGRESSION"}

OWD_TEST_TOOLKIT_DIR=`dirname $PWD`

. set_up_parameters.sh

python install_cert_tests.py

cd $OWD_TEST_TOOLKIT_DIR/../owd-obcertification

sudo python tests/launcher.py

