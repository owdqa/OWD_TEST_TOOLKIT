#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Before we do anything, check the parameters file is okay.
#
$OWD_TEST_TOOLKIT_BIN/check_parameters_file.sh
[ $? -ne 0 ] && exit 1

mkdir /tmp/tests 2>/dev/null
chmod 777 /tmp/tests 2> /dev/null

export THISPATH=$(dirname $0)
export EXECPATH=$(pwd)
export RESULT_DIR="/tmp/tests/B2G_tests.$(date +%Y%m%d%H%M%S)"
export TESTDIR="./tests"
export PARAM_FILE="$HOME/.OWD_TEST_PARAMETERS"
export GET_XREF="$THISPATH/get_xref.sh"

[ ! -d "$RESULT_DIR" ] && mkdir -p $RESULT_DIR

if [ ! -f "$PARAM_FILE" ]
then
	echo "
Please edit the $HOME/.OWD_TEST_PARAMETERS file and add the variable values.
"
	exit
fi

################################################################################
#
# FUNCTIONS
#

#
# Function to run a test case ...
#
run_test(){
    export TEST_FILE="./tests/test_${1}.py"
    
    if [ "$TEST_TYPE" ]
    then
    	export TEST_NAME=$($GET_XREF "$TEST_TYPE" "$1")
    else
        export TEST_NAME=$1
    fi
    
    TEST_DESC=$(grep "_Description" $TEST_FILE | head -1 | sed -e "s/^[^\"]*\"\(.*\)\"/\1/")
    export TEST_DESC=${TEST_DESC:-"(no description found!)"}

    $OWD_TEST_TOOLKIT_BIN/run_test_case.sh 
}



################################################################################
#
# SET UP REQUIRED TEST VARIABLES
#

#
# If the param file exists, then load it (otherwise assume
# the caller has either set the values for this shell manually,
# or wants to be asked).
#
# NOTE: Modified to only set variables which haven't been set already.
if [ -f "$PARAM_FILE" ]
then
    while read line
    do
        var=$(echo $line | awk 'BEGIN{FS="="}{print $1}' | awk '{print $NF}')
        x=$(eval echo \$${var})
        if [ ! "$x" ]
        then
            line="export $line"
            eval $line
        fi
    done <<EOF
    $(egrep -v "^#" $PARAM_FILE)
EOF
fi

if [ ! "$OWD_XREF_FILE" ]
then
    printf "\n'OWD_XREF_FILE' variable not set!\n\n"
    exit 1
fi

if [ ! -f "$OWD_XREF_FILE" ]
then
    printf "\n$OWD_XREF_FILE is not a readable file!\n\n"
    exit 1
fi

#
# Firstly, if this is a TEST TYPE, then ignore everything else.
#
export TEST_TYPE=$(echo "$@" | awk 'BEGIN{FS="{"}{print $2}' | awk 'BEGIN{FS="}"}{print $1}')
if [ "$TEST_TYPE" ]
then
	#
	# This is a specific test - get the list ...
	#
	TESTS=""
    while read orig
    do
    	# The first line is the header - just ignore it.
    	if [ ! "$TESTS" ]
    	then
    		TESTS=" "
    		continue
    	fi
    	
    	# Use the function to return a test (if there is one!)
    NEW=$($GET_XREF "$TEST_TYPE" "$orig")
    	if [ "$NEW" ]
    	then
    	   # This test is part of this test type.
    	   TESTS="$TESTS $orig"
    	fi
    done << EOF
    $(cat $OWD_XREF_FILE | awk 'BEGIN{FS=","}{print $1}')
EOF
else

	#
	# Did the caller just want to run certain tests?
	#
	TESTS="$@"
	if [ ! "$TESTS" ]
	then
	    #
	    # No specific tests requested, so default to all tests.
	    #
	    while read line
	    do
	        TESTS="$TESTS $line"
	    done <<EOF
	    $(ls ./tests/test_*.py | grep -v "test_00" | sed -e "s/^.*test_//" | sed -e "s/\..*//")
EOF
	fi
	
	
	group_markers=""
	while true
	do
	    x=$(echo "$TESTS" | egrep "\[.*\]")    
	    if [ ! "$x" ]
	    then
	    	# no markers left.
	    	break
	    fi
	    
	    # Add the next group marker to the list using newlines (because we can't use space).
	    group=$(echo "$TESTS" | sed -e "s/^.*\(\[[a-zA-Z0-9 ]*\]\).*$/\1/")
	    group_markers="$group_markers\n$group"
	    
	    # Remove this marker from the TESTS variable.
	    x=$(echo $TESTS | sed -e "s/^\(.*\)\(\[[a-zA-Z0-9 ]*\]\)\(.*\)$/\1\3/")
	    TESTS="$x"
	done
		
	#
	# 'Unpack' any group selectors in the tests spec.
	#
	if [ "$group_markers" ]
	then
		while read group_marker
		do
			[ ! "$group_marker" ] && continue
			
			# Prepare the marker to be used in a grep ("[]" need escaped)
		    group_marker=$(echo $group_marker | sed -e "s/\[/\\\[/" | sed -e "s/\]/\\\]/")
		    
		    while read match_file
		    do
		        match_test=$(echo $match_file | \
		                     awk '{print $1}' | \
		                     awk 'BEGIN{FS="_"}{print $NF}' | \
		                     awk 'BEGIN{FS="."}{print $1}')
		        group_tests="$group_tests $match_test"
		    done <<EOF
		    $(grep "$group_marker" ./tests/test_*.py | grep "_Description")
