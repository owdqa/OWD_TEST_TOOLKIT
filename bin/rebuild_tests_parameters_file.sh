#!/bin/bash
#
# Rebuilds the 'parameters' file for you tests.
# (Must be run from the test 'root' folder).
#
if [ ! -d "tests" ]
then
	printf "\nERROR: './tests' folder not found!\n"
	printf "\nThis must be run from the top level folder for your tests (the parent of the './tests' folder).\n\n"
	exit 1
fi

export THISPATH=$(dirname $0)
export EXECPATH=$(pwd)

paramFile="$EXECPATH/tests/parameters"
TMPFILE="/tmp/params.tmp"
cp /dev/null $TMPFILE

if [ -f "$paramFile" ]
then
	cp $paramFile /tmp
	echo "(The previous 'parameters' file has been copied to /tmp in case you need it.)"
fi

echo "################################################################################
#
# These are the parameters for your tests. If any of these are left blank,
# you will be prompted for a value when you run that test.
#
# There must be no space between the "=" and your value.
#" > $paramFile

GENERAL_VARS=""
OWDTT=$THISPATH/../OWDTestToolkit

find $EXECPATH/tests $OWDTT/apps $OWDTT/utils -name "*.py" | grep -v utils.py | while read testfile
do
	EXT_VARS=""
	while read line
	do
		x=$(echo $line | sed -e "s/^.*.get_os_variable//")
		x=$(echo $x | sed -e "s/^(\(.*\))$/\1/")
		VARNAME=$(echo $x | awk 'BEGIN{FS=","}{print $1}' | sed -e "s/^.*\"\(.*\)\" *$/\1/")

		#
		# Ignore this varname - it's just for prompting.
		#
		if [ "$VARNAME" = "ENTER" ]
		then
			continue
		fi

		if [ "$VARNAME" ]
		then
			EXT_VARS="${EXT_VARS}export $VARNAME=\n"
		fi
	done << EOF
	$(grep ".get_os_variable" $testfile | grep -v "def get_os_variable" | sed -e "s/^[ ]*//" | egrep -v "#")
EOF

	if [ "$EXT_VARS" ]
	then
		printf "$EXT_VARS"
	fi
done | sort -u >> $paramFile
