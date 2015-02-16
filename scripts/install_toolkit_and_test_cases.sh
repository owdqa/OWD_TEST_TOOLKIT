#
# Install the toolkit and dependencies (assume we've just cloned it and 
# are still in the parent directory).
#
cd $OWD_TEST_TOOLKIT_DIR

# Log file for 'everything'.

if [ -z "$LOGFILE" ]
then
    export LOGFILE=${LOGFILE:-"/tmp/owd_setup_$(date +%Y%m%d%H%M).log"}
fi

. $OWD_TEST_TOOLKIT_DIR/install.sh $BRANCH >> $LOGFILE 2>&1

#
# Re-install the test cases too.
#
printf "\n\n<b>Installing owd_test_cases...</b>" >> $LOGFILE
printf "\n<b>============================</b>\n" >> $LOGFILE
cd $OWD_TEST_TOOLKIT_DIR/..
rm -rf owd_test_cases 2>/dev/null

git clone https://github.com/owdqa/owd_test_cases.git >> $LOGFILE 2>&1
cd owd_test_cases

printf "\n<b>Switching to branch $INTEGRATION$BRANCH of owd_test_cases ...</b>\n\n" >> $LOGFILE
git checkout $INTEGRATION$BRANCH  >> $LOGFILE 2>&1
printf "\nNow using OWD_TEST_TOOLKIT branch \"$INTEGRATION$BRANCH\".\n\n" >> $LOGFILE

cd $OWD_TEST_TOOLKIT_DIR/..

