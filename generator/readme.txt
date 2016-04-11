These scripts are released under terms of GNU GPL license
See file COPYING for more information

date.txt = current date (first line, in "DD. MM. YYYY" format)
rozclist = list of disambiguation page templates (one name per line, without the namespace prefix)
rozc-blacklist.txt = list of names with brackets which are normal part of name (for rozc_check.pl)

parse.php: parse dump into intermediate files
cswiki-latest-pages-articles.xml -> MISSLINK.txt, NLINK.txt, REDIRLIST.txt, ROZCLIST.txt

miss.pl:
MISSLINK.txt -> missl

redir.pl:
REDIRLIST.txt -> redirl

rozc.pl:
ROZCLIST.txt -> rozcl

rozc_check.pl:
cswiki-latest-all-titles-in-ns0, ROZCLIST.txt -> rozc_check.txt