#!/bin/bash

mysql -hc1.labsdb < drop.sql
mysql -hc1.labsdb < updateSql.sql
mysqldump -hc1.labsdb u13367__urbanecm tmp > dump.sql
mysql -hc1.labsdb < drop.sql
