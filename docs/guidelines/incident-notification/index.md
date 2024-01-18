---
layout: full-width
title: Incident Notification Guidelines
redirect_from: /incident-notification
---

**These guidelines are effective January 9, 2024.**

This document provides guidance to Texas A&M University System members for submitting incident notifications to Texas A&M System Cybersecurity.

Title 1 Texas Administrative Code §202.1 defines "security incident" as "an event which results in the accidental or deliberate unauthorized access, loss, disclosure, modification, disruption, or destruction of information or information resources.[^1]" Texas A&M System cybersecurity control standard IR-6 requires system members to notify Texas A&M System Cybersecurity and consult with the System Chief Information Security Officer regarding information security incidents involving their information and information systems, whether managed by the member, contractor, or other source. This includes privacy incidents that do not impact information systems and any incidents involving industrial control systems or operational technology.

These guidelines support Texas A&M System Cybersecurity in executing its mission objectives and provide the following benefits:

* **Greater quality of information** – Alignment with incident reporting and handling guidance from NIST 800-61 Revision 2 [^2] to introduce functional, informational, and recoverability impact classifications

* **Improved information sharing and situational awareness** – Establishing an 12-hour notification timeframe for all incidents to improve Texas A&M System Cybersecurity’s ability to understand cybersecurity events affecting the system and make timely required notifications to other system offices

* **Faster incident response times** – Moving cause analysis to the closing phase of the incident handling process to expedite initial notification

## Notification Requirement

System members must report information security incidents where the confidentiality, integrity, or availability of a major system-owned or -managed information system, or a system processing confidential information, is potentially compromised.

System members shall notify Texas A&M System Cybersecurity with the required data elements, as well as any other available information, within **12 hours** of being identified by the member or Texas A&M System Cyber Operations.

System members determine which officials of the member institution are to be notified of an incident, but must include the following notifications within **24 hours** of being identified by the member or Texas A&M System Cyber Operations:

1. Agency Director/University President or designee

2. Chief Information Officer (CIO) / Information Resources Manager (IRM)

3. Chief Information Security Officer (CISO) / Information Security Officer (ISO)

4. Chief Research Officer (CRO) _(when the compromised/potentially compromised information includes research data)_

5. Department Head / Information Resources Custodian of affected information resources

Notifications to affected third parties (e.g., vendors, partners) and affected individuals shall be made in accordance with Tex. Bus. & Comm. Code § 521.002 [^3] and guidance provided by the System Office of General Counsel.

