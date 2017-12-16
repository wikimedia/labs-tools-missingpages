#!/usr/bin/env python
#-*- coding: utf-8 -*-

import csv
from wmflabs import db


# Get the data from database
conn = db.connect('cswiki')
with conn.cursor() as cur:
	sql = '''select pl_title as title from pagelinks left join page on (pl_from=page_id)
	where pl_namespace=0 and (page_namespace in (0, 2, 14, 100)
	or (page_namespace=4 and (page_title like 'Požadované%' or page_title like 'Cizojazyčné%' or page_title like 'WikiProjekt%')))
	and not exists (select * from page where page_namespace=pl_namespace and page_title=pl_title) group by title;'''
	cur.execute(sql)
	data = cur.fetchall()

with open('data.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile, delimiter=';', quoting_char='"', quoting=csv.QUOTING_MINIMAL)
	for row in data:
		writer.writerow(row)
