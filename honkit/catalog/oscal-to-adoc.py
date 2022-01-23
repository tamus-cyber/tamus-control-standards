import io
import re
import xml.etree.ElementTree as ET

parser = ET.XMLParser(encoding="ascii")
tree = ET.parse('TAMUS_2.0_resolved-profile_catalog.xml', parser=parser)
root = tree.getroot()

def transformInsideLink(links):
    linksList = []
    for link in links:
        str = ""
        href = link

        str = ("xref:%s.adoc%s[%s]") % (href[1:3], transformParam(href), href[1:].upper())

        linksList.append(str)

    return ", ".join(linksList)

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

def transformParam(param):
    str = re.sub("\.", "-", param)

    return str

def printPart(parts, params, links, props):
    string = ""

    for part in parts:
        if (part.tag == "{http://csrc.nist.gov/ns/oscal/1.0}p"):
            string = string + part.text.lstrip() + "\n"

        if (part.get('name') == "item"):
#            item_p = part.find('{http://csrc.nist.gov/ns/oscal/1.0}p')

            for item_prop in part.findall('{http://csrc.nist.gov/ns/oscal/1.0}prop'):
                if (item_prop.get('name') == "label"):
                    string = string + item_prop.get('value') + " "

#            if (item_p is not None):
#                string = string + item_p.text.lstrip() + "\n"

            if (part.findall('{http://csrc.nist.gov/ns/oscal/1.0}part') is not None):
                string = string + printPart(part, params, links, props)

    return string

def printCatalogItem(element):
    string = ""

    title = element.find('{http://csrc.nist.gov/ns/oscal/1.0}title').text

    if (element.get('class') == "family"):
        string = string + ("= %s\n" % (title))

    if (element.get('class') == "SP800-53" or element.get('class') == "SP800-53-enhancement"):
        if (element.get('class') == "SP800-53"):
            indent = 2

        if (element.get('class') == "SP800-53-enhancement"):
            indent = 4

        params = {}
        for param in element.findall('{http://csrc.nist.gov/ns/oscal/1.0}param'):
            if (param.find('{http://csrc.nist.gov/ns/oscal/1.0}label') is not None):
                if (param.get('id') not in params):
                    params[param.get('id')] = []
                params[param.get('id')] = param.find('{http://csrc.nist.gov/ns/oscal/1.0}label').text
            if (param.find('{http://csrc.nist.gov/ns/oscal/1.0}select/choice') is not None):
                for param_item in param.findall('{http://csrc.nist.gov/ns/oscal/1.0}select/choice'):
                    params[param.get('id')].append(param_item.text)

        links = {}
        for link in element.findall('{http://csrc.nist.gov/ns/oscal/1.0}link'):
            i = 0
            if (link.get('rel') not in links):
                links[link.get('rel')] = []
            links[link.get('rel')].append(link.get('href'))
            i+=1

        parts = {}
        for part in element.findall('{http://csrc.nist.gov/ns/oscal/1.0}part'):
            parts[part.get('name')] = part

        props = {}
        for prop in element.findall('{http://csrc.nist.gov/ns/oscal/1.0}prop'):
            props[prop.get('name')] = prop.get('value')

        string = string + ("%s %s %s[[%s]]\n" % ("="*indent, props['label'], title, \
            transformParam(element.get('id'))))

        if (props.get('baseline') or props.get('required_by') or props.get('status')):
            string = string + "\n[width=50\%]\n|===\n"

            if (props.get('baseline')):
                string = string + "|NIST Baseline "

            if (props.get('required_by')):
                string = string + "|Required By "

            string = string + "\n\n"

            if (props.get('baseline')):
                string = string + ("|%s\n" % (props.get('baseline', '')))

            if (props.get('required_by')):
                string = string + ("|%s\n" % (props.get('required_by', '')))

            string = string + "\n|===\n"

        if (props.get('status')):
            string = string + ("\nStatus:: %s\n" % (props.get('status').capitalize()))

        if ('incorporated-into' in links):
            string = string + ("\nIncorporated Into:: %s\n" % (transformInsideLink(links['incorporated-into'])))

        if ('moved-to' in links):
            string = string + ("\nMoved To:: %s\n" % (transformInsideLink(links['moved-to'])))

        if ('statement' in parts):
            string = string + ("\n%s= Control\n" % ("="*indent))
            string = string + printPart(parts['statement'], params, links, props)

        if ('tx_implementation' in parts):
            string = string + ("\n%s= State Implementation Details\n" % ("="*indent))
            string = string + printPart(parts['tx_implementation'], params, links, props)

        if ('tamus_implementation' in parts):
            string = string + ("\n%s= TAMUS Implementation Details\n" % ("="*indent))
            string = string + printPart(parts['tamus_implementation'], params, links, props)

        if ('guidance' in parts):
            string = string + ("\n%s= Supplemental Guidance\n" % ("="*indent))
            string = string + printPart(parts['guidance'], params, links, props)

        if ('reference' in links):
            string = string + ("\n%s= References\n" % ("="*indent))
            string = string + transformReferences(links['reference'])

    return string

resources = {}
for back_matter in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}back-matter'):
    for resource in back_matter.findall('{http://csrc.nist.gov/ns/oscal/1.0}resource'):
        uuid = resource.get('uuid')
        resources[uuid] = resource

for family in root.findall('{http://csrc.nist.gov/ns/oscal/1.0}group'):
    if (family.get('class') == "family"):
        params = {}
        family_file = open(family.get('id') + ".adoc", "w")
        family_file.write(printCatalogItem(family) + "")
        family_file.write(":toc:\n:toclevels: 1\n")
        for param in family.iter('{http://csrc.nist.gov/ns/oscal/1.0}param'):
            param_id = transformParam(param.get('id'))

            if (param.findall('{http://csrc.nist.gov/ns/oscal/1.0}label')):
                params[param_id] = param.find('{http://csrc.nist.gov/ns/oscal/1.0}label').text

            if (param.findall('{http://csrc.nist.gov/ns/oscal/1.0}select')):
                assignment_tag = ""
                if (param.find('{http://csrc.nist.gov/ns/oscal/1.0}select').get('how-many') is not None):
                    assignment_tag = param.find('{http://csrc.nist.gov/ns/oscal/1.0}select').get('how-many') + ": "

                choices = []
                for choice in param.iter('{http://csrc.nist.gov/ns/oscal/1.0}choice'):
                    choices.append(choice.text.strip().replace("\n", ""))

                params[param_id] = "%s%s" % (assignment_tag, ", ".join(choices))

        for key, value in params.items():
            param_row = ":%s: %s\n" % (key, value)
            param_row = param_row.format(**params)
            family_file.write(param_row)

        family_file.write("\n")

        for control in family.findall('{http://csrc.nist.gov/ns/oscal/1.0}control'):
            family_file.write(printCatalogItem(control) + "\n\n")
            if (control.findall('{http://csrc.nist.gov/ns/oscal/1.0}control')):
                family_file.write("=== Control Enhancements\n")
                for enhancement in control.findall('{http://csrc.nist.gov/ns/oscal/1.0}control'):
                    family_file.write(printCatalogItem(enhancement) + "\n")
        family_file.close()
