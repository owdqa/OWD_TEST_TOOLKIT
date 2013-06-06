#!/bin/bash

PROJNAM=${1:?"Please specify the project to search for."}

# Use PYTHONPATH to get the location of $PROJNAM etc...
x=$(python <<!
import sys
print sys.path
exit()
!
)
IFS=', ' read -a array <<< "$x"
for element in "${array[@]}"
do
    el=$(echo $element | sed -e "s/'//g")
    ck=$(basename $el | egrep "^$PROJNAM")
    if [ "$ck" ]
    then
        install_dir=$(dirname $el)
        if [ "$install_dir" ]
        then
            echo "$install_dir"
            exit 0
        fi
    fi
done
