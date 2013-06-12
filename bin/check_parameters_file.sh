#!/bin/bash
#
# Builds the parameters file.
# If the file already exists, this will keep the current values.
# Any values that aren't present will be added (and set to nothing).
#
. $HOME/.OWD_TEST_TOOLKIT_LOCATION
params_file=$HOME/.OWD_TEST_PARAMETERS
array_count=0
declare -a NEW_PARAMETERS
[ -f "$params_file" ] && file_exists="y" || file_exists=""



###################################################################
#
# Functions.
#

#
# Function to add to the 'new PARAMETERS' array.
#
addToArray(){
    NEW_PARAMETERS[$array_count]="$1"
    array_count=${#NEW_PARAMETERS[@]}
}




###################################################################
#
# Begin...
#

#
# If the file doesn't exist then start by
# putting the header on (including the xref file parameter).
#
if [ ! "$file_exists" ]
then
	echo "#
# This is the parameters file for your tests. If any of these are left blank,
# you will be prompted for a value when you run that test.
#
# There must be no space between the = and your value.
#
OWD_XREF_FILE=$OWD_TEST_TOOLKIT_BIN/../owd_test_cases/Docs/xref_tests_table.txt
" > $params_file
fi


#
# Now build the list of missing parameter names.
#
while read param
do
	x=$(egrep "^${param}=" $params_file)
	if [ ! "$x" ]
	then
		#
		# This parameter isn't in the params file so add it to the array.
		#
		addToArray "$param"
	fi
done << EOF
$($OWD_TEST_TOOLKIT_BIN/get_parameter_list.sh)
EOF


#
# Now add the list of missing params to the params file (set to nothing).
#
if [ $array_count -gt 0 ]
then
	for x in ${NEW_PARAMETERS[*]}
	do
		echo "$x=" >> $params_file
	done
fi

#
# Now report any variables that are in the params file, but not set to
# anything (there might have been some in there already).
#
FIRST_TIME="Y"
while read line
do
	# It'll return a blank line if nothing is found)
	[ ! "$line" ] && continue
	
	if [ "$FIRST_TIME" ]
	then
		FIRST_TIME=""
		printf "\n\n* ** WARNING! **\n"
		printf "*\n* The following parameters are unset in $params_file:\n*\n"
	fi
	
	printf "*    "
	echo $line | sed -e "s/=$//"
done <<EOF
$(egrep "=$" $params_file)
EOF

if [ ! "$FIRST_TIME" ]
then
	printf "*\n* Please assign values to these parameters.\n\n"
	exit 1
fi

exit 0