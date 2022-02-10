#!/bin/sh

echo "Purging old docs directory..."

rm -rf ../docs

echo "Copying OSCAL catalog from source..."

cd catalog
rm TAMUS_resolved-profile_catalog.xml
cp ../../content/tamus.edu/TAMUS_resolved-profile_catalog.xml ./catalog.tmp

echo "Formatting OSCAL catalog for ASCIIdoc..."

sed -i '' 's/<insert type="param" id-ref="\([a-z0-9._-]*\)"\/>/_[{\1}]_/g' catalog.tmp
sed -i '' 's/<a href="\(#[a-z0-9._-]*\)">[A-Z0-9\(\)_-]*<\/a>/{\1}/g' catalog.tmp
sed -i '' 's/{\([a-z0-9#_-]*\)\.\([a-z0-9_-]*\)\.\([a-z0-9_-]*\)}/{\1-\2-\3}/g' catalog.tmp
sed -i '' 's/{\([a-z0-9#_-]*\)\.\([a-z0-9_-]*\)}/{\1-\2}/g' catalog.tmp
iconv -f utf8 -t ascii//translit catalog.tmp > TAMUS_resolved-profile_catalog.xml
rm catalog.tmp

echo "Generating ASCIIdoc pages from OSCAL catalog..."

python3 oscal-to-adoc.py
rm TAMUS_resolved-profile_catalog.xml

echo "Building HonKit site..."

cd ..
honkit build

echo "Moving _book directory to docs..."

mv _book ../docs

echo "Cleaning up catalog ASCIIdoc files..."

rm catalog/*.adoc

echo "New build complete, ready to push to GitHub..."
