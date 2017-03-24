##Run on tools-db

use s52964__missingpages_p;
drop table if exists missingPagesOld;
rename table missingPages to missingPagesOld;
rename table missingPagesNew to missingPages;
