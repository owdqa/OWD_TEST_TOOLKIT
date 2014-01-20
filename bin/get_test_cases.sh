#!/bin/bash
#
# A standalone executable to return a list of test cases from a test folder.
#
TYPE=${1:?"Syntax: $0 <test type>"}

export RESULT_DIR=${RESULT_DIR:-"/tmp/tests/ad-hoc"}
[ ! -d "$RESULT_DIR" ] && mkdir $RESULT_DIR

export LOGFILE=${RESULT_DIR}/@Get_test_ids@Click_here_for_details
cp /dev/null $LOGFILE

for TYPE in $(echo "$@")
do
	printf "\n<u>Gathering ids for test group <b>$TYPE</b>...</u>\n\n" >> $LOGFILE

    x=""
    if [ -d "$owd_test_cases_DIR/tests/$TYPE" ]
    then
    	while read num
    	do
    		x="$x $num"
    done <<EOF
        $(
        ls $owd_test_cases_DIR/tests/$TYPE/test_*.py   | \
        awk 'BEGIN{FS="/"}{print $NF}'                 | \
        sed -e "s/^test_\([A-Z0-9a-z]*\).py/\1/"
        )
EOF
    fi
	
	if [ ! "$x" ]
	then
		printf " <b>Failed!</b> Cannot find test cases for $TYPE (they need to be in folder $owd_test_cases_DIR/tests/$TYPE)!\n\n" >> $LOGFILE
	else
		echo "$x"
		printf "\nFound <b>$(echo "$x" | wc -w)</b> IDs. \n\n" >> $LOGFILE
	fi
done