# eu-ai-act — Extraction Review

*32 rules extracted. Review JSON Logic conditions before committing.*

## [LOW] Prohibition of subliminal/manipulative/deceptive AI causing significant harm

- **Rule ID:** `art5_1_a_subliminal_manipulation`
- **Docref:** Article 5 1(a) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `null`
- **Obligation:** The placing on the market, putting into service or use of an AI system that deploys subliminal, purposefully manipulative or deceptive techniques materially distorting behaviour and causing significant harm is prohibited.

## [LOW] Prohibition of exploiting vulnerabilities (age, disability, social/economic situation)

- **Rule ID:** `art5_1_b_exploitation_vulnerabilities`
- **Docref:** Article 5 1(b) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `null`
- **Obligation:** The placing on the market, putting into service or use of an AI system exploiting vulnerabilities due to age, disability or social/economic situation to materially distort behaviour causing significant harm is prohibited.

## [LOW] Prohibition of social scoring leading to detrimental treatment

- **Rule ID:** `art5_1_c_social_scoring`
- **Docref:** Article 5 1(c) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `null`
- **Obligation:** The placing on the market, putting into service or use of AI systems for social scoring of natural persons leading to unjustified or disproportionate detrimental treatment is prohibited.

## [MEDIUM] Prohibition of crime risk prediction based solely on profiling

- **Rule ID:** `art5_1_d_predictive_policing_profiling`
- **Docref:** Article 5 1(d) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "law_enforcement"]}`
- **Obligation:** The placing on the market, putting into service or use of an AI system to assess/predict the risk of a natural person committing a criminal offence based solely on profiling or personality traits is prohibited.

## [HIGH] Prohibition of facial recognition database creation via untargeted scraping

- **Rule ID:** `art5_1_e_facial_scraping`
- **Docref:** Article 5 1(e) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `null`
- **Obligation:** The placing on the market, putting into service or use of AI systems that create or expand facial recognition databases through untargeted scraping of facial images from the internet or CCTV footage is prohibited.

## [MEDIUM] Prohibition of emotion inference in workplace and education

- **Rule ID:** `art5_1_f_emotion_recognition_work_education`
- **Docref:** Article 5 1(f) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"in": [{"var": "deployment_sector"}, ["employment", "education"]]}`
- **Obligation:** The placing on the market, putting into service or use of AI systems to infer emotions of natural persons in the workplace and education institutions is prohibited.

## [MEDIUM] Prohibition of biometric categorisation inferring sensitive attributes

- **Rule ID:** `art5_1_g_biometric_categorisation_sensitive`
- **Docref:** Article 5 1(g) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "biometric_id"]}`
- **Obligation:** The placing on the market, putting into service or use of biometric categorisation systems that categorise natural persons based on biometric data to deduce race, political opinions, trade union membership, religious or philosophical beliefs, sex life or sexual orientation is prohibited.

## [MEDIUM] Prohibition of real-time remote biometric identification in public spaces for law enforcement

- **Rule ID:** `art5_1_h_realtime_biometric_le`
- **Docref:** Article 5 1(h) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"and": [{"==": [{"var": "real_time_biometric"}, true]}, {"==": [{"var": "publicly_accessible_spaces"}, true]}, {"==": [{"var": "deployment_sector"}, "law_enforcement"]}]}`
- **Obligation:** The use of real-time remote biometric identification systems in publicly accessible spaces for law enforcement is prohibited unless strictly necessary for one of the enumerated objectives (targeted search for victims, prevention of substantial imminent threat/terrorist attack, localisation of suspects of serious offences).

## [MEDIUM] Conditions and safeguards for permitted real-time biometric identification use

- **Rule ID:** `art5_2_realtime_biometric_safeguards`
- **Docref:** Article 5 2 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"and": [{"==": [{"var": "real_time_biometric"}, true]}, {"==": [{"var": "publicly_accessible_spaces"}, true]}, {"==": [{"var": "deployment_sector"}, "law_enforcement"]}]}`
- **Obligation:** Use must be limited to confirming the identity of a specifically targeted individual, take into account the nature of the situation and consequences, comply with necessary and proportionate safeguards, and only be authorised after a fundamental rights impact assessment (Article 27) and registration in the EU database (Article 49), with urgent cases allowing deferred registration.

## [MEDIUM] Prior judicial/administrative authorisation for real-time biometric identification

- **Rule ID:** `art5_3_realtime_biometric_prior_authorisation`
- **Docref:** Article 5 3 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"and": [{"==": [{"var": "real_time_biometric"}, true]}, {"==": [{"var": "publicly_accessible_spaces"}, true]}, {"==": [{"var": "deployment_sector"}, "law_enforcement"]}]}`
- **Obligation:** Each use must be subject to prior authorisation by a judicial or independent administrative authority upon reasoned request; in urgent cases use may commence without authorisation provided it is requested within 24 hours, and if rejected use must stop immediately and all data discarded.

## [MEDIUM] High-risk classification: safety component under Annex I with third-party conformity assessment

