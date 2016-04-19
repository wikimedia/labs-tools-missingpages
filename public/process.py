#!/usr/bin/env python
#-*- coding: utf-8 -*-

##############################################

import cgi
import sys
import os
from wmflabs import db
conn = db.connect("s52964__missingpages_p")

#Print header
print 'Content-type: text/html\n'

#Print header of html document
print """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8" />
                <title>Chybějící stránky</title>
        </head>
        <body>
"""
###############FUNCTIONS######################
#Print end header
def endHeader():
	print """
        </body>
	</html>
	"""
	quit()
#Parse webargs if present
if 'QUERY_STRING' in os.environ:
	nosql = False
	reverseMsg = False
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	title = qs['title'][0]
	if qs['whatlinkshere'][0] == "yes":
		whatlinkshere = True
	else:
		whatlinkshere = False
	try:
		offset = int(qs['offset'][0])
	except:
		print "Špatně nastavený offset, nastavena 0"
		offset = 0
	if 'special' in qs:
		if qs['special'][0] == 'first':
			sql = 'SELECT title FROM missingPages ORDER BY title LIMIT ' + str(offset) + ', 100'
			nosql = True
		elif qs['special'][0] == 'last':
			sql = 'SELECT title FROM missingPages ORDER BY title DESC LIMIT ' + str(offset) + ', 100'
			reverseMsg = True
			nosql = True
		else:
			print "<p>Nepodporovaná hodnota speciálního parametru</p>"
			endHeader()
#Parse args on cmdline or throw error
else:
	whatlinkshere = False
	offset = 0
	if len(sys.argv) > 1:
		title = sys.argv[1]
		if len(sys.argv) > 3:
			if sys.argv[2] == "yes":
				whatlinkshere = True
			else:
				whatlinkshere = False
			try:
				offset = int(sys.argv[3])
			except:
				print "Špatně nastavený offset, nastavena 0"
				offset = 0
		elif len(sys.argv) == 3:
			if sys.argv[2] == "yes":
				whatlinkshere = True
			else:
				whatlinkshere = False
		elif len(sys.argv) > 4:
			print "Max 3 params"
			print """
			</body>
			</html>
			"""
			quit()
	else:
		print "Při spouštění z příkazové řádky musí být předány parametry"
		print """
		</body>
		</html>
		"""
		quit()

#Init db conn
cur = conn.cursor()
#Set names to utf so we could use non-ascii chars
with cur:
	cur.execute("SET NAMES utf8;")

#Init db conn
cur = conn.cursor()
#Fetch all missing pages from db
with cur:
	if nosql:
		pass
	else:
		sql = 'SELECT title FROM missingPages WHERE title NOT LIKE "%../%" AND title LIKE "' + title + '%" ORDER BY title LIMIT ' + str(offset) + ', 100'
	cur.execute(sql)
	data = cur.fetchall()

#If no data fetched, print it and quit
if len(data) == 0:
	print '<p>Nebyly nalezeny žádné výsledky. <a href="index.html">Vraťte se</a> a zkuste jiný dotaz.'
	print """
	</body>
	</html>
	"""
	quit()

#If we have more than 100 results, set it to var
cur = conn.cursor()
with cur:
	sql = 'SELECT COUNT(*) FROM missingPages;'
	cur.execute(sql)
	count = cur.fetchall()[0]
if count > 100:
	more = True
else:
	more = False

#Print results
print "<ol>"
if whatlinkshere:
	for row in data:
		print '<li><a href="https://cs.wikipedia.org/wiki/' + row[0] + '">' + row[0] + '</a> (<a href="https://cs.wikipedia.org/wiki/Special:WhatLinksHere/' + row[0] + '">odkazy</a>)</li>'
else: 
	for row in data:
		print '<li><a href="https://cs.wikipedia.org/wiki/' + row[0] + '">' + row[0] + '</a></li>'
print "</ol>"

#If we fetched more than 100 results, do something (see TODO)
if more:
	if reverseMsg:
		if whatlinkshere:
			prevm = '<a href="process.py?title=' + title + '&whatlinkshere=yes&offset=' + str(offset-100) + '">následující</a>'
			nextm = '<a href="process.py?title=' + title + '&whatlinkshere=yesoffset=' + str(offset+100) + '">předchozí</a>'
		else:
			prevm = '<a href="process.py?title=' + title + '&whatlinkshere=no&offset=' + str(offset-100) + '">následující</a>'
			nextm = '<a href="process.py?title=' + title + '&whatlinkshere=no&offset=' + str(offset+100) + '">předchozí</a>'
	else:
		if whatlinkshere:
			prevm = '<a href="process.py?title=' + title + '&whatlinkshere=yes&offset=' + str(offset-100) + '">předchozí</a>'
			nextm = '<a href="process.py?title=' + title + '&whatlinkshere=yesoffset=' + str(offset+100) + '">následující</a>'
		else:
			prevm = '<a href="process.py?title=' + title + '&whatlinkshere=no&offset=' + str(offset-100) + '">předchozí</a>'
			nextm = '<a href="process.py?title=' + title + '&whatlinkshere=no&offset=' + str(offset+100) + '">následující</a>'
	pprint = ""
	if (offset-100)<0:
		pass
	else:
		pprint += prevm
	if (offset+100)>count:
		pass
	else:
		pprint += "\t"
		pprint += nextm
	print pprint
endHeader()
