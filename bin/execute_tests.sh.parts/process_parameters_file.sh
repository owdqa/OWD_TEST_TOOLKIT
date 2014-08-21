#!/bin/bash
# Load both common and custom parameters from configuration files.
export COMMON_PARAM_FILE="$PWD/.OWD_TEST_COMMON_PARAMETERS"
if [ -f "$COMMON_PARAM_FILE" ]
then
    while read line
    do
        var=$(echo $line | awk 'BEGIN{FS="="}{print $1}' | awk '{print $NF}')
        x=$(eval echo \$${var})
        if [ ! "$x" ]
        then
            x=$(echo "$line" | grep "export ")
            [ ! "$x" ] && line="export $line"
            eval $line
        fi
    done <<EOF
    $(egrep -v "^#" $COMMON_PARAM_FILE)
EOF
fi

export CUSTOM_PARAM_FILE="$PWD/.OWD_TEST_CUSTOM_PARAMETERS"
if [ -f "$CUSTOM_PARAM_FILE" ]
then
    while read line
    do
        var=$(echo $line | awk 'BEGIN{FS="="}{print $1}' | awk '{print $NF}')
        x=$(eval echo \$${var})
        if [ ! "$x" ]
        then
            x=$(echo "$line" | grep "export ")
            [ ! "$x" ] && line="export $line"
            eval $line
        fi
    done <<EOF
    $(egrep -v "^#" $CUSTOM_PARAM_FILE)
EOF
fi
