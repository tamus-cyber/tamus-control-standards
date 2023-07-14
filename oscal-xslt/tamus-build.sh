#!/usr/bin/env bash

# Fail early if an error occurs
set -Eeuo pipefail

usage() {
    cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}")

Patches oscal-xslt files for TAMUS customization.
EOF
}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

cp publish/mvn-make-catalog-html.sh publish/mvn-make-800-53-catalog-html.sh
cp publish/mvn-make-catalog-pdf.sh publish/mvn-make-800-53-catalog-pdf.sh
cp publish/render-oscal-catalog.xpl publish/render-800-53-catalog.xpl

patch -i $SCRIPT_DIR/oscal-xslt.patch

cp publish/nist-emulation/sp800-53A-catalog_html.xsl publish/nist-emulation/sp800-53-catalog_html.xsl

patch -i $SCRIPT_DIR/sp800-53-catalog_html.xsl.patch

cp $SCRIPT_DIR/make-tamus-html.sh publish
cp $SCRIPT_DIR/mvn-make-required-controls-html.sh publish
cp $SCRIPT_DIR/tamus-required-controls-html.xsl publish
cp $SCRIPT_DIR/tamus-required-controls-pdf.xsl publish