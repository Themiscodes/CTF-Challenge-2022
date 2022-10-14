#!/bin/bash

# first argument is the cyphertext 
cyphertext = $1

# second the host
host = $2

# third the url for the post
url = $3

python riddle2.py $cyphertext $host $url