# Texas A&M University System Security Control Standards Catalog

The Texas A&M University System security control standards catalog provides protective measures for information systems, organizations, and individuals.

The `tamus-cyber/tamus-control-standards` project repository is organized as follows:

| Directory | Description |
|---|---|
| content | Native OSCAL XML files that are used to build control catalogs, profiles, etc. |

Contributions and feedback for future control standards releases are welcome via GitHub. [Please open a new issue with your feedback](https://github.com/tamus-cyber/tamus-control-standards/issues).

Machine-readable formats compliant with the Open Security Controls Assessment Language ([OSCAL](https://pages.nist.gov/OSCAL/)) are available in the [project’s GitHub repository](https://github.com/tamus-cyber/tamus-control-standards) within `content`.

# How to Compile OSCAL Catalog and Update Website

## 0. SET UP PREREQUISITES

0.1. Install Maven via Homebrew

0.2. Create an OSCAL working directory near your home (~) directory

## 1. SET UP REPOSITORIES

1.1. Clone the `OSCAL` repository from `https://github.com/usnistgov/OSCAL.git` into working directory

1.2. Clone the `tamus-control-standards` repository from `https://github.com/tamus-cyber/tamus-control-standards.git` into working directory

## 2. UPDATE CONTROLS CATALOG

2.1. Go into `{WORKING_DIR}/tamus-control-standards/utils`

2.2. Run `sh build-tamus-catalogs.sh [Path to POM] [Path to OSCAL library] [Path to OSCAL content]`
