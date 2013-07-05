#
# The directory that the physical files will be located for the web page.
#
HTML_FILEDIR=/var/www/html/owd_tests/$RUN_ID
if [ ! -d "$HTML_FILEDIR" ]
then
    sudo mkdir -p $HTML_FILEDIR
    sudo chmod 777 $HTML_FILEDIR
fi

# 'sudo rm' so be paranoid!
if [ "$HTML_FILEDIR" ]
then
    cd $HTML_FILEDIR
    sudo rm -f * 2>/dev/null
    cd - >/dev/null
fi


#
# The url for this results web page.
#
HTML_WEBDIR="http://owd-qa-server/owd_tests/$RUN_ID"


#
# Get the Jira test cases baseurl form here so we ca nlink to 
# them from our page ....
#
. $OWD_TEST_TOOLKIT_CONFIG/jira_user_stories.sh

[ "$OWD_NO_BLOCKED" ] && blocked="No" || blocked="Yes"
[ "$OWD_USE_2ND_CHANCE" ] && chance2="Yes" || chance2="No"
