#!/bin/bash

# find anything not matching the link in firefox.log
while read line 
do 
    if [ $line != "https://en.wikipedia.org/wiki/The_Conversation" ]
    then
        echo $line
    fi
done < $1