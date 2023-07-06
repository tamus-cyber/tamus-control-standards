<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="3.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:o="http://csrc.nist.gov/ns/oscal/1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    xpath-default-namespace="http://csrc.nist.gov/ns/oscal/1.0"
    exclude-result-prefixes="#all">

<xsl:template match="/">
  <table>
    <tr>
      <th>Control</th>
      <th>Texas DIR Required By</th>
      <th>TAMUS Required By</th>
    </tr>
    <xsl:for-each select="catalog/group">
      <tr>
        <td>
          <h2><xsl:value-of select="@id"/> - <xsl:value-of select="title"/></h2>
        </td>
      </tr>
      <xsl:for-each select="control">
        <xsl:if test="prop[@name='tx_required_by'] or prop[@name='tamus_required_by']">
          <tr>
            <td>
              <xsl:value-of select="prop[@name='label'][1]/@value"/> - <xsl:value-of select="title"/>
            </td>
            <td>
              <xsl:value-of select="prop[@name='tx_required_by']/@value"/>
            </td>
            <td>
              <xsl:value-of select="prop[@name='tamus_required_by']/@value"/>
            </td>
          </tr>
        </xsl:if>
      </xsl:for-each>
    </xsl:for-each>
  </table>
</xsl:template>

</xsl:stylesheet>