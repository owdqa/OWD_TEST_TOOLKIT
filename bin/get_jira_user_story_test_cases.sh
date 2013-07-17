#!/bin/bash
#
# A standalone executable to return a list of test cases from a Jira User Story.
#
TYPE=${1:?"Syntax: $0 <test type, or user story id>"}

U=$(egrep "^U" $HOME/.jira_login | awk '{print $2}')
P=$(egrep "^P" $HOME/.jira_login | awk '{print $2}')

CACHE_BASE=$HOME/tmp/_jira_test_cases
[ ! -d "$HOME/tmp" ] && mkdir $HOME/tmp

export RESULT_DIR=${RESULT_DIR:-"/tmp/tests/ad-hoc"}
[ ! -d "$RESULT_DIR" ] && mkdir $RESULT_DIR

export LOGFILE=${RESULT_DIR}/@Get_Jira_test_ids@Click_here_for_details

# For reporting.
WARNING="<span style=\"color:#ee0000;font-weight:bold;font-size:14px\">WARNING:</span>"

printf "===================================\n\n" >> $LOGFILE
printf "Gathering Jira ids for user story \"$TYPE\" (if it exists).\n\n" >> $LOGFILE

#
# Get the jira id's for the user stories.
#
. $OWD_TEST_TOOLKIT_CONFIG/jira_user_stories.sh

#
# Different types of 'type'.
#
x=$(echo "$TYPE" | egrep "^[0-9]*$")
if [ "$x" ]
then
    # This is already a parent id.
    ROOTIDs=$TYPE
else
    case $TYPE in
        
        "REGRESSION")  
           #
           # Run 'everything'.
           #
           printf "'REGRESSION' requested - get all jira ids for all known user stories ...\n\n" >> $LOGFILE
           for i in "${JIRA_PARENTS[@]}"
           do
               $0 $(echo "$i" | awk '{print $1}' | sed -e 's/\"//g')
           done
           exit;;
           
        "SMOKE")
           #
           # Run smoketests.
           #
           printf "'SMOKE' requested - THIS IS NOT SET UP YET, WE NEED THE JIRA PARENT ID FOR THIS!\n\n" >> $LOGFILE
           ROOTIDs="";;
           
        *)
           #
           # Run all test cases for this particular type.
           #    
           printf "$TYPE requested - gathering all ids for this ...\n\n" >> $LOGFILE       
           for i in "${JIRA_PARENTS[@]}"
           do
               PARENT=$(echo "$i" | awk '{print $1}')
               if [ "$PARENT" = "$TYPE" ]
               then
                    PARENTID=$(echo "$i" | awk '{for (i=2;i<=NF;++i)printf "%s ", $i; printf "\n"}')
                    ROOTIDs="$PARENTID"
                    break
               fi
           done;;
           
    esac
fi

if [ ! "$ROOTIDs" ]
then
    printf "$WARNING No user stories found for \"$TYPE\".\n\n" >> $LOGFILE
    exit
fi


#
# We may have more than one ROOTID for this type ...
#
for ROOTID in $(echo "$ROOTIDs")
do
    printf "Getting ID's from Jira for user story #$ROOTID ...\n\n" >> $LOGFILE
    
    #
    # Go to JIRA and get the ids (requires you to be in the intranet or VPN).
    #
    wget -O /tmp/_jira_issues_tmp.html \
         --no-check-certificate       \
         --user=$U --password=$P      \
         ${USER_STORIES_BASEURL}${ROOTID}?os_authType=basic >/dev/null 2>&1
    
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
    }'
done | tee $CACHE_BASE.$TYPE.tmp

#
# If we found nothing, try the previous list (if available).
#
x=$(wc -l $CACHE_BASE.$TYPE.tmp 2>/dev/null | awk '{print $1}')
if [ "$x" == "0" ]
then
    #
    # Try using the cache.
    #
    rm $CACHE_BASE.$TYPE.tmp
    printf "\n$WARNING Unable to return Jira test cases for $TYPE, trying cache ..." >> $LOGFILE
    
    if [ -f $CACHE_BASE.$TYPE ]
    then
        cat $CACHE_BASE.$TYPE
        printf "\n         Sucess!\n\n" >> $LOGFILE
    else
        printf "\n         ${ERROR}Failed!!</span> Cannot find test cases in jira cache for $TYPE, sorry!\n\n" >> $LOGFILE
        exit 1
    fi
else
    #
    # We got the list - refresh the previous cache with the new list.
    #
    mv $CACHE_BASE.$TYPE.tmp $CACHE_BASE.$TYPE
fi

printf "Found $(wc -l $CACHE_BASE.$TYPE | awk '{print $1}') IDs. \n\n" >> $LOGFILE