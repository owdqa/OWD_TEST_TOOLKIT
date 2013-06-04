#!/bin/bash
#
# Rebuilds the README.md files for each area.
#
THISDIR=$(dirname $0)
cd $THISDIR
BINDIR=$(pwd)

APISCRIPT=$BINDIR/rebuild_api_info_table.sh


#
# utils
#
cd $BINDIR/../OWDTestToolkit/utils
cat README.md | while read line
do
    echo "$line"
	x=$(echo $line | grep "<!--api-->")
	if [ "$x" ]
	then
		$APISCRIPT utils.py
		break
    fi
done > README.tmp
mv README.tmp README.md


#
# apps
#
cd $BINDIR/../OWDTestToolkit/apps
cat README.md | while read line
do
    echo "$line"
    x=$(echo $line | grep "<!--api-->")
    if [ "$x" ]
    then
    	ls app_*.py | while read APPFILE
    	do
            $APISCRIPT $APPFILE
    	done
        break
    fi
done > README.tmp
mv README.tmp README.md