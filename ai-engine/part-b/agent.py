"""
=============================================================================
Compatibility Bridge: ai-engine/part-b/agent.py
=============================================================================
Redirects to the official AI-Agent location:
    ai-engine/ai-agent/agent.py
=============================================================================
"""

import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent / "ai-agent"
if str(AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_DIR))

# pyrefly: ignore [missing-import]
from agent import (
    CivicOrchestratorAgent,
    get_civic_orchestrator,
    MASTER_AGENT_STORE
)

__all__ = ["CivicOrchestratorAgent", "get_civic_orchestrator", "MASTER_AGENT_STORE"]
