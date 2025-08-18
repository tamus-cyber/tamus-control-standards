# Texas A&M University System Security Control Standards Catalog

The Texas A&M University System security control standards catalog provides protective measures for information systems, organizations, and individuals.

The `tamus-cyber/tamus-control-standards` project repository is organized as follows:

| Directory | Description |
|---|---|
| content | Native OSCAL YAML files that are used to build controls catalogs, profiles, etc. |
| examples | Sample OSCAL files and XSLT transforms used to build member controls catalogs, etc. |

Contributions and feedback for future control standards releases are welcome via GitHub. [Please open a new issue with your feedback](https://github.com/tamus-cyber/tamus-control-standards/issues).

Machine-readable formats compliant with the Open Security Controls Assessment Language ([OSCAL](https://pages.nist.gov/OSCAL/)) are available in the [project’s GitHub repository](https://github.com/tamus-cyber/tamus-control-standards) within `content`.

# How to Compile OSCAL Catalog and Update Website

## 0. SET UP PREREQUISITES

0.1. Install the OSCAL CLI tool per the instructions at `https://github.com/usnistgov/oscal-cli`

0.2. Install the `openjdk` Homebrew formula and follow the post-install instructions

## 1. SET UP REPOSITORIES

1.1. Clone the `tamus-control-standards` repository from `https://github.com/tamus-cyber/tamus-control-standards.git` into a working directory

## 2. UPDATE CONTROLS CATALOG

2.1. Make changes to `content/tamus.edu/TAMUS_profile.yaml` as needed

## 3. COMPILE OSCAL CONTROLS CATALOGS

3.1. (As needed): Run `oscal-cli profile resolve --to=yaml <path/to/dir/profile> <path/to/dir/catalog/output>` from the `content/texas.gov` directory

3.2. Run `oscal-cli profile resolve --to=yaml <path/to/tamus/profile> <path/to/tamus/catalog/output>` from the `content/tamus.edu` directory
