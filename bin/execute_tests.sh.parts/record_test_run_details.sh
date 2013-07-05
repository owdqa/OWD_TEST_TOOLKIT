#
# Record the test run details.
#
test_failed=""
test_passes=""
test_total=""
if [ -f "$SUM_FILE" ]
then
    line="$(tail -1 $SUM_FILE)"
    test_passes=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
    test_failed=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
    test_total=$(   echo "$line" | awk 'BEGIN{FS="\t"}{print $3}')
fi

#
# A bit 'hacky', but if, for ANY reason, these are still
# not set, then set them to 'something'.
# (I'm finding certain build issues can cause a mess here!)
#
test_passes=${test_passes:-"?"}
test_failed=${test_failed:-"1"}
test_total=${test_total:-"?"}


