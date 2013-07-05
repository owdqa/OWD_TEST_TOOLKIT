#
# Install the toolkit and dependencies.
#
cd $OWD_TEST_TOOLKIT_DIR

./install.sh > $RESULT_DIR/OWD_TEST_TOOLKIT_install.log


. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Re-install the test cases too.
#
printf "\n\nInstalling owd_test_cases..." >> $LOGFILE
printf "\n============================\n" >> $LOGFILE
cd $OWD_TEST_TOOLKIT_DIR/..
rm -rf owd_test_cases 2>/dev/null

#git clone https://github.com/owdqa/owd_test_cases.git 2> >( tee -a $LOGFILE)
git clone https://github.com/owdqa/owd_test_cases.git >> $LOGFILE 2>&1
cd $owd_test_cases_DIR

printf "\n* Switching to branch $BRANCH of owd_test_cases ...\n\n" >> $LOGFILE
git checkout $BRANCH  >> $LOGFILE 2>&1
