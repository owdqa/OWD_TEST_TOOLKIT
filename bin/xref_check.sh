#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Script to do a simple xref check of a test number.
#
export TEST_TYPE=$1
export TEST_NUM=$2

if [ ! "$OWD_XREF_FILE" ]
then
    echo "
ERROR: OWD_XREF_FILE variable isn't set!

To set it, use the format:

    export OWD_XREF_FILE=/full/path/to/xref_tests_table.txt
"
    exit 1
fi

awk '
BEGIN{
    FS          = ","
    TEST_TYPE   = ENVIRON["TEST_TYPE"]
    TEST_NUM    = ENVIRON["TEST_NUM"]
    XREF_FILE   = ENVIRON["OWD_XREF_FILE"]
    COLNUM      = 10000
	while ( getline < XREF_FILE )
	{
		if ( COLNUM == 10000 ){
			print $0
			for (i=1;i<=NF;++i){
				x = $i
				gsub(/[ \t]/, "", x)
				if ( x == TEST_TYPE ){
					COLNUM = i
					break
				}
			}
		}
        else{
        	x = $COLNUM
        	gsub(/[ \t]/, "", x)
        	if ( x == TEST_NUM ){
        		print $0
        	}
        }
    }
}' | egrep -v "^$"
