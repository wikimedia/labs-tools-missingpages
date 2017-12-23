#!/usr/bin/env python
#-*- coding: utf-8 -*-

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


# Store the data into tools-db
conn = db.connect('s52964__missingpages_p')
with conn.cursor() as cur:
	sql = 'drop table if exists missingPagesNew;'
	cur.execute(sql)

with conn.cursor() as cur:
	sql = 'create table missingPagesNew(title varchar(256));'
	cur.execute(sql)

with conn.cursor() as cur:
	sql = 'set charset utf8;'
	cur.execute(sql)

for row in data:
	with conn.cursor() as cur:
		sql = 'insert into missingPagesNew (title) values("' + row[0].replace('"', '\\"') + '");'
		cur.execute(sql)
