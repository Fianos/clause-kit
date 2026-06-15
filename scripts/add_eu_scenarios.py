import json
from pathlib import Path

path = Path("rules/eu-ai-act.json")
data = json.loads(path.read_text())

data["scenarios"] = [
    {
        "id": "hr-screening",
        "label": "HR screening tool",
        "description": "AI ranks job applicants by predicted suitability for a role",
        "facts": {
            "system_name": "HR Screener v2",
            "deployment_sector": "employment",
            "publicly_accessible_spaces": False,
            "involves_safety_component": False,
            "is_gpai_model": False,
            "real_time_biometric": False,
            "post_hoc_biometric": False,
            "art6_3_exception_narrow_procedure": False,
            "art6_3_exception_human_override": False,
            "art6_3_exception_preparatory_task": False,
            "art6_3_exception_contravention_check": False,
        },
    },
    {
        "id": "credit-scoring",
        "label": "Creditworthiness assessment",
        "description": "AI assesses creditworthiness for consumer loan applications",
        "facts": {
            "system_name": "CreditAI",
            "deployment_sector": "credit",
            "publicly_accessible_spaces": False,
            "involves_safety_component": False,
            "is_gpai_model": False,
            "real_time_biometric": False,
            "post_hoc_biometric": False,
            "art6_3_exception_narrow_procedure": False,
            "art6_3_exception_human_override": False,
            "art6_3_exception_preparatory_task": False,
            "art6_3_exception_contravention_check": False,
        },
    },
    {
        "id": "facial-recognition-public",
        "label": "Facial recognition (public space)",
        "description": "Real-time biometric identification by law enforcement in a publicly accessible shopping centre",
        "facts": {
            "system_name": "FaceID Pro",
            "deployment_sector": "law_enforcement",
            "publicly_accessible_spaces": True,
            "involves_safety_component": False,
            "is_gpai_model": False,
            "real_time_biometric": True,
            "post_hoc_biometric": False,
            "art6_3_exception_narrow_procedure": False,
            "art6_3_exception_human_override": False,
            "art6_3_exception_preparatory_task": False,
            "art6_3_exception_contravention_check": False,
        },
    },
    {
        "id": "art6-3-exception",
        "label": "Narrow procedural task (Art 6(3))",
        "description": "HR system claiming Article 6(3) exception — performs a narrow preparatory task only, with human override",
        "facts": {
            "system_name": "HR PreScreener",
            "deployment_sector": "employment",
            "publicly_accessible_spaces": False,
            "involves_safety_component": False,
            "is_gpai_model": False,
            "real_time_biometric": False,
            "post_hoc_biometric": False,
            "art6_3_exception_narrow_procedure": True,
            "art6_3_exception_human_override": True,
            "art6_3_exception_preparatory_task": True,
            "art6_3_exception_contravention_check": False,
        },
    },
    {
        "id": "customer-service-chatbot",
        "label": "Customer service chatbot",
        "description": "General-purpose customer support assistant, no high-risk use case",
        "facts": {
            "system_name": "SupportBot",
            "deployment_sector": "general",
            "publicly_accessible_spaces": False,
            "involves_safety_component": False,
            "is_gpai_model": False,
            "real_time_biometric": False,
            "post_hoc_biometric": False,
            "art6_3_exception_narrow_procedure": False,
            "art6_3_exception_human_override": False,
            "art6_3_exception_preparatory_task": False,
            "art6_3_exception_contravention_check": False,
        },
    },
]

path.write_text(json.dumps(data, indent=2))
print(f"Written {len(data['scenarios'])} scenarios to {path}")
print(f"Total rules: {len(data['rules'])}")
