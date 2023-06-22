# template_xhtml_toc.py
top = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"  xmlns:xml="http://www.w3.org/XML/1998/namespace" xmlns:ibooks="http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0" epub:prefix="ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0">
<!--
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
-->
<head>
    <title>Table of Contents</title>
</head>

<!-- kobo-style -->
<script xmlns="http://www.w3.org/1999/xhtml" type="text/javascript" src="js/kobo.js"/>

<body>
    <nav epub:type="toc">
    <h1>Table of Contents</h1>
        <ol>"""


middle = """
        </ol>
    </nav>

    <nav epub:type="landmarks">
        <h2>Guide</h2>
        <ol>
            <!--
            <li><a epub:type="ibooks:reader-start-page" href="xhtml/[VCOVER].xhtml">Open</a></li>
            <li><a epub:type="cover" href="xhtml/[VCOVER].xhtml">Cover</a></li>
            -->
            <li><a epub:type="bodymatter" href="xhtml/[BODYMATTER].xhtml">Start of Content</a></li>
        </ol>
    </nav>

    <nav epub:type="page-list">
        <ol>
            <li><a href="xhtml/[VCOVER].xhtml"></a></li>"""


bottom = """
        </ol>
    </nav>
</body>
</html>"""

nl = """
            """

toc = """<li><a href="xhtml/[CH###PG##].xhtml">[chapter_title]</a></li>"""

page_list_src = """<li><a href="xhtml/[CH###PG##].xhtml">[PAGE]</a></li>"""
