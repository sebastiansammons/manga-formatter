# template_xhtml_page.py
top = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xml="http://www.w3.org/XML/1998/namespace" xmlns:ibooks="http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0" epub:prefix="ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0">
<head>
    <meta charset="UTF-8"/>
    <title>[CH###PG##]</title>
    <link rel="stylesheet" href="../css/stylesheet.css" type="text/css"/>
    <meta name="viewport" content="width=[WIDTH], height=[HEIGHT]"/>
</head>

<body>
    <div>
    """
bottom = """
    </div>
</body>
</html>"""

xhtml_pages = """<img class="[spread]" src="../images/[CH###PG##][ext]" alt="[CH###PG##]"/>"""
