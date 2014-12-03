#!/bin/bash
#
# Prepare the dependencies for running OWD tests on the CI server.
#
# It is assumed that the OWD_TEST_TOOLKIT has already been cloned
# (or this script would not exist to run!).
#
export DEVICE=${1:-"flame"}
export BRANCH=${2:-"v2.0"}
export TEST_TYPE=${3:-"REGRESSION"}

. $0.parts/set_up_parameters.sh

. $0.parts/install_toolkit_and_test_cases.sh

. $OWD_TEST_TOOLKIT_BIN/ci_test_run.sh.parts/flash_device.sh

cd $OWD_TEST_TOOLKIT_DIR/../owd_test_cases

sudo DEVICE=$DEVICE BRANCH=$BRANCH DEVICE_BUILDNAME=$DEVICE_BUILDNAME ON_CI_SERVER=$ON_CI_SERVER python $OWD_TEST_TOOLKIT_DIR/scripts/ffox_test_runner.py --testvars=$OWD_TEST_TOOLKIT_DIR/config/gaiatest_testvars.json --address=localhost:2828 tests/$TEST_TYPE

