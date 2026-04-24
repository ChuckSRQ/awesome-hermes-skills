#!/usr/bin/env python3
"""
Patch generator for agentic self-improvement.

Generates XML guidance blocks based on failure analysis,
for insertion into model execution guidance constants.
Supports OpenAI, Anthropic, Gemini, and MiniMax model types.
"""

from __future__ import annotations

import os

import re
from pathlib import Path

HERMES_AGENT_DIR = Path(os.environ.get("HERMES_AGENT_DIR", os.path.expanduser("~/.hermes/hermes-agent")))
PROMPT_BUILDER = HERMES_AGENT_DIR / "agent" / "prompt_builder.py"

# Guidance block templates per category
GUIDANCE_TEMPLATES = {
    "mandatory_tool_use": """
<mandatory_tool_use>
NEVER answer these from memory or mental computation -- ALWAYS use a tool:
- Arithmetic, math, calculations -> use terminal or execute_code
- Hashes, encodings, checksums (MD5, SHA, base64) -> use terminal (e.g. sha256sum, md5sum)
- Current time, date, timezone -> use terminal (e.g. date)
- System state: OS, CPU, memory, disk space, ports, processes -> use terminal
- File contents, line counts, file existence -> use read_file, search_files, or terminal
- Git history, branches, diffs, status -> use terminal (git)
- Current facts (weather, news, versions, prices) -> use web_search
- Network connectivity (ports, URLs) -> use terminal (curl, nc, ping)
Your memory and user profile describe the USER, not the system you are running on.
The execution environment may differ from what the user profile says about their personal setup.
</mandatory_tool_use>
""",

    "act_dont_ask": """
<act_dont_ask>
When a question has an obvious default interpretation, act on it immediately
instead of asking for clarification. Examples:
- "Is port 443 open?" -> check THIS machine (do not ask "open where?")
- "What OS am I running?" -> check the live system (do not use user profile)
- "What time is it?" -> run `date` (do not guess)
- "How much disk space?" -> run `df` (do not ask what disk)
- "Is Python installed?" -> check THIS machine (do not ask which Python)
- "Read the file at /tmp/test.txt" -> use read_file or terminal (do not ask for confirmation)
Only ask for clarification when the ambiguity genuinely changes what tool you would call.
</act_dont_ask>
""",

    "no_hallucination": """
<no_hallucination>
NEVER answer from memory, training data, or stored user profile when a tool could verify:
- Your memory and user profile describe the USER, not the system you run on
- OS version, installed software, file locations -- must verify with tools
- Recent activity, files edited, commands run -- must check, not recall
- Terminal colors, window manager, desktop environment -- must check this machine
If you cannot verify with a tool, say you cannot know rather than guessing.
</no_hallucination>
""",

    "verification": """
<verification>
Before finalizing your response:
- Correctness: does the output satisfy every stated requirement?
- Completeness: did you check all requested items or paths?
- Grounding: are factual claims backed by tool outputs or provided context?
- Errors: did tools return errors or empty results? Report these explicitly.
- File existence: if a file was reported as not found, say so clearly.
Do not present an empty tool result as valid content.
</verification>
""",

    "prerequisite_checks": """
<prerequisite_checks>
Before taking an action, check whether prerequisite discovery or context-gathering
steps are needed:
- Before listing files, verify the directory exists
- Before reading a config, verify the file exists
- Before making an API call, verify credentials are valid and have required scopes
- Before running git commands, verify you are in a git repository
- Before using a Python library, verify it is installed (e.g. python3 -c "import pkg")
Do not skip prerequisite steps just because the final action seems obvious.
</prerequisite_checks>
""",

    "path_accuracy": """
<path_accuracy>
ALWAYS verify paths before using them. Do not assume:
- Files exist without checking (use `ls` or `test -f`)
- Directories exist without checking (use `ls -d` or `test -d`)
- Paths are correct without verification
- Token/config files exist before attempting to read them
When told a path, confirm it exists before attempting operations on it.
</path_accuracy>
""",

    "context_grounding": """
<context_grounding>
ALWAYS verify current context before acting -- do not assume:
- Current directory (use `pwd`)
- Git branch (use `git branch`)
- Git repository status (use `git status`)
- Files in current directory (use `ls`)
- Python environment or project type (check for pyproject.toml, requirements.txt, etc.)
Context from previous conversations or different directories does not apply to the current session.
</context_grounding>
""",

    "credential_verification": """
<credential_verification>
Before using any API token, credentials, or authentication:
1. Verify the credential file exists (test -f or ls)
2. Verify it is valid JSON (parse it)
3. Verify it has not expired (check exp/expiry field)
4. Verify it has the required scopes for the operation you plan to perform
5. If any check fails, report the failure explicitly rather than attempting the call
Do not attempt API calls with credentials you have not verified are valid and sufficient.
</credential_verification>
""",

    "remember_to_obsidian": """
<remember_to_obsidian>
When the user says "remember this" or shares durable personal information:
1. Write it to Obsidian immediately using terminal with cat or write_file
2. The memory tool is SHORT-TERM only (~2,200 chars) -- it is NOT for durable storage
3. Obsidian is the permanent memory -- use it for: personal details, preferences, facts about the user's life/work/family
4. Session summaries go to <obsidian-vault>/03-Notes/sessions/YYYY-MM-DD.md
Examples of what MUST go to Obsidian:
- "My pet's name is X" -> write to Obsidian
- "I work at X company" -> write to Obsidian
- "My partner's name is X" -> write to Obsidian
- "I prefer contact via X" -> write to Obsidian
- Any personal fact the user explicitly asks you to remember
Do NOT rely on the memory tool for anything that should persist across sessions.
</remember_to_obsidian>
""",
}


