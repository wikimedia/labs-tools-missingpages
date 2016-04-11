#!/usr/bin/env python

import cgi
import os
from wmflabs import db
conn = db.connect("s52741__urbanecmbot")

print 'Content-type: text/html\n'

QS = os.environ['QUERY_STRING']
qs = cgi.parse_qs(QS)

title = qs['title'][0]

cur = conn.cursor()
with cur:
	sql = 'SELECT title FROM missingPages WHERE title LIKE "' + title + '%"'
	cur.execute(sql)
	data = cur.fetchall()
if len(row) > 100:
	more = True
else:
	more = False
i = 0
print "<ol>"
for row in data:
	print "<li>" + row[0] + "</li>"
print "</ol>"
if more:
	pass
	#TODO: Some logic for more than 100 rows
