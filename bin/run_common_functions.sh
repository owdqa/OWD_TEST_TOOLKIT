#
# Function to split the output from the test run into variables.
#
f_split_run_details(){
    test_num=""
    test_failed=""
    test_passes=""
    test_total=""
    test_desc=""

    test_num=$(     echo "$1" | awk 'BEGIN{FS="\t"}{print $1}' | sed -e "s/^#//")
    test_failed=$(  echo "$1" | awk 'BEGIN{FS="\t"}{print $2}')
    test_passes=$(  echo "$1" | awk 'BEGIN{FS="\t"}{print $3}')
    test_total=$(   echo "$1" | awk 'BEGIN{FS="\t"}{print $4}')
    test_desc=$(    echo "$1" | awk 'BEGIN{FS="\t"}{print $5}' | sed -e "s/^[ \t]*//" | sed -e "s/\"//g")
    
    x=$(echo "$1" | awk 'BEGIN{FS="\t"}{print NF}')
    if [ "$x" -ge 6 ]
    then
        test_time=$(    echo "$1" | awk 'BEGIN{FS="\t"}{print $6}')
    fi
}
