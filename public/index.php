<!DOCTYPE html>
<html lang="cs-cz">
	<head>
		<meta charset="utf-8" />
		<title>Chybějící stránky</title>
	</head>
	<body>
		<form method="GET" action="process.py">
			<p>Zadejte začátek názvu</p>
			<input type="text" name="title" />
			<input type="submit" />
			<p>S odkazy na Speciální:Odkazuje sem na Wikipedii</p>
			<input type="radio" value="yes" name="whatlinkshere" /> Ano<br />
			<input type="radio" value="no" checked="true" name="whatlinkshere" /> Ne<br />
			<input type="hidden" value="0" name="offset" />
		</form>
		<p>Další odkazy</p>
		<ol>
			<li><a href="process.py?title=a&offset=0&whatlinkshere=no&special=first">První výpis bez odkazů na Speciální:Odkazuje sem</a></li>
			<li><a href="process.py?title=a&offset=0&whatlinkshere=yes&special=first">První výpis s odkazy na Speciální:Odkazuje sem</a></li>
			<li><a href="process.py?title=a&offset=0&whatlinkshere=no&special=last">Poslední výpis bez odkazů na Speciální:Odkazuje sem</a></li>
			<li><a href="process.py?title=a&offset=0&whatlinkshere=yes&special=last">Poslední výpis s odkazy na Speciální:Odkazuje sem</a></li>
		</ol>
		<br/>
		<p>Program využívá dat z <?php echo(file_get_contents("/data/project/missingpages/missingpages/public/date.txt")); ?> </p>
	</body>
</html>
