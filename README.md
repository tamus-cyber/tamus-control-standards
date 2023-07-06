# Texas A&M University System Cybersecurity Control Standards

Texas A&M System Cybersecurity Control Standards provide system members with additional guidance that enhances State-level requirements for implementing security controls.

The `tamus-cyber/tamus-control-standards` project repository is organized as follows:

| Directory | Description |
|---|---|
| content | Native OSCAL XML files that are used to build control catalogs, profiles, etc. |
| docs | The compiled Cybersecurity Control Standards website at https://cyber-standards.tamus.edu |
| oscal-xslt | Patch files to customize NIST's `usnistgov/oscal-xslt` GitHub repository for TAMUS use |

Contributions and feedback for future control standards releases are welcome via GitHub. [Please open a new issue with your feedback](https://github.com/tamus-cyber/tamus-control-standards/issues).

Machine-readable formats compliant with the Open Security Controls Assessment Language ([OSCAL](https://pages.nist.gov/OSCAL/)) are available in the [project’s GitHub repository](https://github.com/tamus-cyber/tamus-control-standards) within `content`.

# How to Compile OSCAL Catalog and Update Website

## 0. SET UP PREREQUISITES

0.1. Install Maven via Homebrew

0.2. Create an OSCAL working directory near your home (~) directory

## 1. SET UP REPOSITORIES

1.1. Clone the `OSCAL` repository from `https://github.com/usnistgov/OSCAL.git` into working directory

1.2. Clone the `oscal-xslt` repository from `https://github.com/usnistgov/oscal-xslt.git` into working directory

1.3. Clone the `tamus-control-standards` repository from `https://github.com/tamus-cyber/tamus-control-standards.git` into working directory

## 2. PATCH OSCAL-XSLT WITH TAMUS CUSTOM CONTENT

2.1. Go into `{WORKING_DIR}/oscal-xslt`

2.2. Run `sh {WORKING_DIR}/tamus-control-standards/oscal-xslt/tamus-build.sh`

## 3. UPDATE CONTROLS CATALOG

3.1. Go into `{WORKING_DIR}/tamus-control-standards/content`

3.2. Run `sh tamus-build.sh`

## 4. GENERATE NEW CONTROLS CATALOG WEBPAGES

4.1. Go into `{WORKING_DIR}/oscal-xslt/publish`

4.2. Run `sh make-tamus-html.sh`

## 5. PUBLISH CHANGES TO GITHUB

5.1. Go into `{WORKING_DIR}/tamus-control-standards`

5.2. Commit and push changes to GitHub
