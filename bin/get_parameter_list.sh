#!/bin/bash
#
# Returns a list of the variables that will be required by the test cases.
#
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Some variables are set during the tests (this list shouldn't change very often).
#
IGNORE_LIST=(
    "TEST_NAME" 
    "TEST_NUM"
    "TEST_DESC" 
    "DET_FILE" 
    "SUM_FILE" 
    "NO_KEYBOARD")

#
# Some variable names are built dynamically and may not be picked up.
#
INCLUDE_LIST=(
    "GMAIL_1_EMAIL"
    "GMAIL_1_PASS"
    "GMAIL_1_USER"
    "GMAIL_2_EMAIL"
    "GMAIL_2_PASS"
    "GMAIL_2_USER"
    "HOTMAIL_1_EMAIL"
    "HOTMAIL_1_PASS"
    "HOTMAIL_1_USER"
    "HOTMAIL_2_EMAIL"
    "HOTMAIL_2_PASS"
    "HOTMAIL_2_USER")
    
#
# Set the counter to the currnet size of the array.
#
include_count=${#INCLUDE_LIST[@]}

###################################################################
#
# Functions.
#

#
# Function to add variable names to the inclusion array.
#
addToArray(){
	INCLUDE_LIST[$include_count]="$1"
    include_count=${#INCLUDE_LIST[@]}
}

#
# Function to check if a value is in the exclude array.
#
excludeCheck(){
	ignore_var=""
    for x in ${IGNORE_LIST[*]}
    do
        if [ "$x" = "$1" ]
        then
            ignore_var="y"
            break
        fi
    done
    echo $ignore_var
}

#
# Function to get the variables into the inclusion array.
#
getVariables(){
    while read parameter
    do
        #
        # Should we ignore this variable?
        #
        ignore_var=""
        
        [ "$(excludeCheck $parameter)" ] && continue
        
        #
        # Nope - let's add it to the include array.
        #
        addToArray "$parameter"
    done <<EOF
    $(  $OWD_TEST_TOOLKIT_BIN/findme.sh get_os_variable     | \
        sed -e "s/^.*get_os_variable//"                     | \
        grep "(\""                                          | \
        awk '{FS=","}{print $1}'                            | \
        sed -e "s/[()\"]//g")
EOF
}



###################################################################
#
# Begin ...
#

#
# Get toolkit variables.
#
cd $OWD_TEST_TOOLKIT_DIR
getVariables

#
# Get test case variables.
#
cd $OWD_TEST_TOOLKIT_DIR/../owd_test_cases
getVariables


#
# Return the array in a way that makes it unique
for x in ${INCLUDE_LIST[*]}
do
	echo "$x"
done | sort -u