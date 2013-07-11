#!/bin/bash
#
# Manage the execution and reporting of all required tests.
#
. $0.parts/set_up_parameters.sh

. $0.parts/process_parameters_file.sh

. $0.parts/create_test_id_list.sh

. $0.parts/ensure_device_connected.sh

#
# RUN THE TESTS ...
#
cp /dev/null $REALTIME_SUMMARY
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
    
    
    . $0.parts/execute_test.sh
    
    
    . $0.parts/record_test_run_details.sh
    
    . $0.parts/update_run_summary_totals.sh
    
    . $0.parts/report_realtime_summary.sh

done

. $0.parts/output_final_summary_info.sh


#
# For Jenkins - if we didn't pass every tests then exit as 'fail' (non-zero).
#
if [ $UNEX_FAILS -gt 0 ]
then
    exit 1
fi