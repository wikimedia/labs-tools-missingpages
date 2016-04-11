<?php

    // This script is released under terms of GNU GPL license
    // See file COPYING for more information
     
    //Input: file with XML dump, only last revision, content only (no userpages and discussions)
    $XmlFilename = 'cswiki-latest-pages-articles.xml';
    //From MediaWiki:Disambiguationspage
    $DisambigTemplates = 'rozclist';
    //Output intermediate files
    $OutputMissing = 'MISSLINK.txt';
    $OutputLinkcount = 'NLINK.txt';
    $OutputDisabmig = 'ROZCLIST.txt';
    $OutputRedirects = 'REDIRLIST.txt';
     
    set_time_limit(0);
     
    if (function_exists('mb_internal_encoding')) mb_internal_encoding("UTF-8");
         
    function LinesFromFile($FileName) {
        $in = file_get_contents($FileName);
        $in = str_replace("\r", '', $in);
        return explode("\n", $in);
    }
     
    $TemplateList = join('|', LinesFromFile($DisambigTemplates));
    $TemplateList = preg_replace('/\|+$/', '', $TemplateList);
    $TemplateRegexp = "\\{\\{(".$TemplateList.")\\}\\}";
     
    function microtime_float() {
        list($usec, $sec) = explode(" ", microtime());
        return ((float)$usec + (float)$sec);
    }
     
    function FirstUpper($str) {
        return mb_strtoupper(mb_substr($str, 0, 1)).mb_substr($str, 1);
    }
     
    $ScriptTime = microtime_float();
     
    function TransformContent($PageText, $Title) {
        global $NumLinks, $LinkCount, $PageExist, $TemplateRegexp, $IsRedirect, $IsDisambig;
        if (preg_match("/$TemplateRegexp/im", $PageText)) {
            $IsDisambig[$Title] = 1;
        }
        if (preg_match("/^#\s*redirect\s*\[\[([^\]]*)\]\]/im", $PageText, $Matches)) {
            $IsRedirect[$Title] = $Matches[1];
        }
        $PageExist[$Title] = 1;
        if (!preg_match_all('/\[\[ *:?([^\[\]\|:#\{]*[^\[\]\|:#\{ ])[^\[\{\]:]*\]\]/', $PageText, $Matches)) return '';
        $LinkArray = array_unique($Matches[1]);
        sort($LinkArray);
        $NumLinks .= count($LinkArray)."\t$Title\n";
        foreach($LinkArray as $LinkItem) {
            $LinkItem = FirstUpper(strtr($LinkItem, '_', ' '));
            $LinkCount[$LinkItem]++;
        }
    }
     
    $NumberOfArticles = 0;
    function EndTextElement() {
        global $ParsedTitle, $ParsedContent, $NumberOfArticles;
        if ($ParsedTitle == 'Wikipedie:Nejžádanější články' || preg_match('/^Wikipedie:(Chybějící stránky|Seznam rozcestníků|Chybějící primární články|Seznam nejvíce odkazovaných rozcestníků)/', $ParsedTitle)) {
            $ParsedTitle = '';
            $ParsedContent = '';
            return;
        }
        if ($NumberOfArticles % 100 == 0) {
            echo "title: $NumberOfArticles $ParsedTitle\n";
            flush();
            ob_flush();
        }
        TransformContent($ParsedContent, $ParsedTitle);
        $NumberOfArticles++;
        $ParsedTitle = '';
        $ParsedContent = '';
    }
     
    function FinalizeOutput() {
        global $NumLinks, $LinkCount, $PageExist, $ScriptTime, $OutputMissing, $OutputLinkcount, $IsDisambig, $IsRedirect, $OutputRedirects, $OutputDisabmig;
        $DisambigOutput = array();
        $RedirectOutput = array();
        foreach($PageExist as $TheKey => $TheValue) {
            if ($IsDisambig[$TheKey]) {
                $DisambigOutput[$TheKey] = $LinkCount[$TheKey];
            }
            if ($IsRedirect[$TheKey]) {
                $RedirectOutput[$TheKey] = $LinkCount[$TheKey];
            }
            unset($LinkCount[$TheKey]);
        }
        $MissingOutput = '';
        foreach($LinkCount as $TheKey => $TheValue) {
            $MissingOutput .= "$TheValue\t$TheKey\n";
        }
        foreach($DisambigOutput as $TheKey => $TheValue) {
            $DisambigTextOutput .= "$TheValue\t$TheKey\n";
        }
        foreach($RedirectOutput as $TheKey => $TheValue) {
            $RedirectTarget = $IsRedirect[$TheKey];
            $RedirectTextOutput .= "$TheValue\t$TheKey\t$RedirectTarget\n";
        }
        $f = fopen($OutputLinkcount, "wb");
        fwrite($f, $NumLinks, 999999999);
        fclose($f);
        $f = fopen($OutputMissing, "wb");
        fwrite($f, $MissingOutput, 999999999);
        fclose($f);
        $f = fopen($OutputDisabmig, "wb");
        fwrite($f, $DisambigTextOutput, 999999999);
        fclose($f);
        $f = fopen($OutputRedirects, "wb");
        fwrite($f, $RedirectTextOutput, 999999999);
        fclose($f);
        $ScriptTime2 = microtime_float();
        $Duration = $ScriptTime2-$ScriptTime;
        echo "$Duration sec\n";
        flush();
        ob_flush();
        die();
    }
     
    function XmlStartElementHandler($p, $name, $attr) {
        global $ParseMode;
        if ($name == 'TITLE') $ParseMode = 1;
        else if ($name == 'TEXT') $ParseMode = 2;
        else $ParseMode = 0;
    }
    function XmlEndElementHandler($p, $name) {
        global $ParseMode;
        if ($name == 'TEXT') {
            EndTextElement();
        }
        $ParseMode = 0;
    }
     
    function XmlDataHandler ($p, $data) {
        global $ParseMode, $ParsedTitle, $ParsedContent;
        if ($ParseMode == 2) {
            $ParsedContent .= $data;
            return;
        }
        if ($ParseMode == 0) return;
        if ($ParseMode == 1) {
            $ParsedTitle .= $data;
            return;
        }
    }
     
    $ParseMode = 0;
     
    function ParseTheDump($FileName) {
        $XmlParser = xml_parser_create('utf-8');
        xml_parser_set_option($XmlParser, XML_OPTION_SKIP_WHITE, 1);
        xml_set_element_handler($XmlParser, 'XmlStartElementHandler', 'XmlEndElementHandler');
        xml_set_character_data_handler($XmlParser, 'XmlDataHandler');
        if (!($FileHandle = fopen($FileName, "rb"))) {
            die("could not open XML input");
        }
        while ($data = fread($FileHandle, 1024 * 1024)) {
            if (!xml_parse($XmlParser, $data, feof($FileHandle))) {
                die(sprintf("XML error: %s at line %d", xml_error_string(xml_get_error_code($XmlParser)),
                    xml_get_current_line_number($XmlParser)));
            }
        }
        fclose($FileHandle);
        xml_parser_free($XmlParser);
    }
     
    ParseTheDump($XmlFilename);
    FinalizeOutput();
?>
