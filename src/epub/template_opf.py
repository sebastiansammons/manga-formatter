top = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="ImTheFridgeID" prefix="rendition: http://www.idpf.org/vocab/rendition/# ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0/">
<metadata xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">
      <dc:identifier id="ImTheFridge_ID">urn:uuid:[UUID]</dc:identifier>
      <dc:title>[TITLE]</dc:title>
      <dc:creator id="author">[CREATOR]</dc:creator>
      <dc:language>en</dc:language>
      <dc:contributor id="ImTheFridge">ImTheFridge</dc:contributor>
      <meta property="dcterms:modified">[DATETIME]</meta>
      <!-- Apple Books stuff -->
      <meta property="ibooks:version">3.2</meta>
      <!-- <meta property="ibooks:version">1.1.2</meta> -->
      <meta property="rendition:layout">pre-paginated</meta>
      <meta property="rendition:spread">landscape</meta>
      <meta property="rendition:orientation">auto</meta>
</metadata>

<manifest>
      <!-- toc xhtml -->
      <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>

      <!-- css stylesheet -->
      <item id="css_stylesheet" href="css/stylesheet.css" media-type="text/css"/>

      <!-- xhtml pages -->"""

mid_a = """

      <!-- image files -->"""

mid_b = """
</manifest>

<spine page-progression-direction="rtl">"""

bottom = """
</spine>
</package>"""

nl = """
      """

manifest_cover = """<item id="[CH###PG##]_img" href="images/[img_filename]" media-type="image/[img_ext]" properties="cover-image"/>"""

manifest_image = """<item id="[CH###PG##]_img" href="images/[img_filename]" media-type="image/[img_ext]"/>"""

manifest_xhtml = """<item id="[CH###PG##]" href="xhtml/[CH###PG##].xhtml" media-type="application/xhtml+xml"/>"""

spine = """<itemref idref="[CH###PG##]" linear="yes" properties="rendition:page-spread-[spread]"/>"""
