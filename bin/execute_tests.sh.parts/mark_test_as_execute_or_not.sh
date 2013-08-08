#
# Decide if this test will be executed or not.
#
if ([ "$OWD_NO_BLOCKED" ] && [ "$test_blocked" ]) || [ ! -f "$TEST_FILE" ]
then
    RUN_TEST=""
else
    RUN_TEST="Y"
fi
