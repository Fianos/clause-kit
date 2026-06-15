# eu-ai-act — Extraction Review

*27 rules extracted. Signed off 2026-06-15 with the following known issues for future correction:*

## Known Issues

1. **Art 5 docref URLs are empty** — `art5_1_*` rules have blank `source` links. All Art 6 and Annex rules have the correct EUR-Lex URL. Fix: add `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#art_5` to Art 5 docrefs in `eu-ai-act.json`.

2. **`annex3_5_essential_services` and `annex3_8_justice_democracy` use `deployment_sector == "general"`** — These cover public benefit systems, water/electricity utilities, courts, and elections, which the fact schema doesn't have specific values for. Mapped to "general" as the least-wrong option. In the sandbox, selecting "General purpose" will incorrectly trigger these. Future fix: add `public_services` and `justice` enum values to `deployment_sector`.

3. **Emotion recognition (annex3_1c) mapped to `biometric_id` sector** — Annex III 1(c) covers emotion recognition broadly, not just biometric identification. The `biometric_id` mapping is narrower than the statute. Medium-risk error for the demo.

4. **Art 5(1)(h) condition requires `deployment_sector == "law_enforcement"`** — Correct per the statute (prohibition applies specifically to law enforcement use of real-time biometric ID). The sandbox scenario "Facial recognition (public space)" should use `deployment_sector: biometric_id` — it won't trigger Art 5(1)(h) unless sector is also set to `law_enforcement`.

## [LOW] Prohibition of subliminal or manipulative/deceptive AI techniques

- **Rule ID:** `art5_1_a_subliminal_manipulation`
- **Docref:** Article 5 1(a) — [source]()
- **Condition:** `null`
- **Obligation:** An AI system that deploys subliminal, purposefully manipulative, or deceptive techniques that materially distort behaviour and are reasonably likely to cause significant harm shall not be placed on the market, put into service, or used.

## [LOW] Prohibition of exploitation of vulnerabilities

- **Rule ID:** `art5_1_b_exploitation_vulnerabilities`
- **Docref:** Article 5 1(b) — [source]()
- **Condition:** `null`
- **Obligation:** An AI system that exploits vulnerabilities due to age, disability, or a specific social or economic situation to materially distort behaviour in a manner likely to cause significant harm shall not be placed on the market, put into service, or used.

## [LOW] Prohibition of social scoring

- **Rule ID:** `art5_1_c_social_scoring`
- **Docref:** Article 5 1(c) — [source]()
- **Condition:** `null`
- **Obligation:** AI systems for evaluation or classification of persons based on social behaviour or personal characteristics leading to unjustified/disproportionate or out-of-context detrimental treatment shall not be placed on market, put into service, or used.

## [LOW] Prohibition of individual criminal risk assessment based solely on profiling

- **Rule ID:** `art5_1_d_predictive_policing_profiling`
- **Docref:** Article 5 1(d) — [source]()
- **Condition:** `null`
- **Obligation:** AI systems for assessing or predicting the risk of a person committing a criminal offence based solely on profiling or personality traits shall not be placed on market, put into service, or used.

## [MEDIUM] Prohibition of untargeted facial image scraping

- **Rule ID:** `art5_1_e_facial_scraping`
- **Docref:** Article 5 1(e) — [source]()
- **Condition:** `null`
- **Obligation:** AI systems that create or expand facial recognition databases through untargeted scraping of facial images from the internet or CCTV footage shall not be placed on market, put into service, or used.

## [MEDIUM] Prohibition of emotion inference in workplace and education

- **Rule ID:** `art5_1_f_emotion_recognition_work_education`
- **Docref:** Article 5 1(f) — [source]()
- **Condition:** `{"in": [{"var": "deployment_sector"}, ["employment", "education"]]}`
- **Obligation:** AI systems to infer emotions of natural persons in workplace and education institutions shall not be placed on market, put into service, or used.

## [MEDIUM] Prohibition of biometric categorisation inferring sensitive attributes

