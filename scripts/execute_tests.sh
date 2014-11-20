#!/bin/bash
#
# Manage the execution and reporting of all required tests.
#
export RUN_INPUT_LIST="$@"
export RESTART_COUNTER_LIMIT=50

. $0.parts/set_up_parameters.sh

. $0.parts/process_parameters_file.sh

. $0.parts/change_results_location.sh

. $0.parts/create_test_id_list.sh

. $0.parts/ensure_device_connected.sh

#
# RUN THE TESTS ...
#
cp /dev/null $REALTIME_SUMMARY
_scheduled_restart_counter=0

FAILED_TESTS=
for TEST_NUM in $(echo $TESTS)
do
    #
    # Set up some 'test id dependant' variables.
    #
    export TEST_NUM
    export ERR_FILE=${RESULT_DIR}/error_output
    export SUM_FILE=${RESULT_DIR}/${TEST_NUM}_summary
    export DET_FILE=${RESULT_DIR}/${TEST_NUM}_detail
    export TEST_FILE=$(find ./tests -name test_${TEST_NUM}.py)

	. $0.parts/build_test_description.sh

	. $0.parts/add_new_test_to_realtime_summary.sh

    . $0.parts/mark_test_as_execute_or_not.sh

    #
    # Restart the device every few test cases (should help a little)
    # unless it's set by a test case anyway.
    #
    if [ "$RUN_TEST" ]
	then
		#
		# If this test will reset the device anyway, then
		# just reset the counter.
		#
		x=$(egrep "^[^#]*_RESTART_DEVICE *= *True" $TEST_FILE)
		if [ "$x" ]
		then
            _scheduled_restart_counter=0
		else
            _scheduled_restart_counter=$(($_scheduled_restart_counter+1))
			unset SCHEDULED_RESTART
			
		    if [ $_scheduled_restart_counter -ge $RESTART_COUNTER_LIMIT ]
		    then
		        export SCHEDULED_RESTART="Y"
		        _scheduled_restart_counter=0
		    fi
		fi
	fi
    

    . $0.parts/execute_test.sh
    
    . $0.parts/record_test_run_details.sh
    
    . $0.parts/update_run_summary_totals.sh
    
    . $0.parts/report_realtime_summary.sh

done

. $0.parts/output_final_summary_info.sh


#
# For Jenkins - if we didn't pass every tests then exit as 'fail' (non-zero).
#
#if [ $UNEX_FAILS -gt 0 ]
#then
#    exit 1
#fi

if [ $UNEX_FAILS -gt 0 ]
then
    # Calculating error rate
    P=$(($EX_PASSES + $UNEX_PASSES))
    F=$(($EX_FAILS + $UNEX_FAILS + $AUTOMATION_FAILS))
    T=$(($P + $F))
    ERROR_RATE=$((($F*100)/$T))
    printf "\n\nERROR RATE = %s %%\n\n" $ERROR_RATE
    # if error rate less than 20% set build as unstable
    if [ $ERROR_RATE -lt 20 ]
    then
        printf "\nJOB_UNSTABLE\n"
    fi
    exit 1
fi
printf "\nFAILED TESTS: $FAILED_TESTS\n"
