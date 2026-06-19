from __future__ import annotations
from typing import Literal
from pydantic import BaseModel


class Docref(BaseModel):
    source_doc: str
    article: str
    section: str
    url: str
    provision_uri: str | None = None  # AKN FRBR URI (AU) or ELI URI (EU)


class Rule(BaseModel):
    rule_id: str
    label: str
    condition: dict | None
    obligation: str
    scope: str
    exceptions: list[str]
    codifiability: Literal["high", "medium", "low"]
    docref: Docref


class Scenario(BaseModel):
    id: str
    label: str
    description: str
    facts: dict


class DomainFile(BaseModel):
    domain: str
    version: str
    extracted_at: str
    source_url: str
    model_version: str | None = None
    rules: list[Rule]
    scenarios: list[Scenario]


class EuAiActFacts(BaseModel):
    system_name: str = ""
    deployment_sector: Literal[
        "employment", "education", "credit", "law_enforcement",
        "border", "critical_infra", "biometric_id", "general"
    ] = "general"
    publicly_accessible_spaces: bool = False
    involves_safety_component: bool = False
    is_gpai_model: bool = False
    real_time_biometric: bool = False
    post_hoc_biometric: bool = False
    art6_3_exception_narrow_procedure: bool = False
    art6_3_exception_human_override: bool = False
    art6_3_exception_preparatory_task: bool = False
    art6_3_exception_contravention_check: bool = False


class NdbFacts(BaseModel):
    incident_type: Literal["unauthorised_access", "loss", "unauthorised_disclosure"] = "unauthorised_access"
    data_categories: list[Literal["health", "financial", "identity", "biometric", "sensitive"]] = []
    encryption_status: Literal["encrypted", "partial", "unencrypted"] = "encrypted"
    individuals_affected: Literal["1-10", "10-100", "100-1000", "1000+"] = "1-10"
    likely_recipient: Literal["unknown", "specific_individual", "criminal", "broad_public"] = "unknown"
    individual_vulnerability: Literal["general", "elderly", "children", "health_patients"] = "general"


class RuleResult(BaseModel):
    rule_id: str
    matched: bool | None     # None = low codifiability, excluded from engine
    codifiability: Literal["high", "medium", "low"]
    label: str
    obligation: str
    docref: Docref
