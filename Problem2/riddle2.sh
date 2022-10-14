#!/bin/bash

# to locate the files in objects
for file in objects/*/*
do

    # uncomment to find all the files
    # git cat-file ${file:8:2}${file:11:4} -p

    # uncomment to find the seed
    # git cat-file ${file:8:2}${file:11:4} -p | grep -i "seed"

    # uncomment to find the shares
    git cat-file ${file:8:2}${file:11:4} -p | grep -i "shares"

done