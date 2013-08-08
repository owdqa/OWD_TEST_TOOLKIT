#
# Splits the current '$line' into components, decides which css palette to use and creates
# the table row.
#
test_num=$(         echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
test_result_str=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
test_passes=$(      echo "$line" | awk 'BEGIN{FS="\t"}{print $3}')
test_total=$(       echo "$line" | awk 'BEGIN{FS="\t"}{print $4}')
test_desc=$(        echo "$line" | awk 'BEGIN{FS="\t"}{print $5}'| sed -e "s/\(blocked\)/<b>\1<\/b>/I")
test_time=$(        echo "$line" | awk 'BEGIN{FS="\t"}{print $6}')

#
# Color this row depending on what happened.
#
title="Click this to see the test run details."
[ ! "$test_result_str" ] && test_result="$EX_PASSES_STR"

#
# Create the summary tab if this is the 'type' we are wanting this time.
#
[ "$TYPE" = "$test_result_str" ] && . $0.parts/create_summary_detail_row_html.sh
