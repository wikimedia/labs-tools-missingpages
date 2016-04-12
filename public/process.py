#!/usr/bin/env python
#-*- coding: utf-8 -*-

##############################################
#TODO: Work with non-ascii chars too

import cgi
import os
from wmflabs import db
conn = db.connect("s52741__urbanecmbot")

print 'Content-type: text/html\n'
print """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8" />
                <title>Chybějící stránky</title>
        </head>
        <body>
"""
QS = os.environ['QUERY_STRING']
qs = cgi.parse_qs(QS)

title = qs['title'][0]

cur = conn.cursor()
with cur:
	cur.execute("SET NAMES utf8;")

cur = conn.cursor()
with cur:
	sql = 'SELECT title FROM missingPages WHERE title NOT LIKE "%../%" AND title LIKE "' + title + '%" ORDER BY title'
	cur.execute(sql)
	data = cur.fetchall()

if len(data) == 0:
	print '<p>Na zadaný dotaz nebylo nic nalezeno. <a href="https://tools.wmflabs.org/urbanecmbot/missingPages">Vraťte se</a> a zkuste jiný.</p>'

if len(data) > 100:
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

print """
        </body>
</html>
"""