In some cases, it may not be feasible to have complete and validated information for [Submitting Incident Notifications](#submitting-incident-notifications) prior to reporting. System members should provide their best estimate at the time of notification and report updated information as it becomes available. Events that have been found by the reporting system member not to impact confidentiality, integrity or availability may be reported voluntarily.

## Submitting Incident Notifications

The information elements described in steps 1-6 below are required when notifying Texas A&M System Cybersecurity of an incident:

1. Identify the current level of impact on system member functions or services (Functional Impact)

2. Identify the type of information lost, compromised, or corrupted (Information Impact)

3. Estimate the scope of time and resources needed to recover from the incident (Recoverability)

4. Identify when the activity was first detected (Date of Detection)

5. Identify the number of systems, records, and users impacted (Number of Systems Affected)

6. Identify the location(s) (campus, building, room, logical network, etc.) impacted (Location)

7. Provide any threat indicators, including signatures, IPs, emails, domains, etc. developed in relationship to the incident (Threat Indicators)

Submit the notification to Texas A&M System Cybersecurity via the [TAMUS ISAO Portal](https://portal.cyber.tamus.edu). Detailed instructions are provided on the [How to Submit an Incident](/incident-notification/submit-incident) page. Once the incident report is reviewed, you will either receive via the TAMUS ISAO Portal a Request for Information alert if more information is needed or a Messenger message acknowledging receipt of the incident report.

## Impact Category Descriptions

The table below defines each impact category description and its associated severity levels. Use the tables below to identify impact levels and incident details.

**Note:** Incidents may affect multiple types of data; therefore, system members may select multiple options when identifying the information impact. The security categorization of information and information systems must be determined in accordance with Federal Information Processing Standards (FIPS) Publication 199.[^4] Specific thresholds for loss-of-service availability (e.g., all, subset, loss of efficiency) must be defined by the reporting organization. Contact the System Research Security Office for guidance on responding to classified data spillage.

| **Impact Category** | **Category Severity Levels** |
|---|---|
| **Functional Impact** - A measure of the impact to business functionality or ability to provide the services | NO IMPACT - Event has no impact<br> NO IMPACT TO SERVICES - Event has no impact to any business or Industrial Control Systems (ICS) services or delivery to entity customers<br> MINIMAL IMPACT TO NON-CRITICAL SERVICES – Some small level of impact to non-critical systems and services<br> MINIMAL IMPACT TO CRITICAL SERVICES –Minimal impact but to a critical system or service, such as email or active directory<br> SIGNIFICANT IMPACT TO NON-CRITICAL SERVICES – A non-critical service or system has a significant impact<br> DENIAL OF NON-CRITICAL SERVICES – A non-critical system is denied or destroyed<br> SIGNIFICANT IMPACT TO CRITICAL SERVICES – A critical system has a significant impact, such as local administrative account compromise<br> DENIAL OF CRITICAL SERVICES/LOSS OF CONTROL – A critical system has been rendered unavailable | 
| **Information Impact** – Describes the type of information lost, compromised, or corrupted | NO IMPACT – No known data impact<br>SUSPECTED BUT NOT IDENTIFIED – A data loss or impact to availability is suspected, but no direct confirmation exists<br>PRIVACY DATA BREACH – The confidentiality of personally identifiable information (PII) or sensitive personal information (SPI) was compromised<br>PROPRIETARY INFORMATION BREACH – The confidentiality of unclassified proprietary information, such as protected critical infrastructure information (PCII), intellectual property, or trade secrets was compromised<br>DESTRUCTION OF NON-CRITICAL SYSTEMS – Destructive techniques, such as master boot record (MBR) overwrite; have been used against a non-critical system<br>CRITICAL SYSTEMS DATA BREACH - Data pertaining to a critical system has been exfiltrated<br>CORE CREDENTIAL COMPROMISE – Core system credentials (such as domain or enterprise administrative credentials) or credentials for critical systems have been exfiltrated<br>DESTRUCTION OF CRITICAL SYSTEM – Destructive techniques, such as MBR overwrite; have been used against a critical system |
| **Recoverability** – Identifies the scope of resources needed to recover from the incident | REGULAR – Time to recovery is predictable with existing resources<br>SUPPLEMENTED – Time to recovery is predictable with additional resources<br>EXTENDED – Time to recovery is unpredictable; additional resources and outside help are needed<br>NOT RECOVERABLE – Recovery from the incident is not possible (e.g., sensitive data exfiltrated and posted publicly) |

## Reporting Contact Information

* [TAMUS ISAO Portal](https://portal.cyber.tamus.edu)

* Supplemental Info / Indicators of Compromise: [contact@cyber.tamus.edu](mailto:contact@cyber.tamus.edu) ([PGP/GPG Key for Encrypted Email](https://cyber.tamus.edu/contact))

* Cyber Operations Watch Officer: (979) 234-0030 Opt. 3

## Footnotes

[^1]: [Title 1 Texas Administrative Code § 202.76, Security Control Standards Catalog](https://www.sos.texas.gov/tac/index.shtml).
[^2]: [NIST Special Publication 800-61 Rev 2, Computer Security Incident Handling Guide, August 2012](https://doi.org/10.6028/NIST.SP.800-61r2).
[^3]: [Texas Business and Commerce Code § 521.002, Unauthorized Use of Identifying Information](https://statutes.capitol.texas.gov/Docs/BC/htm/BC.521.htm).
[^4]: [Federal Information Processing Standard Publication 199, Standards for Security Categorization of Federal Information and Information Systems](https://doi.org/10.6028/NIST.FIPS.199).
