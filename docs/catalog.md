---
layout: main
title: Cybersecurity Control Standards
header_title: Cybersecurity
header_description: >
  Cybersecurity at the A&M System is an individual and collective efforts of our members. It is necessary for us to work together, sharing resources and information assets.
nav:
  - About
  - Lifecycle
  - Control Catalog
  - References
  - Legacy Security Standard Crosswalk
  - Identity Role Examples
  - Incident Notification Matrix
  - Data Classification
---
# Texas A&M University System Cybersecurity Control Standards

{% include on-this-page.html %}

# Release History

Last Revised: {{ site.time | date_to_rfc822 }}

[View this document's release history in GitHub.](https://github.com/tamuscyber/tamus-control-standards/releases)

# About

Texas A&M University System members publish a security control catalog to implement organizational information security controls in a format that aligns with the Texas Security Control Standards Catalog, prescribed by Title 1 Texas Administrative Code §202.76, Security Control Standards Catalog \[[1 TAC 202.76]\].

Texas A&M System Cybersecurity Control Standards provide system members with additional guidance that enhances State-level requirements for implementing security controls.  These standards are prescribed by Texas A&M System Regulation 29.01.03, Information Security \[[TAMUS 29.01.03]\], paragraph 1.2(c).

This document is intended to be used as a supplement to Texas Security Control Standards Catalog Version 1.3, updated February 26, 2016 \[[TxDIR Catalog]\].

# Lifecycle

The Texas A&M University System Office of Cybersecurity will review control standards each even-numbered year, following the Texas Department of Information Resources’ publishing of new statewide security control standards.

Prior to publishing new or revised standards, the Office of Cybersecurity will solicit comments on new control standards from Chief Information Officers and (Chief) Information Security Officers at system members.

# Control Catalog

- [All controls presented in the Texas Security Control Standards Catalog](/control-catalog)

- [Only controls from the Texas Security Control Standards Catalog required by Texas DIR or the Texas A&M System](/required-controls)

- [Only controls from the Texas Security Control Standards Catalog required by the Texas A&M System](/tamus-required-controls)

- [Only recently updated Texas A&M System required controls](/recent-updated-controls)

# References

{% include_relative catalog-references.md %}

# Legacy Security Standard Crosswalk

## Configuration Management Standard

- [CM-3 Configuration Change Control](control-catalog#cm-3)
- [CM-8	Information System Component Inventory](control-catalog#cm-8)
- [PM-5	Information System Inventory](control-catalog#pm-5)

## Contingency Planning Standard

- [CP-1	Contingency Planning Policy and Procedures](control-catalog#cp-1)
- [CP-2	Contingency Plan](control-catalog#cp-2)
- [CP-4	Contingency Plan Testing](control-catalog#cp-4)

## Data Classification Standard

- [RA-2	Security Categorization](control-catalog#ra-2)
- [Data Classification](#data-classification)

## Electronic Media Protection Standard

- [MP-3	Media Marking](control-catalog#mp-3)

## Electronic Signature Standard

- [Removed from Cybersecurity Control Standards]

## Identity Management Standard

- [AC-1	Access Control Policy and Procedures](control-catalog#ac-1)
- [AC-2	Account Management](control-catalog#ac-2)

## Incident Management Standard

- [IR-6	Incident Reporting](control-catalog#ir-6)

## Information Integrity Standard

- [CM-2	Baseline Configuration](control-catalog#cm-2)
- [CM-10 Software Usage Restrictions](control-catalog#cm-10)
- [PL-4	Rules of Behavior](control-catalog#pl-4)
- [SI-3	Malicious Code Protection](control-catalog#si-3)

## Information Resources Access Standard

- [AC-2	Account Management](control-catalog#ac-2)
- [PL-4	Rules of Behavior](control-catalog#pl-4)

## Information System Monitoring Standard

- [PM-14 Testing, Training, and Monitoring](control-catalog#pm-14)
- [SI-4	Information System Monitoring](control-catalog#si-4)

## Notification Matrix

- [Incident Notification Matrix](#incident-notification-matrix)

## Online Privacy Standard

- [TR-1	Privacy Policy](control-catalog#tr-1)

## Physical and Environmental Protection Standard

- [DM-1	Minimization of Personally Identifiable Information](control-catalog#dm-1)
- [PE-6	Monitoring Physical Access](control-catalog#pe-6)
- [PL-4	Rules of Behavior](control-catalog#pl-4)

## Preservation Holds Standard

-	[Removed from Cybersecurity Control Standards]

## System Development and Acquisition Standard

- [SA-3	System Development Life Cycle](control-catalog#sa-3)
- [SA-4	Acquisition Process](control-catalog#sa-4)

# Identity Role Examples

Active Students
: students who are enrolled and attending in learning activities at system institutions

Alumni
: non-personnel who are either former students, graduates or former employees (in good standing) who may be granted some limited access to information resources

Faculty
: personnel who act as instructors or assistants to instructors at system institutions

Financial Staff
: personnel whose work role is to perform financial activities, such as accounting, bursar, budgeting, procurement, invoicing and disbursement activities

Guest
: non-personnel who may or may not be affiliated with system institutions who have temporary and limited access to system information resources

HIPAA-access
: this role is a sub-role that is usually combined with other roles which further define related attributes and is not a healthcare professional but has access to HIPAA-related information

Healthcare Professional
: personnel who have access to HIPAA-related information in accordance with health-related work or research activities

Human Resources
: personnel whose work activities include the ability to view or update personnel records, coordinate performance reviews, perform compensation management and view or manage HIPAA-related or insurance-related information related to personnel

Inactive Students
: students who are not enrolled and are not attending in learning activities at a system institution

IT Security
: personnel who perform cybersecurity activities for system institutions

IT Staff
: information technology professionals and help desk or technical support staff who operate or support IT infrastructure or applications; this also includes programming and database activities

Law Enforcement
: personnel who are a part of the system’s university police departments

Partner (Research)
: non-personnel who are affiliated with system institutions or activities but are not employees; they may be granted specific but limited access to system-related information resources and must be closely monitored

Physical Security
: personnel whose work activities include the physical protection and monitoring of system facilities

Research Professional
: personnel who work in officially sanctioned and recognized system research activities

Staff/Administrative/Service
: personnel who participate in general administrative duties at system institutions

Student Workers
: students who are enrolled and attending learning activities and are also performing officially recognized and sanctioned work activities on behalf of a system institution

Vendor/Service Provider
: non-personnel who perform some service to system institutions that require access to specific and limited information resources for specified activities; their activities must be closely monitored

Visiting Professor
: a person who is employed as a professor or instructor at another university institution that has been officially invited by the system to act as a professor and participate in teaching activities for some defined time; the visiting professor may be granted specific but limited access to system-related information resources and must be closely monitored

Visiting Research Professional
: personnel who are not system employees, faculty or researchers, but who have an official system research sponsor who is either doing direct or assistive work with system research

# Incident Notification Matrix

[![Incident Notification Matrix](/static/images/incident-notification-matrix.png)](/static/pdf/incident-notification-matrix.pdf)

# Data Classification

Texas A&M University System (A&M System) data classification consists of a minimum of three specific classifications based on access restrictions and risk. These classifications apply to all members. While the classification applicable to specific information may change based on circumstances, the intent of this document is to define the appropriate classification for different types of information. These three classifications are:

| **Classification** | **Description** | **Examples** | **Comments** |
|-|-|-|-|
| **Confidential Information** | Information that must be protected from unauthorized disclosure or public release based on state or federal law or other legal agreement (1 TAC §202.1). | - Patient billing information and protected health information as protected by HIPAA.<br>- Student education records protected by FERPA.<br>- Information or Information System security plans, reports and related information<br>- Credit/debit card numbers, bank account numbers<br>- Personal financial information<br>- Social security numbers<br>- A&M System intellectual property and research information having commercial potential<br><br>Confidential Information requiring breach notifications or having stricter access requirements may include SPI as defined by Texas Business and Commerce Code § 521.002(a)(2); credit card numbers covered by PCI DSS v3.1.<br><br>Classified National Security Information under Executive Order 13526, and Controlled Unclassified Information under Executive Order 13556, shall be protected as prescribed by System Regulations 15.05.01 and 15.05.02, respectively, and the System Facility Security Officer (FSO). | This classification may not be absolute; context is an essential element.<br><br>Owners of confidential information must ensure such information is correctly classified.<br><br>Custodians of confidential information must implement appropriate controls.<br><br>HIPAA, FTI or PCI information is covered in this category. This classification may include agreements or contracts for research work that require higher levels of security and/or procedural elements for handling of information.<br><br>Consult the Office of General Counsel regarding confidential information requested through open records, subpoena, or other legal process. |
| **Internal Use** | Information that is not generally created for or made available for public consumption but that may or may not be subject to public disclosure through the Texas Public Information Act or similar laws. | This information includes institutional budgetary, financial and operational records such as expenditures, statistics, contracting information, non-confidential personnel information. It may also include non-confidential internal communications. | Consult the Office of General Counsel regarding controlled information requested through open records, subpoena, or other legal process. |
| **Public Information** | Public information includes all information made available to the public through posting to public websites, distribution through email, or social media, print publications or other media. This classification also includes information for which public disclosure is intended or required. | Published system and system member policy documents, organizational charts, Statistical reports, Fast Facts, unrestricted directory information, employee salaries, and educational content available to the public at no cost. | Information can migrate from one classification to another based on information lifecycle. For example, a draft policy document would fit the criteria of “Internal Use” until being published upon which it would become “Public Information”. |

1. Each member will use this classification criteria as their baseline standard. If a member requires a more restrictive classification for a class of data due to state, federal or other agreements, the more restrictive classification will apply.

2. This classification criteria will be used to assess information access and security requirements for information to be stored or processed within member shared information centers.

3. When determining security controls to use for a given set of information, Information Owners and Custodians should also assess whether special requirements exist regarding importance of information availability and integrity and rate the need as LOW, MODERATE, or HIGH for both integrity and availability. The needs regarding availability and integrity may impact security control decisions but are not used for purposes of assigning a classification label of Confidential, Internal Use, or Public.

4. Some classes of information may have attributes, such as “mission critical” or “business critical”. Information attributes do not supplant these classifications but should be used to clarify their importance to the institution.

## State of Texas Requirement

“State institutions of higher education are responsible for defining all information classification categories except the Confidential Information category, which is defined in Subchapter A of this chapter, and establishing the controls for each” (1 Tex. Admin. Code § 202.74(b)(1)).

## FIPS 199 Impact Table

| **Security Objective** | **LOW** | **MODERATE** | **HIGH** |
|-|-|-|-|
| ***Confidentiality***<br>Preserving authorized restriction on information access and disclosure including means for protecting personal privacy and proprietary information. | The unauthorized disclosure of information could be expected to have a **limited** adverse effect on organizational operations, organizational assets, or individuals. | The unauthorized disclosure of information could be expected to have a **serious** adverse effect on organizational operations, organizational assets, or individuals. | The unauthorized disclosure of information could be expected to have a **severe or catastrophic** adverse effect on organizational operations, organizational assets, or individuals. |
| ***Integrity***<br>Guarding against improper information modification or destruction, and includes ensuring information non-repudiation and authenticity. | The unauthorized modification or destruction of information could be expected to have a **limited** adverse effect on organizational operations, organizational assets, or individuals. | The unauthorized modification or destruction of information could be expected to have a **serious** adverse effect on organizational operations, organizational assets, or individuals. | The unauthorized modification or destruction of information could be expected to have a **severe or catastrophic** adverse effect on organizational operations, organizational assets, or individuals. |
| ***Availability***<br>Ensuring timely and reliable access to and use of information. | The disruption of access to or use of information or an information system could be expected to have a **limited** adverse effect on organizational operations, organizational assets, or individuals. | The disruption of access to or use of information or an information system could be expected to have a **serious** adverse effect on organizational operations, organizational assets, or individuals. | The disruption of access to or use of information or an information system could be expected to have a **severe or catastrophic** adverse effect on organizational operations, organizational assets, or individuals. |

Using the table above, any set of information can be assigned three security ratings: one for Confidentiality (LOW, MODERATE or HIGH), another for Integrity (LOW, MODERATE or HIGH), and a third for Availability (LOW, MODERATE or HIGH). This is useful for defining security controls in cases where, for example, a set of information may have a low need for confidentiality (LOW impact) but require HIGH availability. In this example, encryption may not be appropriate, but redundancy may be a requirement.

Most breaches that cause HIGH impact are a result of unauthorized access to Confidential information. Therefore, this document and System member assignment of classification places prime importance on the level of Confidentiality required of the information.

{% include references.md %}