def detect_model_type(model: str) -> str:
    """Detect which model type guidance to generate."""
    model_lower = model.lower()
    if "gpt" in model_lower or "codex" in model_lower or "openai" in model_lower:
        return "openai"
    elif "claude" in model_lower or "anthropic" in model_lower:
        return "anthropic"
    elif "gemini" in model_lower or "google" in model_lower:
        return "gemini"
    elif "minimax" in model_lower:
        return "minimax"
    else:
        return "openai"  # Default


def get_guidance_constant_name(model_type: str) -> str:
    """Get the guidance constant name for a model type."""
    mapping = {
        "openai": "OPENAI_MODEL_EXECUTION_GUIDANCE",
        "anthropic": "ANTHROPIC_MODEL_EXECUTION_GUIDANCE",
        "gemini": "GEMINI_MODEL_EXECUTION_GUIDANCE",
        "minimax": "MINIMAX_MODEL_EXECUTION_GUIDANCE",
    }
    return mapping.get(model_type, "OPENAI_MODEL_EXECUTION_GUIDANCE")


def generate_guidance_block(category: str) -> str:
    """Generate the guidance text for a category."""
    key = _map_category_to_key(category)
    return GUIDANCE_TEMPLATES.get(key, "")


def _map_category_to_key(category: str) -> str:
    """Map benchmark category to guidance template key."""
    mapping = {
        "mandatory_tool": "mandatory_tool_use",
        "act_dont_ask": "act_dont_ask",
        "no_hallucination": "no_hallucination",
        "verification": "verification",
        "prerequisite": "prerequisite_checks",
        "path_accuracy": "path_accuracy",
        "context_grounding": "context_grounding",
        "auth_state": "credential_verification",
        "remember_to_obsidian": "remember_to_obsidian",
    }
    return mapping.get(category, category)


def generate_patch_for_category(category: str, pass_rate: float) -> str | None:
    """Generate a patch for a category if its pass rate is below threshold."""
    if pass_rate >= 0.9:
        return None  # No patch needed

    guidance = generate_guidance_block(category)
    if not guidance:
        return None

    return f"# CATEGORY: {category} (pass rate: {pass_rate:.0%})\n{guidance.strip()}"


def generate_full_guidance(analyses: dict, model: str = "openai") -> str:
    """Generate full guidance text from analyses."""
    lines = []
    for cat, analysis in analyses.items():
        if analysis.pass_rate < 1.0:  # Only include failing categories
            patch = generate_patch_for_category(cat, analysis.pass_rate)
            if patch:
                lines.append(patch)
                lines.append("\n")

    return "\n".join(lines)


def read_current_guidance(model_type: str) -> str:
    """Read the current guidance constant from prompt_builder.py."""
    if not PROMPT_BUILDER.exists():
        return ""

    const_name = get_guidance_constant_name(model_type)
    with open(PROMPT_BUILDER) as f:
        content = f.read()

    pattern = rf'{const_name}\s*=\s*\('
    match = re.search(pattern, content)
    if not match:
        return ""

    start = match.end()
    depth = 0
    end = start
    for i, c in enumerate(content[start:], start):
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    return content[start:end]


if __name__ == "__main__":
    import fire
    fire.Fire({
        "generate_block": generate_guidance_block,
        "detect_model": detect_model_type,
        "generate_full": generate_full_guidance,
    })
