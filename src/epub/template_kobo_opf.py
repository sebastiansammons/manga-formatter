# template_opf.py
top = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="ImTheFridgeID" prefix="rendition: http://www.idpf.org/vocab/rendition/# ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0/" xml:lang="en" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"  >
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
      <dc:title>[TITLE]</dc:title>
      <dc:language>en</dc:language>
      <dc:identifier id="ImTheFridge_ID">[UUID]</dc:identifier>
      <dc:creator id="author">[CREATOR]</dc:creator>
      <dc:publisher>ImTheFridge</dc:publisher>
      <meta property="ibooks:binding">false</meta>
      <meta property="dcterms:modified">[DATETIME]</meta>
      <meta property="rendition:layout">pre-paginated</meta>
      <meta property="rendition:orientation">auto</meta>
      <meta property="rendition:spread">auto</meta>
</metadata>

<manifest>
      <!-- ncx -->
      <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>

      <!-- toc xhtml -->
      <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>

      <!-- css stylesheet -->
      <item id="css_stylesheet" href="css/stylesheet.css" media-type="text/css"/>

      <!-- javascript -->
      <item id="js-kobo.js" href="js/kobo.js" media-type="application/javascript"/>

      <!-- xhtml pages -->"""

mid_a = """

      <!-- image files -->"""

mid_b = """
</manifest>

<spine page-progression-direction="rtl" toc="ncx">"""

bottom = """
</spine>
</package>"""

nl = """
      """

manifest_image = """<item id="[CH###PG##]_img" href="images/[img_filename]" media-type="image/[img_ext]"/>"""

manifest_xhtml = """<item id="[CH###PG##]" href="xhtml/[CH###PG##].xhtml" media-type="application/xhtml+xml"/>"""

spine_cover = """<itemref idref="[CH###PG##]"/>"""

spine = """<itemref idref="[CH###PG##]" properties="page-spread-[spread]"/>"""


