<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="3.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:o="http://csrc.nist.gov/ns/oscal/1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    xpath-default-namespace="http://csrc.nist.gov/ns/oscal/1.0"
    exclude-result-prefixes="#all">

  <xsl:template name="control">
    <xsl:variable name="controlId" select="@id"/>

    <xsl:variable name="controlClass">
      <xsl:choose>
        <xsl:when test="@class eq 'SP800-53-enhancement'">
          <xsl:text>enhancement</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>control</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:variable name="txNewRequirementClass">
      <xsl:if test="prop[@name='tx_new_requirement']/@value eq 'true'">
        <xsl:text>new-requirement</xsl:text>
      </xsl:if>
    </xsl:variable>

    <xsl:variable name="tamusNewRequirementClass">
      <xsl:if test="prop[@name='tamus_new_requirement']/@value eq 'true'">
        <xsl:text>new-requirement</xsl:text>
      </xsl:if>
    </xsl:variable>

    <tr>
      <td class="{ $controlClass }">
        <a class="control-title" href="/catalog#{ $controlId }">
          <xsl:value-of select="prop[@name='label'][1]/@value"/><xsl:text> </xsl:text><xsl:value-of select="title"/>
        </a>
      </td>
      <td class="required-date { $txNewRequirementClass }">
        <xsl:value-of select="prop[@name='tx_required_by']/@value"/>
      </td>
      <td class="required-date { $tamusNewRequirementClass }">
        <xsl:value-of select="prop[@name='tamus_required_by']/@value"/>
      </td>
      <td class="implementation-level">
        <xsl:for-each select="prop[@name='implementation-level']">
          <xsl:value-of select="concat(upper-case(substring(@value,1,1)),' ')"/>
        </xsl:for-each>
      </td>
      <td class="implementation-level">
        <xsl:value-of select="substring(prop[@name='ot-baseline']/@value,1,1)"/>
      </td>
    </tr>
  </xsl:template>

  <xsl:template match="/">
    <table class="required-controls">
      <tr>
        <th>Control</th>
        <th class="required-date">Texas DIR Required By</th>
        <th class="required-date">TAMUS Required By</th>
        <th class="implementation-level">Org/System Control</th>
        <th class="implementation-level">OT Baseline</th>
      </tr>
      <xsl:for-each select="catalog/group">
        <xsl:variable name="familyId" select="@id"/>

        <tr id="{ $familyId }">
          <td colspan="3">
            <h4><xsl:value-of select="title"/> (<xsl:value-of select="upper-case(@id)"/>)</h4>
          </td>
        </tr>
        <xsl:for-each select="control">
          <xsl:call-template name="control"/>
          <xsl:for-each select="control">
            <xsl:call-template name="control"/>
          </xsl:for-each>
        </xsl:for-each>
      </xsl:for-each>
    </table>
  </xsl:template>

</xsl:stylesheet>