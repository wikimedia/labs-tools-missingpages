#!/bin/bash

#Update data on replicas copy
sql cswiki < updateReplica.sql
#Dump them to a sql dump
mysqldump -h cswiki.labsdb s52964__missingpages missingPagesNew > ~/tmp/dump.sql
#Import the dump to tools-db
sql local < toLocal.sql
#Remove the temp file
rm ~/tmp/dump.sql
#Remove data on relica
sql cswiki < cleanUp.sql
#Rename the tables
sql local < rename.sh
#Actualize date
date '+%d. %m %Y' > /data/project/missingpages/missingpages/public/date.txt
