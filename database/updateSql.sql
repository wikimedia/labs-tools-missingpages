create table tmp
(
title varchar(256)
)
;
INSERT INTO tmp
select pl_title as title_to from cswiki_p.pagelinks left join cswiki_p.page on (pl_from=page_id)
where pl_namespace=0 and (page_namespace in (0, 2, 14, 100)
or (page_namespace=4 and (page_title like 'Požadované%' or page_title like 'Cizojazyčné%' or page_title like 'WikiProjekt%')))
and not exists (select * from cswiki_p.page where page_namespace=pl_namespace and page_title=pl_title) group by title_to;
