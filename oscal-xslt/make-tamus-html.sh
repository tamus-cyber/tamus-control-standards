#!/usr/bin/env bash

# Fail early if an error occurs
set -Eeuo pipefail

usage() {
    cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}")

Generates TAMUS web pages from OSCAL XML catalogs.
EOF
}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

# Generate 800-53 Catalog

sh mvn-make-800-53-catalog-html.sh ../../tamus-control-standards/content/tamus.edu/TAMUS_resolved-profile_catalog.xml temp css-path=/dev/null

{ echo '---\nlayout: catalog\ntitle: Cybersecurity Control Standards Catalog\ncustom-css: catalog.css\n---\n'; cat temp; } > catalog.html

rm temp

mv catalog.html ../../tamus-control-standards/docs/catalog/index.html

# Generate required controls listing

sh mvn-make-required-controls-html.sh ../../tamus-control-standards/content/tamus.edu/TAMUS_resolved-profile_catalog.xml temp css-path=/dev/null

{ echo '---\nlayout: full-width\ntitle: Required Control Standards Listing\ncustom-css: required-controls.css\n---\n'; cat temp; } > required-controls.html

rm temp

mv required-controls.html ../../tamus-control-standards/docs/catalog
