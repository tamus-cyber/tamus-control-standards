import re
import xml.etree.ElementTree as ET

tree = ET.parse('TAMUS_2.0_resolved-profile_catalog.xml')
root = tree.getroot()

for family in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}group'):
	if (family.get('class') == "family"):
		id = family.get('id')
		label = family.get('id').upper()
		title = family.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text

		print ("** link:catalog/%s.adoc[%s - %s]" % (id, label, title))
