#!/bin/bash

findme.sh "-l tap" | while read fnam
do
    sed -e "s/self\.marionette\.tap(\([^)]*\))/\1.tap()/"  $fnam > $fnam.new
    mv $fnam.new $fnam
done
