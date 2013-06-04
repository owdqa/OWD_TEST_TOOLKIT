#!/bin/bash
#
# Recreates the table of tests covered, to be inserted into a 
# README.md file for a test project area (utils / apps / whatever).
# (Assumes it's already in the required folder.)
#
EXECDIR=$(pwd)
THISDIR=$(dirname $0)
COREFILE=$1

#
# Get the class name.
#
CLASS=$(grep -i "class" $1 | head -1 | awk '{print $2}' | sed -e "s/(.*$//")
echo "#$CLASS
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>"
  

#
# Specify the file to use (utils is a bit different since it uses all of them).
#
if [ "$COREFILE" = "utils.py" ]
then
	FINDFILE="."
else
    FINDFILE="$COREFILE"
fi


#
# Do like this to capture the even where parameters are on different lines.
#
grep -l "def " $(find $FINDFILE -name "*.py") | grep -v "__init__" | while read fnam
do
	#
	# The filename.
	#
	FILENAME=$(echo $fnam | awk 'BEGIN{FS="/"}{print $NF}')

    IN_METHOD="N"
    IN_DESC="N"
    cat $fnam | while read line
    do
    	x=$(echo $line | grep "def " | grep -v "__init__")
    	if [ "$x" ]
    	then
    		IN_METHOD="Y"
    		
		    #
		    # The method name.
		    #
		    METHOD=$(echo $line | awk '{print $2}' | sed -e "s/ *(.*$//")
    	fi
    	
    	#
    	# Parameters.
    	#
    	if [ "$IN_METHOD" = "Y" ]
    	then
    	   PARAMS=$(echo $line | sed -e "s/^.*(//" | sed -e "s/[ ():]//g" | sed -e "s/,/<br>\n/g" | grep -v "self")
    	fi

        #
        # At the end of the method def?
        #
        x=$(echo $line | egrep ":$")
        if [ "$x" ]
        then
            if [ "$IN_METHOD" = "Y" ]
            then
                #
                # We finished with a method, now see if we can get a description.
                #
                IN_METHOD="N"
                IN_DESC="Y"
                continue
            fi
        fi
        
        #
        # Description.
        #
        if [ "$IN_DESC" = "Y" ]
        then
        	x=$(echo $line | awk '{print $1}' | egrep "^#")
        	if [ "$x" ]
        	then
	        	while read descline
	        	do
	                DESC="$DESC $descline"
	        	done<<EOF
	        	$(echo $line | grep "#" | sed -e "s/^.*#//")
EOF
	        else
                #
                # We just finished looking at a method's description, 
                # so output all the method's details we gathered.
                #
                echo "<tr>"
                echo "<td align=center>$METHOD</td>"
                echo "<td align=left>$PARAMS</td>"
                echo "<td align=left>$DESC</td>"
                echo "</tr>"
                
	            IN_DESC="N"
	            DESC=""
        	fi
        fi

    done
done

echo  "</table>"