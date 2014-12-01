#!/bin/bash
# Load both common and custom parameters from configuration files.
for line in `grep -e "^[a-zA-Z0-9_]*=" $PWD/.OWD_TEST_COMMON_PARAMETERS`
do
    export $line
done
for line in `grep -e "^[a-zA-Z0-9_]*=" $PWD/.OWD_TEST_CUSTOM_PARAMETERS`
do
    export $line
done
for line in `grep -e "^[a-zA-Z0-9_]*=" $HOME/.OWD_TEST_CI_PARAMETERS`
do
    export $line
done
