import io
import re
import xml.etree.ElementTree as ET

parser = ET.XMLParser(encoding="ascii")
tree = ET.parse('TAMUS_2.0_resolved-profile_catalog.xml', parser=parser)
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

# Each part of a control statement iterates through this function
def printPart(parts, links, props):
    string = "" # Initialize the string to be returned

    # Iterate the part elements and format/output
    for part in parts:
        # If the element is the last child, output the contents of the p tag
        if (part.tag == "{http://csrc.nist.gov/ns/oscal/1.0}p"):
            string += part.text.lstrip() + "\n"

        # If the element is an item part, output the label and re-iterate child elements
        if (part.get('name') == "item"):
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
            props[prop.get('name')] = prop.get('value')

        # Output the ASCIIdoc for the title
        string += ("%s %s %s[[%s]]\n" % ("="*indent, props['label'], title, \
            transformParam(element.get('id'))))

        # Output the NIST baseline (if exists)
        if (props.get('baseline')):
            string += ("NIST Baseline:: %s\n" % (props.get('baseline')))

        # Output the Required By date (if exists)
        if (props.get('required_by')):
            string += ("Required By:: %s\n" % (props.get('required_by')))

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
            string += printPart(parts['tx_implementation'], links, props)

        # Output the TAMUS control implementation statement
        if ('tamus_implementation' in parts):
            string += ("\n%s= TAMUS Implementation Details\n" % ("="*indent))
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

# Created required controls index page
required_controls_file = open("required-controls.adoc", "w") # Create new ASCIIdoc page

string = "# Texas DIR and Texas A&M System Required Controls\n\n"

string += "[cols=\"15%,60%,25%\"]\n"
string += "|===\n"
string += "|Control ID |Title |Required By\n\n"

# Iterate the control families, find ones with a required date, and output as ASCIIdoc
for family in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}group'):
    title = family.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text   # Control family title
    string += ("3+h|%s\n" % (title))

    i = 0

    for control in family.iter('{http://csrc.nist.gov/ns/oscal/1.0}control'):
        props = {}
        for prop in control.findall('{http://csrc.nist.gov/ns/oscal/1.0}prop'):
            props[prop.get('name')] = prop.get('value')

        if ('required_by' in props):
            i += 1
            title = control.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text   # Catalog item's title
            family = control.get('id')[0:2]

            string += ("|xref:%s.adoc#%s[%s] " % (family, control.get('id'), props['label']))
            string += ("|%s " % (title))
            string += ("|%s " % (props['required_by']))
            string += "\n"

    if (i == 0):
        string += "3+|_No required controls in this family_\n"

string += "|===\n"

required_controls_file.write(string)
required_controls_file.close()
