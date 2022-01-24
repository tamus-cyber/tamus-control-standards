rm TAMUS_2.0_resolved-profile_catalog.xml
cp ../../content/tamus.edu/xml/TAMUS_2.0_resolved-profile_catalog.xml ./catalog.tmp
sed -i '' 's/<insert type="param" id-ref="\([a-z0-9._-]*\)"\/>/_[{\1}]_/g' catalog.tmp
sed -i '' 's/{\([a-z0-9_-]*\)\.\([a-z0-9_-]*\)}/{\1-\2}/g' catalog.tmp
iconv -f utf8 -t ascii//translit catalog.tmp > TAMUS_2.0_resolved-profile_catalog.xml
rm catalog.tmp
python3 oscal-to-adoc.py
rm TAMUS_2.0_resolved-profile_catalog.xml
