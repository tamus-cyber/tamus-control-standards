<?xml version="1.0" encoding="utf-8"?>
 <xsl:stylesheet version="1.0" xpath-default-namespace="http://csrc.nist.gov/ns/oscal/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml" indent="yes"/>
  
  <xsl:template match="/ | @* | node()">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="control[not(prop[@name='tx_required_by'] or prop[@name='tamus_required_by'])]"/>

</xsl:stylesheet>