EOF
	    done <<EOF2
	    $(printf "$group_markers")
EOF2
	fi
fi
	
#
# Order the list (uniquely).
#
TEST_TMP="$TESTS $group_tests"
TESTS=""
while read testnum
do
	TESTS="$TESTS $testnum"
done << EOF
$(echo "$TEST_TMP" | sed -e "s/ /\n/g" | sort -u)
EOF




#
# Run the tests ...
#
for i in $(echo $TESTS)
do
	[ ! -f ./tests/test_${i}.py ] && continue
	
    while read line
    do
        # If it's commented out ignore it.
        ISCOMMENTED=$(echo $line | awk '{print $1}' | egrep "^#")
        [ "$ISCOMMENTED" ] && continue

        VARNAM=$(echo $line | sed -e "s/^.*(\"//" | sed -e "s/\".*//")
        VARSTR=$(echo $line | sed -e "s/^.*, *\"//" | sed -e "s/\".*//")

        #
        # Ignore this 'variable' - just using it to prompt.
        #
        if [ "$VARNAM" = "ENTER" ]
        then
            continue
        fi

        #
        # Make sure it's not already set.
        #
        env_set=$(eval echo $`echo $VARNAM`)
        if [ ! "$env_set" ]
        then
            QUESTION=("${QUESTION[@]}" "$VARSTR")
            VARIABLE=("${VARIABLE[@]}" "$VARNAM")
        fi

    done << EOF
    $(grep -i ".get_os_variable" tests/test_${i}.py | grep -v "False)")
EOF
done

for ((i=0; i<=${#QUESTION[@]}; ++i))
do
    if [ "${QUESTION[$i]}" ]
    then
        Q="${QUESTION[$i]}"
        V="${VARIABLE[$i]}"

        if [ ! "$gotParams" ]
        then
            gotParams="Y"
            printf "\nSome of the tests you have chosen require input ...\n\n"
        fi

        ans=""
        while [ ! "$ans" ]
        do
            printf "$Q [$V]: "
            read ans
        done

        eval export $V="$ans" 2>/dev/null

    fi
done 


################################################################################
#
# NOW RUN THE TESTS ...
#
[ "$gotParams" ] && printf "\n\n"


#
# Establsh connection to device.
#
$OWD_TEST_TOOLKIT_BIN/connect_device.sh

if [ $? -ne 0 ]
then
    # There was a problem connecting the device - just quit.
    exit 1
fi


printf "\n\n(For test run details, see '*_detail' files in \"${RESULT_DIR}\".)\n\n"

#
# Now run tests as required.
#
PASSED=0
TOTAL=0
TCPASS=0
TCTOTAL=0
for i in $(echo $TESTS)
do
	if [ ! -f ./tests/test_${i}.py ]
	then
		echo "ERROR: Cannot find test for \"$i\"!"
		continue
	fi	

    results=$(run_test $i)
    exitCode=$?
    
    if [ $exitCode -eq 0 ]
    then
        TCPASS=$(($TCPASS+1))
    fi
    TCTOTAL=$(($TCTOTAL+1))
    
    errChk=$(echo $results | grep -i " unknown)" | awk '{print $2}' | grep "FAIL")
    if [ "$errChk" ]
    then
        #
        # Total failure - ignore and move on...
        #
        echo "$results"
        continue
    fi

    echo "$results"

    #
    # Get the totals (unless the exit code was due to the code
    # being broken).
    #
    #if [ $exitCode -ne 1 ]
    #then
        totals=` echo "$results" | sed -e "s/^[^(]*([^-]*- *\([^)]*\).*$/\1/"`
	    passed=$(echo "$totals"  | awk 'BEGIN{FS="/"}{print $1}' | awk '{print $1}' | egrep "^[0-9]*$")
	    total=$( echo "$totals"  | awk 'BEGIN{FS="/"}{print $2}' | awk '{print $1}' | egrep "^[0-9]*$")

	    passed=${passed:-0}
	    total=${total:-0}
	
	    PASSED=$(($PASSED+$passed))
	    TOTAL=$(($TOTAL+$total))
    #fi
    
done

printf "\nPassed $TCPASS/$TCTOTAL test cases ($PASSED/$TOTAL test actions in total).\n"

printf "\nDONE.\n\n"

#
# For Jenkins - if we didn't pass every tests then exit as 'fail' (non-zero).
#
if [ $TCPASS -lt $TCTOTAL ]
then
    exit 1
fi