- **Rule ID:** `art6_1_safety_component_highrisk`
- **Docref:** 6 1 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `{"and": [{"==": [{"var": "involves_safety_component"}, true]}, {"==": [{"var": "involves_safety_component"}, true]}]}`
- **Obligation:** An AI system intended to be used as a safety component of a product (or that is itself a product) covered by Union harmonisation legislation listed in Annex I, where that product is required to undergo a third-party conformity assessment, shall be considered high-risk.

## [MEDIUM] High-risk classification: Annex III systems

- **Rule ID:** `art6_2_annex3_highrisk`
- **Docref:** 6 2 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `{"in": [{"var": "deployment_sector"}, ["employment", "education", "credit", "law_enforcement", "border", "critical_infra", "biometric_id"]]}`
- **Obligation:** AI systems referred to in Annex III shall be considered to be high-risk, in addition to those under paragraph 1.

## [MEDIUM] Derogation: Annex III system not high-risk where no significant risk

- **Rule ID:** `art6_3_derogation_not_highrisk`
- **Docref:** 6 3 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `{"and": [{"in": [{"var": "deployment_sector"}, ["employment", "education", "credit", "law_enforcement", "border", "critical_infra", "biometric_id"]]}, {"or": [{"==": [{"var": "art6_3_exception_narrow_procedure"}, true]}, {"==": [{"var": "art6_3_exception_preparatory_task"}, true]}, {"==": [{"var": "art6_3_exception_human_override"}, true]}, {"==": [{"var": "art6_3_exception_contravention_check"}, true]}]}]}`
- **Obligation:** By derogation from paragraph 2, an Annex III AI system shall not be considered high-risk where it does not pose a significant risk of harm and meets one of the listed conditions (narrow procedural task, improving a completed human activity, detecting deviations without replacing human assessment, or performing a preparatory task).

## [LOW] Profiling override: always high-risk

- **Rule ID:** `art6_3_profiling_always_highrisk`
- **Docref:** 6 3 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `null`
- **Obligation:** Notwithstanding the derogation, an Annex III AI system shall always be considered high-risk where it performs profiling of natural persons.

## [MEDIUM] Provider documentation of non-high-risk assessment

- **Rule ID:** `art6_4_documentation_obligation`
- **Docref:** 6 4 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `{"in": [{"var": "deployment_sector"}, ["employment", "education", "credit", "law_enforcement", "border", "critical_infra", "biometric_id"]]}`
- **Obligation:** A provider who considers that an Annex III AI system is not high-risk shall document its assessment before placing on the market or putting into service, shall comply with the registration obligation in Article 49(2), and shall provide the documentation to national competent authorities upon request.

## [LOW] Commission guidelines on implementation

- **Rule ID:** `art6_5_commission_guidelines`
- **Docref:** 6 5 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `null`
- **Obligation:** The Commission shall, after consulting the Board and no later than 2 February 2026, provide guidelines specifying the practical implementation of this Article together with a comprehensive list of practical examples of high-risk and non-high-risk use cases.

## [LOW] Commission delegated acts to add/modify derogation conditions

- **Rule ID:** `art6_6_delegated_acts_add`
- **Docref:** 6 6 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `null`
- **Obligation:** The Commission is empowered to adopt delegated acts to amend paragraph 3, second subparagraph, by adding or modifying conditions where there is concrete and reliable evidence of Annex III systems that do not pose a significant risk of harm.

## [LOW] Commission delegated acts to delete derogation conditions

- **Rule ID:** `art6_7_delegated_acts_delete`
- **Docref:** 6 7 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `null`
- **Obligation:** The Commission shall adopt delegated acts to amend paragraph 3, second subparagraph, by deleting any condition where there is concrete and reliable evidence necessary to maintain the level of protection of health, safety and fundamental rights.

## [LOW] Constraints on amendments to derogation conditions

- **Rule ID:** `art6_8_amendment_constraints`
- **Docref:** 6 8 — [source](http://data.europa.eu/eli/reg/2024/1689/art_6)
- **Condition:** `null`
- **Obligation:** Any amendment to the conditions under paragraphs 6 and 7 shall not decrease the overall level of protection of health, safety and fundamental rights, shall ensure consistency with delegated acts under Article 7(1), and shall take account of market and technological developments.

## [LOW] Union harmonisation legislation based on New Legislative Framework (Section A)

- **Rule ID:** `annex_1_nlf_harmonisation_list`
- **Docref:** Annex I Section A — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"==": [{"var": "involves_safety_component"}, true]}`
- **Obligation:** An AI system intended as a safety component of, or itself a product covered by, the Union harmonisation legislation listed in Annex I Section A (machinery, toys, recreational craft, lifts, ATEX equipment, radio equipment, pressure equipment, cableway installations, PPE, gas appliances, medical devices, in vitro diagnostic medical devices) is treated as high-risk under Article 6(1) when conformity assessment is required.

## [LOW] Other Union harmonisation legislation (Section B)

- **Rule ID:** `annex_1_other_harmonisation_list`
- **Docref:** Annex I Section B — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"==": [{"var": "involves_safety_component"}, true]}`
- **Obligation:** An AI system intended as a safety component of, or itself a product covered by, the Union harmonisation legislation listed in Annex I Section B (civil aviation security, two/three-wheel vehicles, agricultural/forestry vehicles, marine equipment, rail interoperability, motor vehicles type-approval, general vehicle safety, civil aviation/EASA for unmanned aircraft) is treated as high-risk under Article 6(1) when conformity assessment is required.