- **Rule ID:** `art5_1_g_biometric_categorisation_sensitive`
- **Docref:** Article 5 1(g) — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "biometric_id"]}`
- **Obligation:** Biometric categorisation systems that deduce or infer race, political opinions, trade union membership, religious/philosophical beliefs, sex life, or sexual orientation shall not be placed on market, put into service, or used.

## [MEDIUM] Prohibition of real-time remote biometric ID in public spaces for law enforcement

- **Rule ID:** `art5_1_h_realtime_biometric_le`
- **Docref:** Article 5 1(h) — [source]()
- **Condition:** `{"and": [{"==": [{"var": "real_time_biometric"}, true]}, {"==": [{"var": "publicly_accessible_spaces"}, true]}, {"==": [{"var": "deployment_sector"}, "law_enforcement"]}]}`
- **Obligation:** Use of real-time remote biometric identification systems in publicly accessible spaces for law enforcement is prohibited unless strictly necessary for an exhaustively listed objective (targeted search for victims, prevention of substantial imminent threat/terrorist attack, or localisation of a suspect for serious offences in Annex II).

## [MEDIUM] Conditions for permitted real-time biometric ID use (FRIA and registration)

- **Rule ID:** `art5_2_realtime_biometric_safeguards`
- **Docref:** Article 5 2 — [source]()
- **Condition:** `{"and": [{"==": [{"var": "real_time_biometric"}, true]}, {"==": [{"var": "publicly_accessible_spaces"}, true]}, {"==": [{"var": "deployment_sector"}, "law_enforcement"]}]}`
- **Obligation:** Permitted use must confirm identity of a specifically targeted individual, account for the nature/consequences of the situation, comply with necessary and proportionate safeguards under national law, and only be authorised after completing a fundamental rights impact assessment (Article 27) and registering the system in the EU database (Article 49); in urgent cases registration may be completed without undue delay.

## [HIGH] Prior judicial/administrative authorisation for real-time biometric ID use

- **Rule ID:** `art5_3_realtime_biometric_prior_authorisation`
- **Docref:** Article 5 3 — [source]()
- **Condition:** `{"and": [{"==": [{"var": "real_time_biometric"}, true]}, {"==": [{"var": "publicly_accessible_spaces"}, true]}, {"==": [{"var": "deployment_sector"}, "law_enforcement"]}]}`
- **Obligation:** Each law enforcement use requires prior authorisation by a judicial or independent administrative authority upon reasoned request; in urgency, use may begin without authorisation provided it is requested within 24 hours, and if rejected use must stop immediately and all data/results discarded.

## [MEDIUM] High-risk classification via Annex I safety component requiring third-party conformity assessment

- **Rule ID:** `art6_1_safety_component_highrisk`
- **Docref:** Article 6 1 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"and": [{"==": [{"var": "involves_safety_component"}, true]}]}`
- **Obligation:** An AI system intended to be used as a safety component of a product (or which is itself a product) covered by Union harmonisation legislation in Annex I, and required to undergo third-party conformity assessment, shall be considered high-risk.

## [MEDIUM] High-risk classification for Annex III systems

- **Rule ID:** `art6_2_annex_iii_highrisk`
- **Docref:** Article 6 2 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"in": [{"var": "deployment_sector"}, ["employment", "education", "credit", "law_enforcement", "border", "critical_infra", "biometric_id"]]}`
- **Obligation:** AI systems referred to in Annex III shall be considered high-risk.

## [MEDIUM] Derogation: Annex III system not high-risk if it meets an exception and does not perform profiling

- **Rule ID:** `art6_3_derogation_not_highrisk`
- **Docref:** Article 6 3 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"and": [{"in": [{"var": "deployment_sector"}, ["employment", "education", "credit", "law_enforcement", "border", "critical_infra", "biometric_id"]]}, {"or": [{"==": [{"var": "art6_3_exception_narrow_procedure"}, true]}, {"==": [{"var": "art6_3_exception_human_override"}, true]}, {"==": [{"var": "art6_3_exception_contravention_check"}, true]}, {"==": [{"var": "art6_3_exception_preparatory_task"}, true]}]}]}`
- **Obligation:** An Annex III AI system shall not be considered high-risk where it does not pose a significant risk of harm and fulfils one of the listed conditions (narrow procedural task, improving a completed human activity, detecting deviations without replacing human assessment, or preparatory task), unless it performs profiling of natural persons.

