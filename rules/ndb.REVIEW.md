# ndb — Extraction Review

*66 rules extracted. Signed off 2026-06-15 with the following known issues:*

## Known Issues

1. **26WG-c-d-sensitive condition is inverted** — `{"in": [{"var": "data_categories"}, ["health"]]}` has needle/haystack reversed in JSON Logic. Should be `{"some": [{"var": "data_categories"}, {"in": [{"var": ""}, ["health","financial","identity","biometric","sensitive"]]}]}`. Evaluate manually until corrected in rules/ndb.json.

2. **Almost all rules are LOW codifiability** — correct per the statute. NDB serious harm is a judgment call; the sandbox shows which factors are triggered, not a yes/no verdict. This is the intended design.

3. **Source URLs mostly empty** — docref links for 26WA–26WN and 26WR rules are blank. 26WG rules point to C2017A00012 (not the current compilation). Fix: `https://www.legislation.gov.au/C2004A03712/latest/text` per section.

4. **66 rules is long for demo** — 26WP/26WQ/26WR are procedural Commissioner-direction rules rarely triggered in demo scenarios. Consider filtering to key rules (26WA, 26WE, 26WG, 26WL, 26WR) in a future version.

## [HIGH] Eligible data breach requires unauthorised access, disclosure or loss

- **Rule ID:** `26WA_eligible_breach_access_disclosure_loss`
- **Docref:** 26WA Guide to this Part — [source]()
- **Condition:** `{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure", "loss"]]}`
- **Obligation:** The incident must involve unauthorised access to, unauthorised disclosure of, or loss of, personal information held by an entity to potentially constitute an eligible data breach.

## [LOW] Eligible data breach requires likelihood of serious harm

- **Rule ID:** `26WA_serious_harm_requirement`
- **Docref:** 26WA Guide to this Part — [source]()
- **Condition:** `null`
- **Obligation:** The access, disclosure or loss must be likely to result in serious harm to any of the individuals to whom the information relates for it to be an eligible data breach.

## [LOW] Notification required on reasonable grounds to believe breach occurred

- **Rule ID:** `26WA_notification_reasonable_grounds`
- **Docref:** 26WA Guide to this Part — [source]()
- **Condition:** `null`
- **Obligation:** An entity must give a notification if it has reasonable grounds to believe that an eligible data breach has happened.

## [LOW] Notification required when directed by Commissioner

- **Rule ID:** `26WA_notification_commissioner_direction`
- **Docref:** 26WA Guide to this Part — [source]()
- **Condition:** `null`
- **Obligation:** An entity must give a notification if it is directed to do so by the Commissioner.

## [LOW] Commissioner may obtain information or documents on actual or suspected breaches

- **Rule ID:** `26WA_commissioner_information_powers`
- **Docref:** 26WA Guide to this Part — [source]()
- **Condition:** `null`
- **Obligation:** The Commissioner may obtain information or documents in relation to actual or suspected eligible data breaches.

## [LOW] Entity includes file number recipient

- **Rule ID:** `26WB_entity_includes_file_number_recipient`
- **Docref:** 26WB 26WB — [source]()
- **Condition:** `null`
- **Obligation:** For the purposes of this Part, the term 'entity' includes a person who is a file number recipient.

## [LOW] Deemed holding of information disclosed to overseas recipient

- **Rule ID:** `26WC-1`
- **Docref:** 26WC 26WC(1) — [source]()
- **Condition:** `null`
- **Obligation:** Where an APP entity has disclosed personal information to an overseas recipient under APP 8.1 and the overseas recipient holds the information, this Part has effect as if the personal information were held by the APP entity and the APP entity were required under section 15 not to breach APP 11.1 in relation to that information.

## [LOW] Deemed holding of credit eligibility information disclosed to bodies with no Australian link

- **Rule ID:** `26WC-2`
- **Docref:** 26WC 26WC(2) — [source]()
- **Condition:** `null`
- **Obligation:** Where a credit provider has disclosed credit eligibility information under paragraph 21G(3)(b) or (c) or subsection 21M(1) to a related body corporate, body or person with no Australian link, and that recipient holds the information, this Part has effect as if the credit eligibility information were held by the credit provider and the credit provider were required to comply with subsection 21S(1) in relation to that information.

## [LOW] Exception for breaches notified under My Health Records Act 2012

