#!/usr/bin/env bash

# Fail early if an error occurs
set -Eeuo pipefail

Help()
{
	echo "Build the DIR and TAMUS OSCAL catalogs using OSCAL profiles"
	echo
	echo "Syntax: build-tamus-catalogs [Path to POM] [Path to OSCAL library] [Path to OSCAL content]"
	echo
}

if ! [ -x "$(command -v mvn)" ]; then
  echo 'Error: Maven (mvn) is not in the PATH, is it installed?' >&2
  exit 1
fi

MAIN_CLASS="net.sf.saxon.Transform" # Saxon defined in pom.xml

# Resolve XML profiles to catalogs
mvn -f $1/pom.xml \
	exec:java -Dexec.mainClass="net.sf.saxon.Transform" \
	-Dexec.args="-t -s:$3/texas.gov/TX_DIR_profile.xml \
-xsl:$2/src/utils/resolver-pipeline/oscal-profile-RESOLVE.xsl \
-o:$3/texas.gov/TX_DIR_resolved-profile_catalog.xml"

mvn -f $1/pom.xml \
	exec:java -Dexec.mainClass="net.sf.saxon.Transform" \
	-Dexec.args="-t -s:$3/tamus.edu/TAMUS_profile.xml \
-xsl:$2/src/utils/resolver-pipeline/oscal-profile-RESOLVE.xsl \
-o:$3/tamus.edu/TAMUS_resolved-profile_catalog.xml"
