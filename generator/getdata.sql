##Run on cswiki.labsdb
select pl_title as title from pagelinks left join page on (pl_from=page_id)
where pl_namespace=0 and (page_namespace in (0, 2, 14, 100)
or (page_namespace=4 and (page_title like 'Požadované%' or page_title like 'Cizojazyčné%' or page_title like 'WikiProjekt%')))
and not exists (select * from page where page_namespace=pl_namespace and page_title=pl_title) group by title;
