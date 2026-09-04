"""
Corporate CSR Funding & Prototype Showcase Package
Module: ai-engine/part-b/corporate
"""

from .prototypes_data import (
    PROTOTYPES_STORE,
    CORPORATE_SPONSORS_STORE,
    SCHEDULE_VII_CATEGORIES,
    TRL_DESCRIPTIONS,
    register_prototype_submission,
    list_prototypes,
    get_prototype_by_id,
)

from .stakeholder_governance import (
    SPONSORSHIPS_STORE,
    create_sponsorship_pledge,
    approve_milestone,
    generate_tripartite_agreement_text,
)

from .csr_engine import (
    match_sponsors_for_prototype,
    generate_csr_impact_certificate,
)

__all__ = [
    "PROTOTYPES_STORE",
    "CORPORATE_SPONSORS_STORE",
    "SCHEDULE_VII_CATEGORIES",
    "TRL_DESCRIPTIONS",
    "register_prototype_submission",
    "list_prototypes",
    "get_prototype_by_id",
    "SPONSORSHIPS_STORE",
    "create_sponsorship_pledge",
    "approve_milestone",
    "generate_tripartite_agreement_text",
    "match_sponsors_for_prototype",
    "generate_csr_impact_certificate",
]
