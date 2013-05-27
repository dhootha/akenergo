#!/bin/sh

if [ $# -ne 1 ]

then

        echo "Bad Arguments"
        echo "-----------------------------------"
        echo "USAGE : 7za.sh  version"
        echo "-----------------------------------"
        exit 1
else   
       7z a  akenergo_project-$1.7z akenergo_project/ 
       sha1sum  akenergo_project-$1.7z  > akenergo_project-$1.7z.sha1
fi



