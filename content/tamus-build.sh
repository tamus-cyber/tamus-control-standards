#!/usr/bin/env bash

# Fail early if an error occurs
set -Eeuo pipefail

usage() {
    cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}")

Transforms OSCAL XML profiles into an OSCAL XML catalog using Saxon invoked from Maven.
Please install Maven first.
EOF
}

if ! [ -x "$(command -v mvn)" ]; then
  echo 'Error: Maven (mvn) is not in the PATH, is it installed?' >&2
  exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
POM_FILE="${SCRIPT_DIR}/../../oscal-xslt/pom.xml"

MAIN_CLASS="net.sf.saxon.Transform" # Saxon defined in pom.xml

# Resolve XML profiles to catalogs
mvn -f $POM_FILE \
	exec:java -Dexec.mainClass="$MAIN_CLASS" \
	-Dexec.args="-t -s:texas.gov/TX_DIR_profile.xml \
-xsl:../../OSCAL/src/utils/util/resolver-pipeline/oscal-profile-RESOLVE.xsl \
-o:texas.gov/TX_DIR_resolved-profile_catalog.xml"

mvn -f $POM_FILE \
	exec:java -Dexec.mainClass="$MAIN_CLASS" \
	-Dexec.args="-t -s:tamus.edu/TAMUS_profile.xml \
-xsl:../../OSCAL/src/utils/util/resolver-pipeline/oscal-profile-RESOLVE.xsl \
-o:tamus.edu/TAMUS_resolved-profile_catalog.xml"
