f_sub_variables_into_webpage(){
	#
	# Function to substitute a list of variables into the web page template.
	#
    cp $0.parts/web_page_template.html $HTML_INDEX
    for i in $(echo "$@")
    do
        z=$(echo "${!i}")
      
        export reps=$(grep -c "@$i@" $HTML_INDEX)
        [ $reps -eq 0 ] && continue
        
        for line in "$(cat $HTML_INDEX)"
        do
            x=$(echo "$line" | grep "@$i@")
            if [ "$x" ]
            then
                y=$(echo "$line" | sed -e "s/@$i@/%s/")
                printf "$y\n" "$z"
            else
                echo "$line"
            fi
        done > $HTML_INDEX.tmp
        
        mv $HTML_INDEX.tmp $HTML_INDEX
    done
}
