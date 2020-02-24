#!/bin/bash

echo $1, $2

# $1 is analysis options - ".mao" file
# $2 is sequence data - ".meg" file

./megacc -a $1 -d $2 -o mega_output
