#!/usr/bin/env bash

# Fail early if an error occurs
set -Eeuo pipefail

cp ../tamus-control-standards/oscal-xslt/publish/make-tamus-html.sh publish
cp ../tamus-control-standards/oscal-xslt/publish/mvn-make-required-controls-html.sh publish
cp ../tamus-control-standards/oscal-xslt/publish/tamus-required-controls-html.xsl publish

patch publish/nist-emulation/sp800-53A-catalog_html.xsl ../tamus-control-standards/oscal-xslt/publish/nist-emulation/sp800-53A-catalog_html.xsl.patch
patch publish/generic-preview/oscal_catalog_html.xsl ../tamus-control-standards/oscal-xslt/publish/generic-preview/oscal_catalog_html.xsl.patch
patch publish/generic-preview/oscal_metadata_html.xsl ../tamus-control-standards/oscal-xslt/publish/generic-preview/oscal_metadata_html.xsl.patch
