#!/bin/sh
##############################
#Thanks goes to ANAS for this script
##############################

#Substitute your postgresql root username in the below given line
PGUSER=energosite
#Substitute your postgresql root password in the below given line
#PGPASSWORD=11111111111
PGPASSWORD=22222222222222222
export PGUSER PGPASSWORD


pgpath=/opt/PostgreSQL/9.1/bin

tdate=`date +%d-%m-%Y`

if [ $# -lt 1 ]

# Check if there is atleast one argument [i.e the database whose dump is to be taken]
#First argument is mandatory - Databse name
#Second argument is optional - Destination path to save dump
then

        echo "Bad Arguments"
        echo "-----------------------------------"
        echo "USAGE : pg_dmp.sh  [database name]"
        echo "-----------------------------------"
        exit 1
else

#if one or more arguments were provided
        if [ $# -eq 1 ]
#if arguments provided is equal to 1
then
            rm -f  $1_$tdate*
            pg_dump $1 -f ./$1_$tdate.backup -x -O -b -v                            
            7z a $1_$tdate.backup.7z  $1_$tdate.backup
            rm -f  $1_$tdate.backup
        fi
        if [ $# -gt 1 ]
        #if arguments passed where greater than 1 then  show message
        then
            echo "Extra Arguments ignored"
        fi
fi

#reset PGUSER and PGPASSWORD
PGUSER=""
PGPASSWORD=""
export PGUSER PGPASSWORD
#End

#/opt/PostgreSQL/9.1/bin/pg_dump --host localhost --port 5432 --username "energosite" --no-password  --format custom --blobs --compress 9 --verbose --file "/home/uzer/pg_backup_energosite/energo" "energosite"
