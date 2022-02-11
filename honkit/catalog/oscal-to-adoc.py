import io
import re
import xml.etree.ElementTree as ET

parser = ET.XMLParser(encoding="ascii")
tree = ET.parse('TAMUS_resolved-profile_catalog.xml', parser=parser)
root = tree.getroot()

# Take a link element, format into an ASCIIdoc cross-reference, and output
def transformInsideLinks(links):
    linksList = []
    for link in links:
        str = ""

        label = re.sub("(.*)_smt\.(.*)", "\\1(\\2)", link)
        label = re.sub(link[1:3], link[1:3].upper(), label)
        href = re.sub("(.*)_smt\.(.*)", "\\1", link)

        str = ("xref:%s.adoc%s[%s]") % (href[1:3], transformParam(href), label[1:])

        linksList.append(str)

    return ", ".join(linksList)

# Take a link element, retrieve the href from the resources dictionary, format into ASCIIdoc, and output
def transformReferences(links):
    linksList = []
    for link in links:
        str = ""
        resource = resources[re.sub("#", "", link)]
        title = resource.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text
        href = resource.find('{http://csrc.nist.gov/ns/oscal/1.0}rlink').get('href')

        str = ("%s[%s]") % (href, title)

        linksList.append(str)

    return ", ".join(linksList)

# Replace . in a string with - ; intended for custom attributes and <a> id tags
def transformParam(param):
    str = re.sub("\.", "-", param)

    return str

# Custom function for printPart() to format the output of an cross-reference link
def printPartFormatXref(x):
    if (x.group(3)):
        return ("xref:%s.adoc#%s-%s-%s[%s-%s(%s)]" % (x.group(1), x.group(1), x.group(2), x.group(3), x.group(1).upper(), x.group(2).upper(), x.group(3)))
    else:
        return ("xref:%s.adoc#%s-%s[%s-%s]" % (x.group(1), x.group(1), x.group(2), x.group(1).upper(), x.group(2).upper()))

# Each part of a control statement iterates through this function
def printPart(parts, links, props):
    string = "" # Initialize the string to be returned

    # Re-iterate prop elements
    part_props = {}
    for part_prop in parts.findall('{http://csrc.nist.gov/ns/oscal/1.0}prop'):
        if (part_prop.get('class') != "sp800-53a"):
            part_props[part_prop.get('name')] = part_prop.get('value')

    # If the element is changed, add the Changed role tag
    if ('tx_changed' in part_props or 'tamus_changed' in part_props):
        string += "[.Changed]\n"

    # Iterate the part elements and format/output
    for part in parts:

        if (part.tag == "{http://csrc.nist.gov/ns/oscal/1.0}p"):
            str = re.sub("{#([a-z]{2})-(\d{1,2})-?([a-z0-9]*)}", printPartFormatXref, part.text.lstrip())
            string += str + "\n"

        # If the element is an item part, output the label and re-iterate child elements
        for item_prop in part.findall('{http://csrc.nist.gov/ns/oscal/1.0}prop'):
            if (item_prop.get('name') == "label"):
                string += item_prop.get('value') + " "

            if (part.findall('{http://csrc.nist.gov/ns/oscal/1.0}part') is not None):
                string += printPart(part, links, props)

    return string

