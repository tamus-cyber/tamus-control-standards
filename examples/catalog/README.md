# Example Texas A&M University System Member Security Controls Catalog

This directory contains the OSCAL content and XSLT transforms to publish a PDF or web version of a security controls catalog based on the Texas A&M System Security Control Standards Catalog.

The `tamus-cyber/tamus-control-standards/examples/catalog` project repository is organized as follows:

| Directory | Description |
|---|---|
| content | Native OSCAL YAML files that are used to build controls profiles and catalogs |
| publish | XSLT transforms, Shell scripts, CSS, etc. needed to publish a PDF or web version of a catalog |

Contributions and feedback for future control standards releases are welcome via GitHub. [Please open a new issue with your feedback](https://github.com/tamus-cyber/tamus-control-standards/issues).

# How to Compile OSCAL Catalog and Publish PDF/Web Version

## 0. SET UP PREREQUISITES

0.1. Install the OSCAL CLI tool per the instructions at `https://github.com/usnistgov/oscal-cli`

0.2. Install the `openjdk` Homebrew formula and follow the post-install instructions

## 1. SET UP REPOSITORIES

1.1. Clone the `tamus-control-standards` repository from `https://github.com/tamus-cyber/tamus-control-standards.git` into a working directory

1.2. Customize the predefined text variables in the `examples/catalog/publish/nist-emulation/tamux-catalog_html.xsl` transform file to suit 
the system member

## 2. UPDATE CONTROLS PROFILE OSCAL FILE

2.1. Make changes to `examples/catalog/content/TAMUX_profile.yaml` as needed

## 3. COMPILE CONTROLS CATALOG OSCAL FILE FROM PROFILE

3.1. Run `oscal-cli profile resolve --to=yaml <path/to/tamux/profile> <path/to/tamux/catalog/output>` from the `examples/catalog/content` directory

## 4. GENERATE PDF OR WEB CONTROLS CATALOG FROM OSCAL CATALOG

4.1. Run `sh mvn-make-catalog-[html|pdf].sh <path/to/tamux/catalog> <path/to/html-or-pdf/output/file>` from the `examples/catalog/publish` directory

### Bonus

You can customize the appearance and content of the generated files by modifying the XSLT files in `examples/catalog/publish` and its sub-directories.

### Credits

The `examples/catalog/publish` directory is extracted from https://github.com/usnistgov/oscal-xslt