#!/usr/bin/env bash

# Fail early if an error occurs
set -Eeuo pipefail

usage() {
    cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") CATALOG_XML RESULT_PDF [ADDITIONAL_ARGS]

Transforms and formats an OSCAL XML Catalog into PDF using Saxon, FOP and XML Calabash invoked from Maven.
Please install Maven first.

Additional arguments should be specified in the `key=value` format.
EOF
}

if ! [ -x "$(command -v mvn)" ]; then
  echo 'Error: Maven (mvn) is not in the PATH, is it installed?' >&2
  exit 1
fi

[[ -z "${1-}" ]] && { echo "Error: CATALOG_XML not specified"; usage; exit 1; }
CATALOG_XML=$1
[[ -z "${2-}" ]] && { echo "Error: RESULT_PDF not specified"; usage; exit 1; }
RESULT_PDF=$2

ADDITIONAL_ARGS=$(shift 2; echo ${*// /\\ })

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
POM_FILE="${SCRIPT_DIR}/../pom.xml"

MAIN_CLASS="com.xmlcalabash.drivers.Main" # XML Calabash

PIPELINE="render-800-53-catalog.xpl"


if [ -e "$RESULT_PDF" ]
then 
    echo "Deleting prior $RESULT_PDF ..."
    rm -f ./$RESULT_PDF
fi

mvn \
    -f "$POM_FILE" \
    exec:java \
    -Dexec.mainClass="net.sf.saxon.Transform" \
    -Dexec.args="-xsl:tamus-required-controls-pdf.xsl -s:\"$CATALOG_XML\" -o:\"temp.xml\""

mvn \
    -f "$POM_FILE" \
    exec:java \
    -Dexec.mainClass="$MAIN_CLASS" \
    -Dcom.xmlcalabash.fo-processor="com.xmlcalabash.util.FoFOP" \
    -Dexec.args="-iOSCAL=\"temp.xml\" -oSOURCE=/dev/null -oHTML=/dev/null -oFO=/dev/null $ADDITIONAL_ARGS \"$PIPELINE\" result-pdf-path=\"$RESULT_PDF\""

rm temp.xml

if [ -e "$RESULT_PDF" ]
then 
    echo "Results can be viewed in $RESULT_PDF"
fi