# Each catalog item (family, control or enhancement) iterates through this function
def printCatalogItem(element):
    string = "" # Initialize the string to be returned

    title = element.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text   # Catalog item's title

    # If the catalog item is the control family, only output the title and return
    if (element.get('class') == "family"):
        string += ("= %s\n" % (title))

    # If the catalog item is a control or enhancement, follow this logic
    if (element.get('class') == "SP800-53" or element.get('class') == "SP800-53-enhancement"):
        # Control headers start at level 2
        if (element.get('class') == "SP800-53"):
            indent = 2

        # Enhancement headers start at level 4
        if (element.get('class') == "SP800-53-enhancement"):
            indent = 4

        # Iterate the link elements and set links as a dictionary
        links = {}
        for link in element.findall('{http://csrc.nist.gov/ns/oscal/1.0}link'):
            if (link.get('rel') not in links):
                links[link.get('rel')] = []
            links[link.get('rel')].append(link.get('href'))

        # Iterate the part elements and set parts as a dictionary
        parts = {}
        for part in element.findall('{http://csrc.nist.gov/ns/oscal/1.0}part'):
            parts[part.get('name')] = part

        # Iterate the prop elements and set props as a dictionary
        props = {}
        for prop in element.findall('{http://csrc.nist.gov/ns/oscal/1.0}prop'):
            if (prop.get('class') != "sp800-53a"):
                props[prop.get('name')] = prop.get('value')

        # Output the ASCIIdoc for the title
        string += ("%s %s %s[[%s]]\n" % ("="*indent, props['label'], title, \
            transformParam(element.get('id'))))

        # Add change bar (if set)
        if ('tx_changed' in props or 'tamus_changed' in props or 'tx_new_requirement' in props or 'tamus_new_requirement' in props):
            string += "[.Changed]\n"

        # Output the Texas baseline (if exists)
        if (props.get('tx_baseline')):
            string += ("Texas DIR Baseline:: %s\n" % (props.get('tx_baseline')))

        # Output the TAMUS baseline (if exists)
        if (props.get('tamus_baseline')):
            string += ("TAMUS Baseline:: %s\n" % (props.get('tamus_baseline')))

        # Output the NIST baseline (if exists)
        if (props.get('tx_privacy_baseline') or props.get('tamus_privacy_baseline')):
            string += ("Privacy Baseline:: Yes\n")

        # Output the TxDIR Required By date (if exists)
        if (props.get('tx_required_by')):
            string += ("TxDIR Required By:: %s\n" % (props.get('tx_required_by')))

        # Output the TAMUS Required By date (if exists)
        if (props.get('tamus_required_by')):
            string += ("TAMUS Required By:: %s\n" % (props.get('tamus_required_by')))

        # Output the control status (used for inactive controls)
        if (props.get('status')):
            string += ("%s: " % (props.get('status').capitalize()))

        # Output the Incorporated Into link (used for inactive controls)
        if ('incorporated-into' in links):
            string += ("Incorporated into %s\n" % (transformInsideLinks(links['incorporated-into'])))

        # Output the Moved To link (used for inactive controls)
        if ('moved-to' in links):
            string += ("Moved to %s\n" % (transformInsideLinks(links['moved-to'])))

        # Output the control statement
        if ('statement' in parts):
            string += ("\n%s= Control\n" % ("="*indent))
            string += printPart(parts['statement'], links, props)

        # Output the Texas control implementation statement
        if ('tx_implementation' in parts):
            string += ("\n%s= State Implementation Details\n" % ("="*indent))
            # If the control is changed/new, add the Changed role tag
            if ('tx_changed' in props or 'tx_new_requirement' in props):
                string += "[.Changed]\n"
            string += printPart(parts['tx_implementation'], links, props)

        # Output the TAMUS control implementation statement
        if ('tamus_implementation' in parts):
            string += ("\n%s= TAMUS Implementation Details\n" % ("="*indent))
            # If the control is changed/new, add the Changed role tag
            if ('tamus_changed' in props or 'tamus_new_requirement' in props):
                string += "[.Changed]\n"
            string += printPart(parts['tamus_implementation'], links, props)

        # Output the supplemental guidance
        if ('guidance' in parts):
            string += ("\n%s= Discussion\n" % ("="*indent))
            string += printPart(parts['guidance'], links, props)

        # Output the related controls links
        if ('related' in links):
            string += ("\n%s= Related Controls\n" % ("="*indent))
            string += transformInsideLinks(links['related'])
            string += "\n"

        # Output the reference links
        if ('reference' in links):
            string += ("\n%s= References\n" % ("="*indent))
            string += transformReferences(links['reference'])

    return string

############################################################
### Start the script here
############################################################

### This section creates the family ASCIIdoc files

resources = {}  # Initialize resources dictionary

# Iterate the back-matter section of the XML and set resources as a dictionary
for back_matter in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}back-matter'):
    for resource in back_matter.findall('{http://csrc.nist.gov/ns/oscal/1.0}resource'):
        uuid = resource.get('uuid')
        resources[uuid] = resource

# Iterate the group sections of the XML and generate one ASCIIdoc page per control family
for family in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}group'):
    if (family.get('class') == "family"):
        params = {} # Initialize params dictionary
        family_file = open(family.get('id') + ".adoc", "w") # Create new ASCIIdoc page
        family_file.write(printCatalogItem(family) + "") # Output page title
        family_file.write(":toc:\n:toclevels: 1\n") # Output page table of contents

        # Iterate the family elements and set params as a dictionary
        for param in family.iter('{http://csrc.nist.gov/ns/oscal/1.0}param'):
            param_id = transformParam(param.get('id'))
            assignment_tag = ""

            # If the param is a label, just grab the text of the label
            if (param.findall('{http://csrc.nist.gov/ns/oscal/1.0}label')):
                assignment_tag = "Assignment"
                params[param_id] = ("%s: %s" % (assignment_tag, param.find('{http://csrc.nist.gov/ns/oscal/1.0}label').text))

            # If the param is a choice, determine if it's a any/one-or-more and grab the choices
            if (param.findall('{http://csrc.nist.gov/ns/oscal/1.0}select')):
                assignment_tag = "Selection"
                if (param.find('{http://csrc.nist.gov/ns/oscal/1.0}select').get('how-many') is not None):
                    assignment_tag += " (" + param.find('{http://csrc.nist.gov/ns/oscal/1.0}select').get('how-many') + ")"
                    assignment_tag = assignment_tag.replace("-", " ")

                choices = []
                for choice in param.iter('{http://csrc.nist.gov/ns/oscal/1.0}choice'):
                    choices.append(choice.text.strip().replace("\n", ""))

                params[param_id] = "%s: %s" % (assignment_tag, "; ".join(choices))

        # Iterate the params dictionary and output as ASCIIdoc custom attributes
        for key, value in params.items():
            param_row = ":%s: %s\n" % (key, value)
            param_row = param_row.format(**params)
            family_file.write(param_row)

        family_file.write("\n")

        # Iterate the control elements and output as ASCIIdoc
        for control in family.findall('{http://csrc.nist.gov/ns/oscal/1.0}control'):
            family_file.write(printCatalogItem(control) + "\n\n")
            if (control.findall('{http://csrc.nist.gov/ns/oscal/1.0}control')):
                family_file.write("=== Control Enhancements\n")
                for enhancement in control.findall('{http://csrc.nist.gov/ns/oscal/1.0}control'):
                    family_file.write(printCatalogItem(enhancement) + "\n")

        family_file.close() # Close the ASCIIdoc page


