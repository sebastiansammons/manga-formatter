# template_kobo_toc_ncx.py
top = '''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" xml:lang="en" version="2005-1">
<head>
    <meta name="dtb:uid" content="[TITLE]"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle><text>[TITLE]</text></docTitle>
<docAuthor><text>[CREATOR]</text></docAuthor>
<navMap>'''

bottom = '''
</navMap>
</ncx>'''

nl = '''
    '''

nav_point = '''<navPoint class="other" id="ch[COUNT]" playOrder="[COUNT]"><navLabel><text>[chapter_title]</text></navLabel><content src="xhtml/[CH###PG##].xhtml"/></navPoint>'''