## [LOW] Profiling always renders Annex III system high-risk

- **Rule ID:** `art6_3_profiling_always_highrisk`
- **Docref:** Article 6 3 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `null`
- **Obligation:** Notwithstanding the derogation conditions, an Annex III AI system shall always be considered high-risk where it performs profiling of natural persons.

## [LOW] Provider must document non-high-risk assessment and register

- **Rule ID:** `art6_4_document_non_highrisk_assessment`
- **Docref:** Article 6 4 — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `null`
- **Obligation:** A provider who considers that an Annex III AI system is not high-risk shall document its assessment before placing on the market or putting into service, comply with the registration obligation in Article 49(2), and provide the documentation to national competent authorities upon request.

## [MEDIUM] AI system as safety component under Annex I harmonisation legislation

- **Rule ID:** `annex_i_harmonisation_safety_component`
- **Docref:** Annex I Sections A and B — [source](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- **Condition:** `{"==": [{"var": "involves_safety_component"}, true]}`
- **Obligation:** An AI system intended to be used as a safety component of a product, or which is itself a product, covered by the Union harmonisation legislation listed in Annex I is subject to the high-risk classification and conformity requirements of this Regulation.

## [HIGH] Remote biometric identification systems are high-risk

- **Rule ID:** `annex3_1a_remote_biometric_id`
- **Docref:** Annex III 1(a) — [source]()
- **Condition:** `{"and": [{"==": [{"var": "deployment_sector"}, "biometric_id"]}, {"or": [{"==": [{"var": "real_time_biometric"}, true]}, {"==": [{"var": "post_hoc_biometric"}, true]}]}]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [LOW] Biometric categorisation by sensitive attributes is high-risk

- **Rule ID:** `annex3_1b_biometric_categorisation`
- **Docref:** Annex III 1(b) — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "biometric_id"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [LOW] Emotion recognition systems are high-risk

- **Rule ID:** `annex3_1c_emotion_recognition`
- **Docref:** Annex III 1(c) — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "biometric_id"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [HIGH] AI safety components in critical infrastructure are high-risk

- **Rule ID:** `annex3_2_critical_infrastructure`
- **Docref:** Annex III 2 — [source]()
- **Condition:** `{"and": [{"==": [{"var": "deployment_sector"}, "critical_infra"]}, {"==": [{"var": "involves_safety_component"}, true]}]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [HIGH] Education and vocational training AI systems are high-risk

- **Rule ID:** `annex3_3_education`
- **Docref:** Annex III 3 — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "education"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [HIGH] Employment and worker management AI systems are high-risk

- **Rule ID:** `annex3_4_employment`
- **Docref:** Annex III 4 — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "employment"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [HIGH] Creditworthiness/credit scoring AI systems are high-risk

- **Rule ID:** `annex3_5b_creditworthiness`
- **Docref:** Annex III 5(b) — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "credit"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [LOW] Essential public/private services AI systems are high-risk

- **Rule ID:** `annex3_5_essential_services`
- **Docref:** Annex III 5 — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "general"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [HIGH] Law enforcement AI systems are high-risk

- **Rule ID:** `annex3_6_law_enforcement`
- **Docref:** Annex III 6 — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "law_enforcement"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [HIGH] Migration, asylum and border control AI systems are high-risk

- **Rule ID:** `annex3_7_border`
- **Docref:** Annex III 7 — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "border"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

## [LOW] Administration of justice and democratic processes AI systems are high-risk

- **Rule ID:** `annex3_8_justice_democracy`
- **Docref:** Annex III 8 — [source]()
- **Condition:** `{"==": [{"var": "deployment_sector"}, "general"]}`
- **Obligation:** Classified as high-risk AI system subject to Chapter III requirements