- **Rule ID:** `26WD_my_health_records_exception`
- **Docref:** 26WD Exception—notification under the My Health Records Act 2012 — [source]()
- **Condition:** `{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure", "loss"]]}`
- **Obligation:** This Part (the NDB scheme) does not apply in relation to the access, disclosure or loss where it has been, or is required to be, notified under section 75 of the My Health Records Act 2012.

## [LOW] Eligible data breach via unauthorised access or disclosure likely to result in serious harm

- **Rule ID:** `26WE-2-a`
- **Docref:** 26WE 26WE(2)(a) — [source]()
- **Condition:** `{"and": [{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure"]]}]}`
- **Obligation:** Where there is unauthorised access to or unauthorised disclosure of the information and a reasonable person would conclude it would be likely to result in serious harm to any affected individual, the access or disclosure is an eligible data breach.

## [LOW] Eligible data breach via loss where unauthorised access/disclosure likely and serious harm likely

- **Rule ID:** `26WE-2-b`
- **Docref:** 26WE 26WE(2)(b) — [source]()
- **Condition:** `{"==": [{"var": "incident_type"}, "loss"]}`
- **Obligation:** Where information is lost in circumstances where unauthorised access or disclosure is likely to occur, and a reasonable person would conclude that such access or disclosure would be likely to result in serious harm to any affected individual, the loss is an eligible data breach.

## [LOW] Individual at risk from eligible data breach

- **Rule ID:** `26WE-2-d`
- **Docref:** 26WE 26WE(2)(d) — [source]()
- **Condition:** `null`
- **Obligation:** An individual to whom the information relates and who would be likely to suffer serious harm is at risk from the eligible data breach.

## [LOW] Scope of section - entities required to protect held information

- **Rule ID:** `26WE-1`
- **Docref:** 26WE 26WE(1) — [source]()
- **Condition:** `null`
- **Obligation:** This section applies where an APP entity, credit reporting body, credit provider, or file number recipient holds relevant personal/credit/tax file number information and is required to comply with the applicable protection obligation.

## [LOW] Remedial action for access/disclosure prevents eligible data breach

- **Rule ID:** `26WF-1`
- **Docref:** 26WF (1) — [source]()
- **Condition:** `{"and": [{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure"]]}]}`
- **Obligation:** If the entity takes remedial action before the access or disclosure results in serious harm, and as a result a reasonable person would conclude serious harm is no longer likely, the access or disclosure is taken never to have been an eligible data breach of the entity or any other entity.

## [LOW] Remedial action for access/disclosure removes notification requirement for particular individual

- **Rule ID:** `26WF-2`
- **Docref:** 26WF (2) — [source]()
- **Condition:** `{"and": [{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure"]]}]}`
- **Obligation:** If the entity takes remedial action before the access or disclosure results in serious harm to a particular individual, and as a result a reasonable person would conclude serious harm to that individual is no longer likely, this Part does not require the entity or any other entity to notify that individual of the statement contents.

## [MEDIUM] Remedial action for loss before any unauthorised access/disclosure prevents eligible data breach

- **Rule ID:** `26WF-3`
- **Docref:** 26WF (3) — [source]()
- **Condition:** `{"==": [{"var": "incident_type"}, "loss"]}`
- **Obligation:** If the entity takes remedial action in relation to the loss before there is any unauthorised access to or disclosure of the information, and as a result there is no unauthorised access or disclosure, the loss is taken never to have been an eligible data breach of the entity or any other entity.

## [LOW] Remedial action for loss after access/disclosure prevents eligible data breach

- **Rule ID:** `26WF-4`
- **Docref:** 26WF (4) — [source]()
- **Condition:** `{"==": [{"var": "incident_type"}, "loss"]}`
- **Obligation:** If the entity takes remedial action after there is unauthorised access or disclosure but before it results in serious harm, and as a result a reasonable person would conclude serious harm is no longer likely, the loss is taken never to have been an eligible data breach of the entity or any other entity.

## [LOW] Remedial action for loss removes notification requirement for particular individual

- **Rule ID:** `26WF-5`
- **Docref:** 26WF (5) — [source]()
- **Condition:** `{"==": [{"var": "incident_type"}, "loss"]}`
- **Obligation:** If the entity takes remedial action after there is unauthorised access or disclosure but before it results in serious harm to a particular individual, and as a result a reasonable person would conclude serious harm to that individual is no longer likely, this Part does not require the entity or any other entity to notify that individual of the statement contents.

## [MEDIUM] Sensitivity of information as serious harm factor

