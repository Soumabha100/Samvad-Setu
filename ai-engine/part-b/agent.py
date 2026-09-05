"""
=============================================================================
Compatibility Bridge: ai-engine/part-b/agent.py
=============================================================================
Redirects to the official AI-Agent location:
    ai-engine/ai-agent/agent.py
=============================================================================
"""

import sys
import importlib.util
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent / "ai-agent"
agent_file = AGENT_DIR / "agent.py"

if not agent_file.exists():
    raise FileNotFoundError(f"Civic AI-Agent not found at {agent_file}")

# Avoid self-import by loading explicitly
spec = importlib.util.spec_from_file_location("ai_agent_core", str(agent_file))
ai_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai_agent_module)

CivicOrchestratorAgent = ai_agent_module.CivicOrchestratorAgent
get_civic_orchestrator = ai_agent_module.get_civic_orchestrator
MASTER_AGENT_STORE = ai_agent_module.MASTER_AGENT_STORE

__all__ = ["CivicOrchestratorAgent", "get_civic_orchestrator", "MASTER_AGENT_STORE"]

