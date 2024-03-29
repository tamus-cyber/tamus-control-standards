#!/usr/bin/env bash

# Fail early if an error occurs
set -Eeuo pipefail

usage() {
    cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") CATALOG_XML RESULT_HTML [ADDITIONAL_ARGS]

Transforms and formats an OSCAL XML Catalog into PDF using Saxon invoked from Maven.
Please install Maven first.

Additional arguments are provided to XML Calabash
EOF
}

if ! [ -x "$(command -v mvn)" ]; then
  echo 'Error: Maven (mvn) is not in the PATH, is it installed?' >&2
  exit 1
fi

[[ -z "${1-}" ]] && { echo "Error: CATALOG_XML not specified"; usage; exit 1; }
CATALOG_XML=$1
[[ -z "${2-}" ]] && { echo "Error: RESULT_HTML not specified"; usage; exit 1; }
RESULT_HTML=$2

ADDITIONAL_ARGS=$(shift 2; echo ${*// /\\ })

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
POM_FILE="${SCRIPT_DIR}/../pom.xml"

MAIN_CLASS="net.sf.saxon.Transform" # Saxon defined in pom.xml

if [ -e "$RESULT_HTML" ]
then 
    echo "Deleting prior $RESULT_HTML ..."
    rm -f ./$RESULT_HTML
fi

mvn \
    -f "$POM_FILE" \
    exec:java \
    -Dexec.mainClass="$MAIN_CLASS" \
    -Dexec.args="-xsl:tamus-required-controls-html.xsl -s:\"$CATALOG_XML\" -o:\"$RESULT_HTML\" $ADDITIONAL_ARGS"

if [ -e "$RESULT_HTML" ]
then 
    echo "Results can be viewed in $RESULT_HTML"
fi
