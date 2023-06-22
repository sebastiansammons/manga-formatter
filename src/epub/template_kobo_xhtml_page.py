# template_xhtml_page.py
top = """<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html>
<!--
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace" xmlns:ibooks="http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0" epub:prefix="ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0">
-->
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>[CH###PG##]</title>
    <link rel="stylesheet" type="text/css" href="../css/stylesheet.css" />
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=[WIDTH], height=[HEIGHT]"/>

<!-- kobo-style -->
<script xmlns="http://www.w3.org/1999/xhtml" type="text/javascript" src="js/kobo.js"/>

</head>

<body>
    <div class="fs">
    """
bottom = """
    </div>
</body>
</html>"""

xhtml_pages = """<div><img src="../images/[CH###PG##][ext]" alt="[CH###PG##]" class="singlePage"/></div>"""