## [HIGH] Remote biometric identification systems are high-risk

- **Rule ID:** `annex3_1a_remote_biometric_id`
- **Docref:** Annex III 1(a) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"and": [{"==": [{"var": "deployment_sector"}, "biometric_id"]}, {"or": [{"==": [{"var": "real_time_biometric"}, true]}, {"==": [{"var": "post_hoc_biometric"}, true]}]}]}`
- **Obligation:** AI systems used as remote biometric identification systems are classified as high-risk under Annex III, in so far as their use is permitted under relevant Union or national law.

## [MEDIUM] Biometric categorisation by sensitive attributes is high-risk

- **Rule ID:** `annex3_1b_biometric_categorisation`
- **Docref:** Annex III 1(b) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "biometric_id"]}`
- **Obligation:** AI systems intended to be used for biometric categorisation according to sensitive or protected attributes based on inference are high-risk, in so far as permitted under Union or national law.

## [MEDIUM] Emotion recognition systems are high-risk

- **Rule ID:** `annex3_1c_emotion_recognition`
- **Docref:** Annex III 1(c) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "biometric_id"]}`
- **Obligation:** AI systems intended to be used for emotion recognition are high-risk, in so far as permitted under Union or national law.

## [HIGH] Critical infrastructure safety components are high-risk

- **Rule ID:** `annex3_2_critical_infrastructure`
- **Docref:** Annex III 2 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"and": [{"==": [{"var": "deployment_sector"}, "critical_infra"]}, {"==": [{"var": "involves_safety_component"}, true]}]}`
- **Obligation:** AI systems intended to be used as safety components in the management and operation of critical digital infrastructure, road traffic, or supply of water, gas, heating or electricity are high-risk.

## [HIGH] Education and vocational training AI systems are high-risk

- **Rule ID:** `annex3_3_education`
- **Docref:** Annex III 3 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "education"]}`
- **Obligation:** AI systems used to determine access/admission, assign persons to institutions, evaluate learning outcomes, assess appropriate level of education, or monitor prohibited behaviour during tests in educational and vocational training institutions are high-risk.

## [HIGH] Employment and worker management AI systems are high-risk

- **Rule ID:** `annex3_4_employment`
- **Docref:** Annex III 4 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "employment"]}`
- **Obligation:** AI systems used for recruitment/selection, or to make decisions affecting terms of work-related relationships, promotion/termination, task allocation based on traits, or monitoring/evaluating performance are high-risk.

## [HIGH] Creditworthiness evaluation AI systems are high-risk

- **Rule ID:** `annex3_5b_creditworthiness`
- **Docref:** Annex III 5(b) — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "credit"]}`
- **Obligation:** AI systems intended to evaluate creditworthiness of natural persons or establish their credit score are high-risk.

## [HIGH] Law enforcement AI systems are high-risk

- **Rule ID:** `annex3_6_law_enforcement`
- **Docref:** Annex III 6 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "law_enforcement"]}`
- **Obligation:** AI systems used by or on behalf of law enforcement for victim risk assessment, polygraphs, evidence reliability evaluation, offending/re-offending risk assessment, or profiling are high-risk, in so far as permitted under Union or national law.

## [HIGH] Migration, asylum and border control AI systems are high-risk

- **Rule ID:** `annex3_7_migration_border`
- **Docref:** Annex III 7 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `{"==": [{"var": "deployment_sector"}, "border"]}`
- **Obligation:** AI systems used by competent public authorities for polygraphs, risk assessment of persons entering the territory, examination of asylum/visa/residence applications, or detecting/identifying persons in migration/border contexts are high-risk, in so far as permitted under Union or national law.

## [LOW] Essential public/private services and benefits AI systems are high-risk

- **Rule ID:** `annex3_5_essential_services_general`
- **Docref:** Annex III 5 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `null`
- **Obligation:** AI systems used by public authorities to evaluate eligibility for essential public assistance benefits, to evaluate creditworthiness, for risk assessment and pricing of life/health insurance, or to evaluate/dispatch emergency calls and first response services are high-risk.

## [LOW] Administration of justice and democratic processes AI systems are high-risk

- **Rule ID:** `annex3_8_justice_democratic`
- **Docref:** Annex III 8 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689)
- **Condition:** `null`
- **Obligation:** AI systems used to assist judicial authorities in researching/interpreting facts and applying law (or in ADR), or to influence the outcome of elections/referenda or voting behaviour, are high-risk.

