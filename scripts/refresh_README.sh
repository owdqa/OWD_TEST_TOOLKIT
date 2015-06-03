#!/bin/bash
#
# Rebuilds the README.md files for each area.
#
THISDIR=$(dirname $0)
cd $THISDIR
BINDIR=$(pwd)

README="/tmp/README.md"

generate_api_table(){
    #
    # Generate api table for all files under this dir.
    #
    METHODS_LIST=""
    
    echo "<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>" >> $README
    
    #
    # Get all non-private functions in all files.
    #
    printf "Analysing \"$(basename $PWD)\" "
    while read fnam
    do
        IN_METHOD=""
        IN_PARAMS=""
        IN_COMMENT=""
        METHOD_DESC=""
        METHOD_PARAMS=""
        while read line
        do
            #
            # Get the method name.
            #
            method=$(echo $line | egrep "^[ \t]*def [ \t]*[a-zA-Z]" | sed -e "s/^.*def [ \t]*\([^(]*\).*$/\1/")
            if [ "$method" ]
            then
                printf "."
                METHOD_NAME="$method"
                IN_METHOD="Y"
                IN_PARAMS="Y"
                IN_COMMENT=""
                METHOD_DESC=""
                METHOD_PARAMS=""
            fi
            
            if [ "$IN_METHOD" ]
            then
                #
                # Get parameters?
                #
                if [ "$IN_PARAMS" ]
                then
                    PARAMS=$(echo $line | sed -e "s/^.*(self,* *//" | sed -e "s/):.*$//")
                    METHOD_PARAMS="$METHOD_PARAMS $PARAMS"
                    
                    EOP=$(echo $line | grep "):")
                    if [ "$EOP" ]
                    then
                        #
                        # We're at the end of the parameters for this method.
                        #
                        IN_PARAMS=""
                        IN_COMMENT="Y"
                        continue
                    fi
                fi
                
                #
                # Get comments?
                #
                if [ "$IN_COMMENT" ]
                then
                    COMMENT=$(echo "$line" | egrep "^[ \t]*#")
                    if [ "$COMMENT" ]
                    then
                        COMMENT=$(echo $COMMENT | sed -e "s/^.*#//")
                        METHOD_DESC="$METHOD_DESC $COMMENT"
                    else
                       #
                       # We're at the end of the comments for this method.
                       #
                       METHOD_PARAMS=$(echo "$METHOD_PARAMS" | sed -e "s/ *, */<br>/g")
                       
                       if [ "$METHODS_LIST" ]
                       then
                           METHODS_LIST="$METHODS_LIST
$METHOD_NAME|$METHOD_PARAMS|$METHOD_DESC"
                       else
                           METHODS_LIST="$METHOD_NAME|$METHOD_PARAMS|$METHOD_DESC"
                       fi
                       IN_COMMENT=""
                       IN_METHOD=""
                    fi
                fi
            fi
        done <<EOF2
        $(cat $fnam)
EOF2
    done <<EOF
    $(find . -name "*.py" | grep -v __)
EOF
    
    echo "$METHODS_LIST" | while read line
    do
        #
        # Strip leading and trainling whitespaces.
        #
        line=$(echo "$line" | sed -e "s/[ \t]*|[ \t]*/|/g")

        METHOD_NAME=$(  echo "$line" | awk 'BEGIN{FS="|"}{print $1}')
        METHOD_PARAMS=$(echo "$line" | awk 'BEGIN{FS="|"}{print $2}')
        METHOD_DESC=$(  echo "$line" | awk 'BEGIN{FS="|"}{print $3}')
        echo "
    <tr>
        <td align=center>$METHOD_NAME</td>
        <td align=left>$METHOD_PARAMS</td>
        <td align=left>$METHOD_DESC</td>
    </tr>
" >> $README

    done
    echo "</table>" >> $README
    printf " DONE.\n"
}


echo ""
echo "Building README.md file for 'apps'."
echo "==================================="
cd $BINDIR/../OWDTestToolkit/apps
cp /dev/null $README
cat README.md | while read line
do
    echo "$line" >> $README
    x=$(echo $line | grep "<!--api-->")
    if [ "$x" ]
    then
        #
        # For each 'app' ...
        #
        ls | while read appnam
        do
            [ ! -d "$appnam" ] && continue
            
            echo "#$appnam" >> $README
            cd $appnam
            generate_api_table            
            cd ..
        done
        break
    fi
done
[ -s "$README" ] && mv $README README.md




echo ""
echo "Building README.md file for 'utils'."
echo "==================================="
cd $BINDIR/../OWDTestToolkit/utils
cp /dev/null $README
cat README.md | while read line
do
    echo "$line" >> $README
    x=$(echo $line | grep "<!--api-->")
    if [ "$x" ]
    then
        generate_api_table
        break
    fi
done
[ -s "$README" ] && mv $README README.md


printf "\n\n"