### This section creates the required controls ASCIIdoc files

# Create required controls index page
required_controls_file = open("required-controls.adoc", "w") # Create new ASCIIdoc page

string = "= Texas DIR and Texas A&M System Required Controls\n\n"

string += "[cols=\"15%,45%,20%,20%\"]\n"
string += "|===\n"
string += "|Control ID |Title |TxDIR Required By |TAMUS Required By\n\n"

# Iterate the control families, find ones with a required date, and output as ASCIIdoc
for family in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}group'):
    title = family.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text   # Control family title
    string += ("4+h|%s\n" % (title))

    i = 0

    for control in family.iter('{http://csrc.nist.gov/ns/oscal/1.0}control'):
        props = {}
        for prop in control.findall('{http://csrc.nist.gov/ns/oscal/1.0}prop'):
            if (prop.get('class') != "sp800-53a"):
                props[prop.get('name')] = prop.get('value')

        if ('tx_required_by' in props or 'tamus_required_by' in props):
            i += 1
            title = control.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text   # Catalog item's title
            family = control.get('id')[0:2]

            string += ("|xref:%s.adoc#%s[%s] " % (family, transformParam(control.get('id')), props['label']))
            string += ("|%s " % (title))
            if ('tx_required_by' in props):
                string += ("|%s " % (props['tx_required_by'] or ""))
            else:
                string += "| "
            if ('tamus_required_by' in props):
                string += ("|%s " % (props['tamus_required_by'] or ""))
            else:
                string += "| "
            string += "\n"

    if (i == 0):
        string += "4+|_No required controls in this family_\n"

string += "|===\n"

required_controls_file.write(string)
required_controls_file.close()

# Create new controls index page
new_controls_file = open("new-controls.adoc", "w") # Create new ASCIIdoc page

string = "= Texas DIR and Texas A&M System New Required Controls\n\n"

string += "[cols=\"15%,45%,20%,20%\"]\n"
string += "|===\n"
string += "|Control ID |Title |TxDIR Required By |TAMUS Required By\n\n"

# Iterate the control families, find ones with a new required control, and output as ASCIIdoc
for family in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}group'):
    title = family.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text   # Control family title
    string += ("4+h|%s\n" % (title))

    i = 0

    for control in family.iter('{http://csrc.nist.gov/ns/oscal/1.0}control'):
        props = {}
        for prop in control.findall('{http://csrc.nist.gov/ns/oscal/1.0}prop'):
            if (prop.get('class') != "sp800-53a"):
                props[prop.get('name')] = prop.get('value')

        if ('tx_new_requirement' in props or 'tamus_new_requirement' in props):
            i += 1
            title = control.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text   # Catalog item's title
            family = control.get('id')[0:2]

            string += ("|xref:%s.adoc#%s[%s] " % (family, transformParam(control.get('id')), props['label']))
            string += ("|%s " % (title))
            if ('tx_required_by' in props):
                string += ("|%s " % (props['tx_required_by'] or ""))
            else:
                string += "| "
            if ('tamus_required_by' in props):
                string += ("|%s " % (props['tamus_required_by'] or ""))
            else:
                string += "| "
            string += "\n"

    if (i == 0):
        string += "4+|_No new required controls in this family_\n"

string += "|===\n"

new_controls_file.write(string)
new_controls_file.close()

# Create index page
index_file = open("README.adoc", "w") # Create new ASCIIdoc page

string = "= Control Standards Catalog\n:table-caption!:\n\n"

string += "Security and privacy control standards described in this control standards catalog have a well-defined organization and structure. For ease of use in the security and privacy control selection and specification process, controls are organized into families (listed below and in the navigation menu to the left). Each family contains controls that are related to the specific topic of the family. A two-character identifier uniquely identifies each control family (e.g., PS for Personnel Security). Security and privacy controls may involve aspects of policy, oversight, supervision, manual processes, and automated mechanisms that are implemented by systems or actions by individuals.\n\n"

string += ".Control Families\n[cols=\"1,1\"]\n|===\n"

for family in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}group'):
    title = family.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text   # Control family title
    string += ("|xref:%s.adoc[%s - %s]\n" % (family.get('id'), family.get('id').upper(), title))

string += "|==="

index_file.write(string)
index_file.close()
