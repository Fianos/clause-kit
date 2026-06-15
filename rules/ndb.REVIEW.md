# ndb — Extraction Review

*54 rules extracted. Review JSON Logic conditions before committing.*

## [LOW] Eligible data breach definition

- **Rule ID:** `26WA-eligible-data-breach-definition`
- **Docref:** 26WA Guide to this Part — [source](https://www.legislation.gov.au/Details/C2022C00099)
- **Condition:** `{"and": [{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure", "loss"]]}]}`
- **Obligation:** An eligible data breach happens if there is unauthorised access to, unauthorised disclosure of, or loss of, personal information held by an entity, and the access, disclosure or loss is likely to result in serious harm to any of the individuals to whom the information relates.

## [LOW] Obligation to notify eligible data breach

- **Rule ID:** `26WA-notification-obligation`
- **Docref:** 26WA Guide to this Part — [source](https://www.legislation.gov.au/Details/C2022C00099)
- **Condition:** `null`
- **Obligation:** An entity must give a notification if it has reasonable grounds to believe that an eligible data breach has happened, or if it is directed to do so by the Commissioner.

## [LOW] Commissioner may obtain information or documents

- **Rule ID:** `26WA-commissioner-information-power`
- **Docref:** 26WA Guide to this Part — [source](https://www.legislation.gov.au/Details/C2022C00099)
- **Condition:** `null`
- **Obligation:** The Commissioner may obtain information or documents in relation to actual or suspected eligible data breaches.

## [LOW] Entity includes file number recipient

- **Rule ID:** `26WB-entity-definition`
- **Docref:** 26WB 26WB — [source](https://www.legislation.gov.au/Details/C2014A00119)
- **Condition:** `null`
- **Obligation:** For the purposes of this Part, the term 'entity' is to be construed as including a person who is a file number recipient.

## [LOW] Deemed holding of personal information disclosed to overseas recipient

- **Rule ID:** `26WC-1`
- **Docref:** 26WC 26WC(1) — [source](https://www.legislation.gov.au/Details/C2018C00292)
- **Condition:** `null`
- **Obligation:** Where an APP entity has disclosed personal information about individuals to an overseas recipient, APP 8.1 applied to that disclosure, and the overseas recipient holds the information, this Part has effect as if the information were held by the APP entity and the APP entity were required under section 15 not to breach APP 11.1 in relation to the information.

## [LOW] Deemed holding of credit eligibility information disclosed to bodies with no Australian link

- **Rule ID:** `26WC-2`
- **Docref:** 26WC 26WC(2) — [source](https://www.legislation.gov.au/Details/C2018C00292)
- **Condition:** `null`
- **Obligation:** Where a credit provider has disclosed credit eligibility information about individuals to a related body corporate, body or person with no Australian link (under paragraph 21G(3)(b) or (c) or subsection 21M(1)) and that recipient holds the information, this Part has effect as if the information were held by the credit provider and the credit provider were required to comply with subsection 21S(1) in relation to the information.

## [LOW] Exception for My Health Records Act notification

- **Rule ID:** `26WD-1`
- **Docref:** 26WD 26WD — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure", "loss"]]}`
- **Obligation:** This Part (NDB scheme) does not apply in relation to the access, disclosure or loss if it has been, or is required to be, notified under section 75 of the My Health Records Act 2012.

## [LOW] Eligible data breach via unauthorised access or disclosure with likely serious harm

- **Rule ID:** `26WE-2-a-access-disclosure`
- **Docref:** 26WE 26WE(2)(a) — [source](https://www.legislation.gov.au/Details/C2018C00292)
- **Condition:** `{"and": [{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure"]]}]}`
- **Obligation:** Where there is unauthorised access to or unauthorised disclosure of the information and a reasonable person would conclude the access or disclosure would be likely to result in serious harm to any affected individual, this constitutes an eligible data breach and the individual is at risk from it.

## [LOW] Eligible data breach via loss likely to result in unauthorised access/disclosure and serious harm

- **Rule ID:** `26WE-2-b-loss`
- **Docref:** 26WE 26WE(2)(b) — [source](https://www.legislation.gov.au/Details/C2018C00292)
- **Condition:** `{"and": [{"==": [{"var": "incident_type"}, "loss"]}]}`
- **Obligation:** Where information is lost in circumstances where unauthorised access or disclosure is likely to occur and, assuming such access or disclosure occurred, a reasonable person would conclude it would be likely to result in serious harm to any affected individual, this constitutes an eligible data breach and the individual is at risk from it.

## [LOW] Remedial action for access/disclosure prevents eligible data breach

- **Rule ID:** `26WF-1`
- **Docref:** 26WF 26WF(1) — [source](https://www.legislation.gov.au/C2004A03712)
- **Condition:** `{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure"]]}`
- **Obligation:** Where an APP entity takes remedial action in relation to an unauthorised access or disclosure before it results in serious harm, and as a result a reasonable person would conclude the access or disclosure would not be likely to result in serious harm to any affected individual, the access or disclosure is taken never to have been an eligible data breach.

## [LOW] Remedial action for access/disclosure removes notification requirement for particular individual

- **Rule ID:** `26WF-2`
- **Docref:** 26WF 26WF(2) — [source](https://www.legislation.gov.au/C2004A03712)
- **Condition:** `{"in": [{"var": "incident_type"}, ["unauthorised_access", "unauthorised_disclosure"]]}`
- **Obligation:** Where remedial action is taken before serious harm results to a particular individual, and as a result a reasonable person would conclude the access or disclosure would not be likely to result in serious harm to that individual, this Part does not require notifying that individual of the statement contents relating to the access or disclosure.

## [LOW] Remedial action for loss before unauthorised access/disclosure prevents eligible data breach

- **Rule ID:** `26WF-3`
- **Docref:** 26WF 26WF(3) — [source](https://www.legislation.gov.au/C2004A03712)
- **Condition:** `{"==": [{"var": "incident_type"}, "loss"]}`
- **Obligation:** Where a loss of information is covered and the entity takes action before there is any unauthorised access to or disclosure of the information, and as a result there is no unauthorised access or disclosure, the loss is taken never to have been an eligible data breach.

## [LOW] Remedial action for loss after unauthorised access/disclosure prevents eligible data breach

- **Rule ID:** `26WF-4`
- **Docref:** 26WF 26WF(4) — [source](https://www.legislation.gov.au/C2004A03712)
- **Condition:** `{"==": [{"var": "incident_type"}, "loss"]}`
- **Obligation:** Where a loss of information is covered and the entity takes action after unauthorised access or disclosure occurs but before it results in serious harm, and as a result a reasonable person would conclude the access or disclosure would not be likely to result in serious harm to any affected individual, the loss is taken never to have been an eligible data breach.

## [LOW] Remedial action for loss removes notification requirement for particular individual

- **Rule ID:** `26WF-5`
- **Docref:** 26WF 26WF(5) — [source](https://www.legislation.gov.au/C2004A03712)
- **Condition:** `{"==": [{"var": "incident_type"}, "loss"]}`
- **Obligation:** Where a loss is covered and the entity takes action after unauthorised access or disclosure but before serious harm results to a particular individual, and as a result a reasonable person would conclude the access or disclosure would not be likely to result in serious harm to that individual, this Part does not require notifying that individual of the statement contents relating to the loss.

## [LOW] Relevant matters for assessing likelihood of serious harm

- **Rule ID:** `26WG_relevant_matters`
- **Docref:** 26WG 26WG — [source](https://www.legislation.gov.au/Details/C2018C00292)
- **Condition:** `null`
- **Obligation:** In determining whether a reasonable person would conclude that access to or disclosure of information would, or would not, be likely to result in serious harm to affected individuals, have regard to: the kind(s) of information; its sensitivity; whether it is protected by security measures; the likelihood those measures could be overcome; the persons or kinds of persons who have obtained or could obtain the information; where security technology was designed to make information unintelligible, the likelihood that persons with intent to harm could obtain knowledge required to circumvent it; the nature of the harm; and any other relevant matters.

## [LOW] Reasonable and expeditious assessment of suspected eligible data breach

- **Rule ID:** `26WH-2-a`
- **Docref:** 26WH 26WH(2)(a) — [source](https://www.legislation.gov.au/Details/C2017A00012)
- **Condition:** `null`
- **Obligation:** The entity must carry out a reasonable and expeditious assessment of whether there are reasonable grounds to believe that the relevant circumstances amount to an eligible data breach of the entity.

## [MEDIUM] Complete assessment within 30 days

- **Rule ID:** `26WH-2-b`
- **Docref:** 26WH 26WH(2)(b) — [source](https://www.legislation.gov.au/Details/C2017A00012)
- **Condition:** `null`
- **Obligation:** The entity must take all reasonable steps to ensure the assessment is completed within 30 days after becoming aware of the reasonable grounds to suspect an eligible data breach.

## [LOW] Exception for eligible data breaches of other entities

- **Rule ID:** `26WJ-1`
- **Docref:** 26WJ Exception—eligible data breaches of other entities — [source](https://www.legislation.gov.au/Details/C2022C00321)
- **Condition:** `null`
- **Obligation:** Where an entity complies with section 26WH in relation to an eligible data breach, and that same access, disclosure or loss is also an eligible data breach of one or more other entities, section 26WH does not apply in relation to those other entities' eligible data breaches.

## [LOW] Prepare and give statement to Commissioner

- **Rule ID:** `26WK-2`
- **Docref:** 26WK 26WK(2) — [source](/akn/au/act/1988-119/section/26WK)
- **Condition:** `null`
- **Obligation:** The entity must prepare a statement that complies with subsection (3) and give a copy to the Commissioner as soon as practicable after becoming aware that there are reasonable grounds to believe there has been an eligible data breach.

## [LOW] Required content of statement

- **Rule ID:** `26WK-3`
- **Docref:** 26WK 26WK(3) — [source](/akn/au/act/1988-119/section/26WK)
- **Condition:** `null`
- **Obligation:** The statement must set out the identity and contact details of the entity, a description of the eligible data breach, the particular kind or kinds of information concerned, and recommendations about steps individuals should take in response.

## [LOW] Optional inclusion of other affected entities

- **Rule ID:** `26WK-4`
- **Docref:** 26WK 26WK(4) — [source](/akn/au/act/1988-119/section/26WK)
- **Condition:** `null`
- **Obligation:** If the entity has reasonable grounds to believe the breach is also an eligible data breach of one or more other entities, the statement may also set out the identity and contact details of those other entities.

## [LOW] Notify individuals to whom information relates

- **Rule ID:** `26WL-1`
- **Docref:** 26WL 26WL(2)(a) — [source]()
- **Condition:** `null`
- **Obligation:** If practicable to notify each individual to whom the relevant information relates, take reasonable steps to notify the contents of the statement to each of those individuals.

## [LOW] Notify individuals at risk

- **Rule ID:** `26WL-2`
- **Docref:** 26WL 26WL(2)(b) — [source]()
- **Condition:** `null`
- **Obligation:** If it is not practicable to notify each individual to whom the information relates but practicable to notify each individual at risk from the breach, take reasonable steps to notify the contents of the statement to each of those at-risk individuals.

## [LOW] Publish statement where individual notification impracticable

- **Rule ID:** `26WL-3`
- **Docref:** 26WL 26WL(2)(c) — [source]()
- **Condition:** `null`
- **Obligation:** If neither paragraph (2)(a) nor (2)(b) applies, publish a copy of the statement on the entity's website (if any) and take reasonable steps to publicise the contents of the statement.

## [LOW] Timing of notification

- **Rule ID:** `26WL-4`
- **Docref:** 26WL 26WL(3) — [source]()
- **Condition:** `null`
- **Obligation:** The entity must comply with the notification requirement in subsection (2) as soon as practicable after completing the preparation of the statement.

## [LOW] Permitted method of providing statement to individual

- **Rule ID:** `26WL-5`
- **Docref:** 26WL 26WL(4) — [source]()
- **Condition:** `null`
- **Obligation:** Where the entity normally communicates with a particular individual using a particular method, the notification under paragraph (2)(a) or (b) may use that method.

## [LOW] Exception for eligible data breaches of other entities

- **Rule ID:** `26WM-1`
- **Docref:** 26WM 26WM — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** Sections 26WK and 26WL do not apply to other entities where one entity has already complied with those sections in relation to the same access, disclosure or loss that constitutes an eligible data breach of those other entities.

## [LOW] Exception for enforcement related activities

- **Rule ID:** `26WN-enforcement-exception`
- **Docref:** 26WN 26WN — [source](https://www.legislation.gov.au/Details/C2018C00292)
- **Condition:** `null`
- **Obligation:** Paragraph 26WK(3)(d) and section 26WL (notification obligations) do not apply where an enforcement body's CEO believes on reasonable grounds that an eligible data breach has occurred and that compliance would likely prejudice one or more enforcement related activities.

## [LOW] Exception extends to other affected entities

- **Rule ID:** `26WN-extends-to-other-entities`
- **Docref:** 26WN 26WN — [source](https://www.legislation.gov.au/Details/C2018C00292)
- **Condition:** `null`
- **Obligation:** Where the access, disclosure or loss constituting the eligible data breach is also an eligible data breach of one or more other entities, the exception in section 26WN applies in relation to those other entities' eligible data breaches as well.

## [LOW] Definition of secrecy provision

- **Rule ID:** `26WP-1`
- **Docref:** 26WP 26WP(1) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** A 'secrecy provision' means a provision of a law of the Commonwealth (other than the Privacy Act) that prohibits or regulates the use or disclosure of information.

## [LOW] Exception to statement contents where inconsistent with non-prescribed secrecy provision

- **Rule ID:** `26WP-2`
- **Docref:** 26WP 26WP(2) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If compliance with subparagraph 26WK(2)(a)(ii) would be inconsistent with a secrecy provision (other than a prescribed secrecy provision), subsection 26WK(2) does not apply to the extent of the inconsistency.

## [LOW] Exception to notification where inconsistent with non-prescribed secrecy provision

- **Rule ID:** `26WP-3`
- **Docref:** 26WP 26WP(3) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If compliance with section 26WL would be inconsistent with a secrecy provision (other than a prescribed secrecy provision), section 26WL does not apply to the extent of the inconsistency.

## [LOW] Definition of prescribed secrecy provision

- **Rule ID:** `26WP-4`
- **Docref:** 26WP 26WP(4) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** A 'prescribed secrecy provision' means a secrecy provision specified in the regulations.

## [LOW] Prescribed secrecy provisions not treated as authorising use or disclosure

- **Rule ID:** `26WP-5`
- **Docref:** 26WP 26WP(5) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** For the purposes of a prescribed secrecy provision, subparagraph 26WK(2)(a)(ii) and section 26WL are taken not to be provisions that require or authorise the use or disclosure of information.

## [LOW] Exception to statement contents where inconsistent with prescribed secrecy provision

- **Rule ID:** `26WP-6`
- **Docref:** 26WP 26WP(6) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If compliance with subparagraph 26WK(2)(a)(ii) would be inconsistent with a prescribed secrecy provision, subsection 26WK(2) does not apply to the entity in relation to the statement (entirely, not merely to the extent of inconsistency).

## [LOW] Exception to notification where inconsistent with prescribed secrecy provision

- **Rule ID:** `26WP-7`
- **Docref:** 26WP 26WP(7) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If compliance with section 26WL would be inconsistent with a prescribed secrecy provision, section 26WL does not apply to the entity in relation to the statement (entirely, not merely to the extent of inconsistency).

## [LOW] Commissioner may declare exception from notification obligations

- **Rule ID:** `26WQ-1-declaration-power`
- **Docref:** 26WQ 26WQ(1) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** The Commissioner may, by written notice to the entity, declare that sections 26WK and 26WL do not apply, or that subsection 26WL(3) has effect as if requiring compliance within a specified period, where the Commissioner has reasonable grounds to believe (or is so informed by the entity) that an eligible data breach has occurred.

## [LOW] Extension of compliance period limited to reasonable period

- **Rule ID:** `26WQ-2-extension-reasonable`
- **Docref:** 26WQ 26WQ(2) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** The power under paragraph (1)(d) may only be used to extend the time for compliance with subsection 26WL(2) to the end of a period that the Commissioner is satisfied is reasonable in the circumstances.

## [LOW] Declaration only if reasonable having regard to relevant matters

- **Rule ID:** `26WQ-3-declaration-reasonableness`
- **Docref:** 26WQ 26WQ(3) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** The Commissioner must not make a declaration under subsection (1) unless satisfied it is reasonable in the circumstances, having regard to the public interest, any relevant advice from an enforcement body or the Australian Signals Directorate, and such other matters as the Commissioner considers relevant.

## [LOW] Declaration on own initiative or on application

- **Rule ID:** `26WQ-5-notice-initiative-or-application`
- **Docref:** 26WQ 26WQ(5) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** The Commissioner may give notice of a declaration on the Commissioner's own initiative or on application by the entity.

## [LOW] Commissioner may refuse application and must give written notice

- **Rule ID:** `26WQ-7-refusal-notice`
- **Docref:** 26WQ 26WQ(7) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If an entity applies under paragraph (5)(b), the Commissioner may refuse the application and, if so, must give written notice of the refusal to the entity.

## [LOW] Specifying different period is not a refusal

- **Rule ID:** `26WQ-8-different-period-not-refusal`
- **Docref:** 26WQ 26WQ(8) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If an application nominates a period but the Commissioner makes the declaration specifying a different period, the Commissioner is taken not to have refused the application.

## [LOW] Notification obligations suspended pending decision on application

- **Rule ID:** `26WQ-9-suspension-pending-decision`
- **Docref:** 26WQ 26WQ(9) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If an entity applies under paragraph (5)(b) for a declaration relating to an eligible data breach, sections 26WK and 26WL do not apply to that breach (and related breaches of other entities) until the Commissioner makes a decision on the application.

## [LOW] Entity not entitled to apply if another affected entity has already applied

- **Rule ID:** `26WQ-10-no-duplicate-application`
- **Docref:** 26WQ 26WQ(10) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** An entity is not entitled to make an application under paragraph (5)(b) where the same access, disclosure or loss is an eligible data breach of one or more other entities and one of those other entities has already made an application under paragraph (5)(b).

## [LOW] Commissioner may extend specified period

- **Rule ID:** `26WQ-11-extension-of-period`
- **Docref:** 26WQ 26WQ(11) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If notice of a paragraph (1)(d) declaration has been given, the Commissioner may, by written notice to the entity, extend the period specified in the declaration.

## [LOW] Commissioner may direct entity to prepare and provide statement

- **Rule ID:** `26WR-1-direction-power`
- **Docref:** 26WR 26WR(1) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If the Commissioner is aware of reasonable grounds to believe there has been an eligible data breach, the Commissioner may by written notice direct the entity to prepare a compliant statement and give a copy to the Commissioner.

## [LOW] Direction must require notification or publication of statement

- **Rule ID:** `26WR-2-notification-method-required`
- **Docref:** 26WR 26WR(2) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** The direction must require the entity to notify the statement contents to affected individuals (if practicable), or to at-risk individuals (if practicable), or otherwise to publish the statement on its website and take reasonable steps to publicise it.

## [LOW] Commissioner must invite submission before giving direction

- **Rule ID:** `26WR-3-invite-submission`
- **Docref:** 26WR 26WR(3) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** Before giving a direction under subsection (1), the Commissioner must invite the entity to make a submission within the specified period.

## [MEDIUM] Required contents of statement

- **Rule ID:** `26WR-4-statement-contents`
- **Docref:** 26WR 26WR(4) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** The statement must set out the entity's identity and contact details, a description of the eligible data breach, the kind(s) of information concerned, and recommendations about steps individuals should take.

## [LOW] Direction may require additional specified information in statement

- **Rule ID:** `26WR-5-additional-specified-info`
- **Docref:** 26WR 26WR(5) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** A direction may require the statement to set out specified information relating to the eligible data breach.

## [LOW] Commissioner must have regard to relevant matters

- **Rule ID:** `26WR-6-relevant-considerations`
- **Docref:** 26WR 26WR(6) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** In deciding whether to give a direction, the Commissioner must have regard to relevant advice from enforcement bodies or the Australian Signals Directorate, any relevant submission from the entity, and any other relevant matters.

## [LOW] Direction may require identification of other affected entities

- **Rule ID:** `26WR-8-multiple-entities`
- **Docref:** 26WR 26WR(8) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If the Commissioner has reasonable grounds to believe the breach is also an eligible data breach of other entities, the direction may require the statement to set out the identity and contact details of those other entities.

## [LOW] Notification may use normal communication method

- **Rule ID:** `26WR-9-notification-method`
- **Docref:** 26WR 26WR(9) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** If an entity normally communicates with an individual using a particular method, notification under 26WR(2)(a) or (b) may use that method.

## [LOW] Entity must comply with direction as soon as practicable

- **Rule ID:** `26WR-10-comply-asap`
- **Docref:** 26WR 26WR(10) — [source](https://www.legislation.gov.au/Details/C2022C00361)
- **Condition:** `null`
- **Obligation:** An entity must comply with a direction under subsection (1) as soon as practicable after the direction is given.

