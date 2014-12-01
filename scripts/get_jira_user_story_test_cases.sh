#!/bin/bash
#
# A standalone executable to return a list of test cases for a Jira User Story.
#
USER_STORY=${1:?"Syntax: $0 <user story id>"}

#
# First check you have the jira login file.
#
if [ ! -f $HOME/.jira_login ]
then
    echo "$HOME/.jira_login not found, please enter these details (only required once):"
    printf "JIRA 'baseurl' (up to the final number part): "
    read BASEURL
    printf "JIRA username: "
    read username
    printf "JIRA password: "
    stty -echo
    read password
    stty echo
    printf "BASEURL $BASEURL\nUSERNAME $username\nPASSWORD $password\n" > $HOME/.jira_login
    chmod go-rwx ~/.jira_login
fi

U=$(egrep "^U" $HOME/.jira_login | awk '{print $2}')
P=$(egrep "^P" $HOME/.jira_login | awk '{print $2}')
B=$(egrep "^B" $HOME/.jira_login | awk '{print $2}')

CACHE_BASE=$HOME/tmp/_jira_test_cases
[ ! -d "$HOME/tmp" ] && mkdir $HOME/tmp

export RESULT_DIR=${RESULT_DIR:-"/tmp/tests/ad-hoc"}
[ ! -d "$RESULT_DIR" ] && mkdir $RESULT_DIR

export LOGFILE=${RESULT_DIR}/@Get_Jira_test_ids@Click_here_for_details  

# For reporting.
WARNING="<span style=\"color:#ee0000;font-weight:bold;font-size:14px\">WARNING:</span>"

printf "\n<u>Gathering Jira ids for user story <b>$USER_STORY</b> (if it exists).</u>\n\n" >> $LOGFILE

#
# Process the user stories.
#
printf "Getting test cases from Jira for user story #$1 ...\n" >> $LOGFILE

#
# Go to JIRA and get the ids (requires you to be in the intranet or VPN).
#
wget -O /tmp/_jira_issues_tmp.html \
     --no-check-certificate       \
     --user=$U --password=$P      \
     ${B}${USER_STORY}?os_authType=basic >/dev/null 2>&1

#
# Strip out the numbers from the html.
#
awk 'BEGIN{
    FOUND = ""
    while ( getline < "/tmp/_jira_issues_tmp.html" ){

        if ( $0 ~ /dt title="is tested by/ ){ FOUND = "Y" }

        if ( $0 ~ /div id="show-more-links"/ ){ break }

        if ( $0 ~ /span title="OWD-/ ){
            x = $0
            gsub(/^.*span title=\"OWD-/, "", x)
            gsub(/:.*$/, "", x)
            print x
        }
    }
}'| tee $CACHE_BASE.$USER_STORY.tmp

#
# If we found nothing, try the previous list (if available).
#
x=$(wc -l $CACHE_BASE.$USER_STORY.tmp 2>/dev/null | awk '{print $1}')
if [ "$x" == "0" ]
then
    #
    # Try using the cache.
    #
    rm $CACHE_BASE.$USER_STORY.tmp
    printf "$WARNING Unable to return Jira test cases for $USER_STORY, trying cache ..." >> $LOGFILE
    
    if [ -f $CACHE_BASE.$USER_STORY ]
    then
        cat $CACHE_BASE.$USER_STORY
        printf " sucess!\n\n" >> $LOGFILE
    else
        printf " <b>Failed!</b> Cannot find test cases in jira cache for $USER_STORY, sorry!\n\n" >> $LOGFILE
        exit 1
    fi
else
    #
    # We got the list - refresh the previous cache with the new list.
    #
    mv $CACHE_BASE.$USER_STORY.tmp $CACHE_BASE.$USER_STORY
fi

printf "\nFound <b>$(wc -l $CACHE_BASE.$USER_STORY | awk '{print $1}')</b> IDs. \n\n" >> $LOGFILE