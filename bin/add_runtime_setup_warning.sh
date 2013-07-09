#!/bin/bash
#
# Adds a warning to the 'runtime setup' file.
#
echo "RUNTIME_WARNINGS: \"$RUNTIME_WARNINGS\""
if [ ! "$RUNTIME_WARNINGS" ]
then
	printf "\RUNTIME_WARNINGS variable not set (should be the filename for messages) - cannot report warnings.\n\n"
	exit 1
fi

WARNING_MSG=${1:-"(no warning reason given)"}

echo "[$(date)] : $WARNING_MSG" >> $RUNTIME_WARNINGS