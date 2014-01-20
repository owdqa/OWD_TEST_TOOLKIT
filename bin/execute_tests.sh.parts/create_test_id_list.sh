#
# Set up test list (using test type, if specified, or test numbers.
#
TESTS=""
for user_story in $(echo "$@")
do
    x=$(echo "$user_story" | egrep "[A-Z]+[0-9]+[a-z]+")
    y=$(echo "$user_story" | egrep "^[0-9]+$")

    if [ $x ] || [ $y ]
    then
        #
        # This is an id - no need to get the children for it.
        #
        TESTS="$TESTS $user_story"
        continue
    else
        x=$($OWD_TEST_TOOLKIT_BIN/get_test_cases.sh $user_story)
        [ "$x" ] && TESTS="$TESTS $x"
   fi
done

#
# Order the list uniquely.
#
x=$(echo "$TESTS")
TESTS="$x"

NUMBER_OF_TESTS=$(echo "$TESTS" | wc -w)
