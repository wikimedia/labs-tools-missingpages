#!/usr/bin/env python
#-*- coding: utf-8 -*-

##############################################

import cgi
import sys
import os
from wmflabs import db
conn = db.connect("s52964__missingpages_p")

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
if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	title = qs['title'][0]
	if qs['whatlinkshere'][0] == "yes":
		whatlinkshere = True
	else:
		whatlinkshere = False
else:
	if len(sys.argv) > 1:
		title = sys.argv[1]
		if len(sys.argv) == 2:
			if sys.argv[2] == "yes":
				whatlinkshere = True
			else:
				whatlinkshere = False
		else:
			print "Max 2 params"
	else:
		print "Při spouštění z příkazové řádky musí být předány parametry"

cur = conn.cursor()
with cur:
	cur.execute("SET NAMES utf8;")

cur = conn.cursor()
with cur:
	sql = 'SELECT title FROM missingPages WHERE title NOT LIKE "%../%" AND title LIKE "' + title + '%" ORDER BY title LIMIT 100'
	cur.execute(sql)
	data = cur.fetchall()

if len(data) == 0:
	print '<p>Nebyly nalezeny žádné výsledky. <a href="index.html">Vraťte se</a> a zkuste jiný dotaz.'
	quit()

if len(data) > 100:
	more = True
else:
	more = False

print "<ol>"
if whatlinkshere:
	for row in data:
		print '<li><a href="https://cs.wikipedia.org/wiki/' + row[0] + '">' + row[0] + '</a> (<a href="https://cs.wikipedia.org/wiki/Special:WhatLinksHere/' + row[0] + '">odkazy</a>)</li>'
else: 
	for row in data:
		print '<li><a href="https://cs.wikipedia.org/wiki/' + row[0] + '">' + row[0] + '</a></li>'
print "</ol>"
if more:
	pass
	#TODO: Some logic for more than 100 rows

print """
        </body>
</html>
"""
