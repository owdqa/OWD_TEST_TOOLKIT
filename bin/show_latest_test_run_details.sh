#!/bin/bash

num=${1:?"Syntax: $0 <test number>"}

ls -ltd /tmp/tests/* | awk '{print $NF}' | while read dirnam
do
	if [ -f "$dirnam/${num}_detail" ]
	then
		cat $dirnam/${num}_detail
		exit
	fi
	if [ -f "$dirnam/0${num}_detail" ]
	then
		cat $dirnam/0${num}_detail
		exit
	fi
done