- **Rule ID:** `26WG-c-d-sensitive`
- **Docref:** 26WG (c)-(d) — [source](https://www.legislation.gov.au/Details/C2017A00012)
- **Condition:** `{"or": [{"in": [{"var": "data_categories"}, ["health"]]}, {"in": [{"var": "data_categories"}, ["financial"]]}, {"in": [{"var": "data_categories"}, ["identity"]]}, {"in": [{"var": "data_categories"}, ["biometric"]]}, {"in": [{"var": "data_categories"}, ["sensitive"]]}]}`
- **Obligation:** Have regard to the kind and sensitivity of the information when assessing whether serious harm is likely

## [MEDIUM] Security measures and likelihood of being overcome

- **Rule ID:** `26WG-e-f-security`
- **Docref:** 26WG (e)-(f) — [source](https://www.legislation.gov.au/Details/C2017A00012)
- **Condition:** `{"in": [{"var": "encryption_status"}, ["encrypted", "partial", "unencrypted"]]}`
- **Obligation:** Have regard to whether the information is protected by security measures and the likelihood those measures could be overcome

## [MEDIUM] Persons who have or could obtain the information

- **Rule ID:** `26WG-g-recipients`
- **Docref:** 26WG (g) — [source](https://www.legislation.gov.au/Details/C2017A00012)
- **Condition:** `{"in": [{"var": "likely_recipient"}, ["unknown", "specific_individual", "criminal", "broad_public"]]}`
- **Obligation:** Have regard to the persons or kinds of persons who have obtained or could obtain the information

## [MEDIUM] Likelihood of circumventing security technology by malicious actors

- **Rule ID:** `26WG-h-circumvention`
- **Docref:** 26WG (h) — [source](https://www.legislation.gov.au/Details/C2017A00012)
- **Condition:** `{"and": [{"in": [{"var": "encryption_status"}, ["encrypted", "partial"]]}, {"==": [{"var": "likely_recipient"}, "criminal"]}]}`
- **Obligation:** Have regard to the likelihood that persons with intent to cause harm could obtain knowledge required to circumvent the security technology (e.g. an encryption key)

## [LOW] Nature of the harm

- **Rule ID:** `26WG-i-nature-of-harm`
- **Docref:** 26WG (i) — [source](https://www.legislation.gov.au/Details/C2017A00012)
- **Condition:** `null`
- **Obligation:** Have regard to the nature of the harm when assessing whether serious harm is likely

## [LOW] Any other relevant matters

- **Rule ID:** `26WG-j-other-matters`
- **Docref:** 26WG (j) — [source](https://www.legislation.gov.au/Details/C2017A00012)
- **Condition:** `null`
- **Obligation:** Have regard to any other relevant matters when assessing whether serious harm is likely

## [LOW] Reasonable and expeditious assessment of suspected breach

- **Rule ID:** `26WH_2a`
- **Docref:** 26WH 26WH(2)(a) — [source]()
- **Condition:** `null`
- **Obligation:** The entity must carry out a reasonable and expeditious assessment of whether there are reasonable grounds to believe that the relevant circumstances amount to an eligible data breach of the entity.

## [LOW] Complete assessment within 30 days

- **Rule ID:** `26WH_2b`
- **Docref:** 26WH 26WH(2)(b) — [source]()
- **Condition:** `null`
- **Obligation:** The entity must take all reasonable steps to ensure that the assessment is completed within 30 days after the entity becomes aware of the reasonable grounds to suspect an eligible data breach.

## [LOW] Exception for shared data breach already notified by another entity

- **Rule ID:** `26WJ-1`
- **Docref:** 26WJ Exception—eligible data breaches of other entities — [source]()
- **Condition:** `null`
- **Obligation:** Section 26WH (notification obligation) does not apply to an other entity in relation to an eligible data breach where another entity has already complied with section 26WH in relation to the same access, disclosure or loss that constituted an eligible data breach of both entities.

## [LOW] Obligation to prepare and give statement to Commissioner

- **Rule ID:** `26WK-1`
- **Docref:** 26WK 26WK(2) — [source]()
- **Condition:** `null`
- **Obligation:** The entity must prepare a statement complying with subsection (3) and give a copy to the Commissioner as soon as practicable after becoming aware of reasonable grounds to believe an eligible data breach has occurred.

## [LOW] Required content of statement

- **Rule ID:** `26WK-2`
- **Docref:** 26WK 26WK(3) — [source]()
- **Condition:** `null`
- **Obligation:** The statement must set out the identity and contact details of the entity, a description of the eligible data breach, the particular kind or kinds of information concerned, and recommendations about steps individuals should take in response.

## [LOW] Optional inclusion of other affected entities

- **Rule ID:** `26WK-3`
- **Docref:** 26WK 26WK(4) — [source]()
- **Condition:** `null`
- **Obligation:** If the entity has reasonable grounds to believe the breach is also an eligible data breach of one or more other entities, the statement may also set out the identity and contact details of those other entities.

## [LOW] Notification obligation triggered by reasonable grounds and prepared statement

- **Rule ID:** `26WL-1`
- **Docref:** 26WL (1) — [source]()
- **Condition:** `null`
- **Obligation:** If an entity is aware of reasonable grounds to believe an eligible data breach has occurred and has prepared a compliant statement, the entity must notify the breach.

## [LOW] Notify individuals to whom information relates if practicable

- **Rule ID:** `26WL-2`
- **Docref:** 26WL (2)(a) — [source]()
- **Condition:** `null`
- **Obligation:** If practicable, the entity must take reasonable steps to notify the contents of the statement to each individual to whom the relevant information relates.

## [LOW] Notify individuals at risk if practicable

- **Rule ID:** `26WL-3`
- **Docref:** 26WL (2)(b) — [source]()
- **Condition:** `null`
- **Obligation:** If it is not practicable to notify all individuals to whom information relates but practicable to notify individuals at risk, the entity must take reasonable steps to notify the contents of the statement to each individual at risk from the breach.

## [LOW] Publish statement if direct notification not practicable

- **Rule ID:** `26WL-4`
- **Docref:** 26WL (2)(c) — [source]()
- **Condition:** `null`
- **Obligation:** If neither direct notification option is practicable, the entity must publish a copy of the statement on its website (if any) and take reasonable steps to publicise the contents of the statement.

## [LOW] Timing of notification

- **Rule ID:** `26WL-5`
- **Docref:** 26WL (3) — [source]()
- **Condition:** `null`
- **Obligation:** The entity must comply with the notification obligation as soon as practicable after completing preparation of the statement.

## [LOW] Method of providing statement to individual

- **Rule ID:** `26WL-6`
- **Docref:** 26WL (4) — [source]()
- **Condition:** `null`
- **Obligation:** If the entity normally communicates with a particular individual using a particular method, the notification may use that method.

## [LOW] Exception from notification for other entities sharing the same breach

- **Rule ID:** `26WM-1`
- **Docref:** 26WM 26WM — [source]()
- **Condition:** `null`
- **Obligation:** Sections 26WK and 26WL do not apply to other entities in relation to the same eligible data breach where one entity has already complied with sections 26WK and 26WL for that breach.

## [LOW] Exception for enforcement related activities

- **Rule ID:** `26WN-enforcement-exception`
- **Docref:** 26WN 26WN — [source]()
- **Condition:** `null`
- **Obligation:** Paragraph 26WK(3)(d) and section 26WL (notification obligations) do not apply to the eligible data breach where the entity is an enforcement body and its CEO believes on reasonable grounds that there has been an eligible data breach and that compliance with section 26WL would be likely to prejudice one or more enforcement related activities.

## [LOW] Exception extends to other entities affected by same breach

- **Rule ID:** `26WN-extension-other-entities`
- **Docref:** 26WN 26WN — [source]()
- **Condition:** `null`
- **Obligation:** If the access, disclosure or loss constituting the eligible data breach is also an eligible data breach of one or more other entities, the exception (non-application of paragraph 26WK(3)(d) and section 26WL) also applies to those other entities' eligible data breaches.

## [LOW] Definition of secrecy provision

- **Rule ID:** `26WP_def_secrecy_provision`
- **Docref:** 26WP 26WP(1) — [source]()
- **Condition:** `null`
- **Obligation:** A 'secrecy provision' is a provision of a Commonwealth law (other than the Privacy Act) that prohibits or regulates the use or disclosure of information.

## [LOW] Exception to 26WK(2) statement detail for inconsistency with secrecy provision

- **Rule ID:** `26WP_exception_26WK_secrecy`
- **Docref:** 26WP 26WP(2) — [source]()
- **Condition:** `null`
- **Obligation:** Where compliance with subparagraph 26WK(2)(a)(ii) (recommended steps content in the statement) would be inconsistent with a non-prescribed secrecy provision, subsection 26WK(2) does not apply to the extent of the inconsistency.

## [LOW] Exception to 26WL notification for inconsistency with secrecy provision

- **Rule ID:** `26WP_exception_26WL_secrecy`
- **Docref:** 26WP 26WP(3) — [source]()
- **Condition:** `null`
- **Obligation:** Where compliance with section 26WL (notifying individuals) would be inconsistent with a non-prescribed secrecy provision, section 26WL does not apply to the extent of the inconsistency.

## [LOW] Definition of prescribed secrecy provision

- **Rule ID:** `26WP_def_prescribed_secrecy_provision`
- **Docref:** 26WP 26WP(4) — [source]()
- **Condition:** `null`
- **Obligation:** A 'prescribed secrecy provision' is a secrecy provision specified in the regulations.

## [LOW] Prescribed secrecy provision treatment of 26WK and 26WL

- **Rule ID:** `26WP_prescribed_not_authorising`
- **Docref:** 26WP 26WP(5) — [source]()
- **Condition:** `null`
- **Obligation:** For a prescribed secrecy provision, subparagraph 26WK(2)(a)(ii) and section 26WL are taken not to be provisions that require or authorise the use or disclosure of information.

## [LOW] Full exception to 26WK(2) for inconsistency with prescribed secrecy provision

- **Rule ID:** `26WP_exception_26WK_prescribed`
- **Docref:** 26WP 26WP(6) — [source]()
- **Condition:** `null`
- **Obligation:** Where compliance with subparagraph 26WK(2)(a)(ii) would be inconsistent to any extent with a prescribed secrecy provision, subsection 26WK(2) does not apply to the entity in relation to the statement.

## [LOW] Full exception to 26WL for inconsistency with prescribed secrecy provision

- **Rule ID:** `26WP_exception_26WL_prescribed`
- **Docref:** 26WP 26WP(7) — [source]()
- **Condition:** `null`
- **Obligation:** Where compliance with section 26WL would be inconsistent to any extent with a prescribed secrecy provision, section 26WL does not apply to the entity in relation to the statement.

## [LOW] Commissioner may declare exception to sections 26WK and 26WL

- **Rule ID:** `26WQ-1-declaration-power`
- **Docref:** 26WQ (1) — [source]()
- **Condition:** `null`
- **Obligation:** The Commissioner may, by written notice to the entity, declare that sections 26WK and 26WL do not apply to the eligible data breach (and related breaches of other entities), or that subsection 26WL(3) requires compliance with 26WL(2) within a specified period.

## [LOW] Time extension limited to reasonable period

- **Rule ID:** `26WQ-2-extension-reasonable-period`
- **Docref:** 26WQ (2) — [source]()
- **Condition:** `null`
- **Obligation:** The Commissioner may only use the paragraph (1)(d) power to extend the time for compliance with subsection 26WL(2) to the end of a period the Commissioner is satisfied is reasonable in the circumstances.

## [LOW] Declaration only if reasonable in the circumstances

- **Rule ID:** `26WQ-3-reasonableness-requirement`
- **Docref:** 26WQ (3) — [source]()
- **Condition:** `null`
- **Obligation:** The Commissioner must not make a declaration unless satisfied it is reasonable in the circumstances, having regard to the public interest, relevant advice from an enforcement body or the Australian Signals Directorate, and any other relevant matters.

## [LOW] Advice considered not limited to specified bodies

- **Rule ID:** `26WQ-4-advice-not-limited`
- **Docref:** 26WQ (4) — [source]()
- **Condition:** `null`
- **Obligation:** Paragraph (3)(b) does not limit the advice to which the Commissioner may have regard.

## [LOW] Declaration on own initiative or on application

- **Rule ID:** `26WQ-5-initiation`
- **Docref:** 26WQ (5) — [source]()
- **Condition:** `null`
- **Obligation:** The Commissioner may give notice of a declaration on the Commissioner's own initiative or on application made by the entity.

## [LOW] Forms of application for declaration

- **Rule ID:** `26WQ-6-application-types`
- **Docref:** 26WQ (6) — [source]()
- **Condition:** `null`
- **Obligation:** An entity's application may be expressed as an application for a paragraph (1)(c) declaration, a paragraph (1)(d) declaration, or a paragraph (1)(c) declaration with a fallback to a paragraph (1)(d) declaration if the Commissioner is not disposed to grant the former.

## [LOW] Commissioner may refuse application with written notice

- **Rule ID:** `26WQ-7-refusal-notice`
- **Docref:** 26WQ (7) — [source]()
- **Condition:** `null`
- **Obligation:** The Commissioner may refuse an application and, if so, must give written notice of the refusal to the entity.

## [LOW] Specifying different period not a refusal

- **Rule ID:** `26WQ-8-different-period-not-refusal`
- **Docref:** 26WQ (8) — [source]()
- **Condition:** `null`
- **Obligation:** Where an application nominates a period and the Commissioner makes the declaration but specifies a different period, the Commissioner is taken not to have refused the application.

## [LOW] Sections 26WK and 26WL suspended pending decision

- **Rule ID:** `26WQ-9-suspension-pending-decision`
- **Docref:** 26WQ (9) — [source]()
- **Condition:** `null`
- **Obligation:** If an entity applies for a declaration relating to an eligible data breach, sections 26WK and 26WL do not apply to the breach (and related breaches of other entities) until the Commissioner makes a decision on the application.

## [LOW] No application where another entity has applied for same breach

- **Rule ID:** `26WQ-10-no-duplicate-application`
- **Docref:** 26WQ (10) — [source]()
- **Condition:** `null`
- **Obligation:** An entity is not entitled to make an application in relation to its eligible data breach if the same access, disclosure or loss is also an eligible data breach of another entity and that other entity has already made an application.

## [LOW] Commissioner may extend specified period

- **Rule ID:** `26WQ-11-extension-of-specified-period`
- **Docref:** 26WQ (11) — [source]()
- **Condition:** `null`
- **Obligation:** If notice of a paragraph (1)(d) declaration has been given, the Commissioner may by written notice extend the period specified in the declaration.

## [LOW] Commissioner may direct entity to prepare and provide statement

- **Rule ID:** `26WR-1`
- **Docref:** 26WR (1) — [source]()
- **Condition:** `null`
- **Obligation:** If the Commissioner has reasonable grounds to believe there has been an eligible data breach, the Commissioner may direct the entity by written notice to prepare a compliant statement and give a copy to the Commissioner.

## [LOW] Direction must require notification to affected individuals

- **Rule ID:** `26WR-2`
- **Docref:** 26WR (2) — [source]()
- **Condition:** `null`
- **Obligation:** The direction must require the entity to: if practicable, take reasonable steps to notify the statement contents to each individual to whom the information relates; or if practicable, to each individual at risk; or otherwise publish on website and take reasonable steps to publicise.

## [LOW] Commissioner must invite submission before direction

- **Rule ID:** `26WR-3`
- **Docref:** 26WR (3) — [source]()
- **Condition:** `null`
- **Obligation:** Before giving a direction under subsection (1), the Commissioner must invite the entity to make a submission within a specified period.

## [LOW] Required contents of statement

- **Rule ID:** `26WR-4`
- **Docref:** 26WR (4) — [source]()
- **Condition:** `null`
- **Obligation:** The statement must set out: the entity's identity and contact details; a description of the eligible data breach; the particular kind(s) of information concerned; and recommendations about steps individuals should take in response.

## [LOW] Direction may require additional specified information

- **Rule ID:** `26WR-5`
- **Docref:** 26WR (5) — [source]()
- **Condition:** `null`
- **Obligation:** A direction may also require the statement to set out specified information relating to the eligible data breach.

## [LOW] Matters Commissioner must consider before directing

- **Rule ID:** `26WR-6`
- **Docref:** 26WR (6) — [source]()
- **Condition:** `null`
- **Obligation:** In deciding whether to give a direction, the Commissioner must have regard to relevant advice from an enforcement body or the Australian Signals Directorate, any relevant submission made by the entity within the specified period, and any other relevant matters.

## [LOW] Direction may require identity of other affected entities

- **Rule ID:** `26WR-7`
- **Docref:** 26WR (8) — [source]()
- **Condition:** `null`
- **Obligation:** If the Commissioner has reasonable grounds to believe the breach is also an eligible data breach of one or more other entities, the direction may require the statement to set out the identity and contact details of those other entities.

## [LOW] Method of notifying an individual

- **Rule ID:** `26WR-8`
- **Docref:** 26WR (9) — [source]()
- **Condition:** `null`
- **Obligation:** If the entity normally communicates with a particular individual using a particular method, the notification under paragraph (2)(a) or (b) may use that method.

## [LOW] Entity must comply with direction as soon as practicable

- **Rule ID:** `26WR-9`
- **Docref:** 26WR (10) — [source]()
- **Condition:** `null`
- **Obligation:** An entity must comply with a direction under subsection (1) as soon as practicable after the direction is given.

