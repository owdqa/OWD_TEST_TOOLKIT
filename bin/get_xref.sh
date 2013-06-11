#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Script to return the cross-reference number.
#
export TEST_TYPE=$1
export ORIGINAL=$2

if [ ! "$OWD_XREF_FILE" ]
then
	echo "
ERROR: OWD_XREF_FILE variable isn't set!

To set it, use the format:

    export OWD_XREF_FILE=/full/path/to/xref_tests_table.txt
"
    exit 1
fi

egrep "^ORIGINAL,|$ORIGINAL," $OWD_XREF_FILE | \
sed -e "s/[ \t]*//g"                     | \
awk '
BEGIN{
    FS          = ","
    TEST_TYPE   = ENVIRON["TEST_TYPE"]      
    COLNUM      = 10000
}
{
    if ( COLNUM == 10000 )
    {
        for (i=1;i<=NF;++i){
            if ( $i == TEST_TYPE ){
                # Now we know which column to use.
                COLNUM = i
            }
        }
    }
    else{
        # This matches the ORGINAL and column.
        print $COLNUM
    }
}' | egrep -v "^$"