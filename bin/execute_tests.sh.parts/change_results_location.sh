#!/bin/bash

if [ $ALTERNATIVE_RESULTS_DIR ]
then
	export RESULT_DIR="$ALTERNATIVE_RESULTS_DIR/$(date +"%d%m%Y_%H:%M")"
	if [ ! -d "$RESULT_DIR" ]
	then
		mkdir -p $RESULT_DIR
	else
	    rm -f $RESULT_DIR/*  >/dev/null 2>&1
	    rm -f $RESULT_DIR/.* >/dev/null 2>&1
	fi

	export HTML_SUMMARIES=$RESULT_DIR/.html_lines
	export HTML_INDEX=$RESULT_DIR/index.html
	export REALTIME_SUMMARY=$RESULT_DIR/realtime_summary

else
	echo "Remember: if you want the tests results to appear in another directory, set the ALTERNATIVE_RESULTS_DIR in your parameter file"

fi