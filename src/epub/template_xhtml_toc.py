top = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"  xmlns:xml="http://www.w3.org/XML/1998/namespace" xmlns:ibooks="http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0" epub:prefix="ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0">
<head>
    <title>Table of Contents</title>
</head>

<body>
    <nav epub:type="toc">
        <!-- <h1>TOC</h1> h1 needed? -->
        <ol>"""
            

middle = """
        </ol>
    </nav>

    <nav epub:type="landmarks">
        <!-- <h1>Guide</h1> h1 needed? -->
        <ol>
            <li><a epub:type="ibooks:reader-start-page" href="xhtml/[VCOVER].xhtml">Open</a></li>
            <li><a epub:type="cover" href="xhtml/[VCOVER].xhtml">Cover</a></li>
            <li><a epub:type="bodymatter" href="xhtml/[BODYMATTER].xhtml">Bodymatter</a></li>
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
