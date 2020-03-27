#! /bin/bash

set -e # exit on error

read -p "blog post name: " bpname # read in desired name 
filename="$(date +%F)-" # add current date
filename+=$filename
filename+="${bpname// /-}" # find and replace spaces with -
touch $filename.md # create empty file
datestr="$(date)"
echo -e '===========================' >> $filename.md # push string into file
echo -e $datestr >> $filename.md # push datestring into file
echo -e '---\nlayout: post\npublished: false\n---' >> $filename.md # push string into file
