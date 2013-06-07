#!/bin/bash
#
# Simple way to find a string in all *.py files in all subfolders.
#

egrep $1 $(find . -name "*.py" | grep -v gaiatest | grep -v "/build/") | sort
