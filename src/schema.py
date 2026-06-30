from __future__ import annotations
import re
from typing import Literal
from pydantic import BaseModel, field_validator


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


class PrivacyAppsFacts(BaseModel):
    entity_type: Literal[
        "app_entity", "small_business", "contracted_service_provider", "employee_record_exempt"
    ] = "app_entity"
    data_category: Literal["sensitive", "health", "financial", "biometric", "general"] = "general"
    purpose: Literal["primary", "secondary", "direct_marketing", "law_enforcement"] = "primary"
    consent_given: bool = False
    individual_requested_access: bool = False
    cross_border_disclosure: bool = False
    overseas_recipient_oecd_comparable: bool = False


class SsaBereavementFacts(BaseModel):
    payment_type: Literal[
        "bereavement_allowance", "austudy", "youth_allowance", "age_pension", "carer_payment"
    ] = "age_pension"
    relationship_to_deceased: Literal["partner", "carer", "dependent_child"] = "partner"
    claimant_notified_centrelink: bool = False
    within_notification_period: bool = False


class RuleResult(BaseModel):
    rule_id: str
    matched: bool | None     # None = low codifiability, excluded from engine
    codifiability: Literal["high", "medium", "low"]
    label: str
    obligation: str
    docref: Docref
    matched_facts: dict[str, object] | None = None


class CompareRequest(BaseModel):
    domain: Literal["ndb", "eu-ai-act"]
    section_id: str

    @field_validator("section_id")
    @classmethod
    def section_id_safe(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9-]+$", v):
            raise ValueError("section_id must be alphanumeric/hyphen only")
        return v


class ComparisonResult(BaseModel):
    domain: str
    section_id: str
    plain_rules: list[Rule]
    akn_rules: list[Rule]
