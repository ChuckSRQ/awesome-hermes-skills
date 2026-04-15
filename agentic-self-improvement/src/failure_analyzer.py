#!/usr/bin/env python3
"""
Failure analyzer for agentic self-improvement.

Reads benchmark results, groups failures by category,
computes pass rates, and extracts failure examples.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

RESULTS_DIR = Path(os.environ.get("SELF_IMPROVE_DIR", os.path.expanduser("~/.hermes/self-improvement/results")))


@dataclass
class FailureExample:
    prompt_id: str
    prompt: str
    response: str
    tools_used: list
    expected_behavior: str
    category: str


@dataclass
class CategoryAnalysis:
    category: str
    total: int
    passed: int
    failed: int
    pass_rate: float
    failure_examples: list
    suggested_guidance_category: str


def load_results(run_id: str) -> dict:
    """Load results from a past run."""
    results_file = RESULTS_DIR / run_id / "results.json"
    if not results_file.exists():
        raise FileNotFoundError(f"Results not found: {results_file}")
    with open(results_file) as f:
        return json.load(f)


def analyze_results(results: dict) -> dict[str, CategoryAnalysis]:
    """
    Analyze benchmark results and produce per-category analysis.

    Returns a dict mapping category -> CategoryAnalysis.
    """
    categories = results.get("categories", {})
    analyses = {}

    for cat_name, cat_data in categories.items():
        if "error" in cat_data:
            continue

        results_list = cat_data.get("results", [])
        failures = [r for r in results_list if not r.get("passed", False)]

        failure_examples = []
        for f in failures[:3]:  # Keep top 3 failure examples per category
            failure_examples.append(FailureExample(
                prompt_id=f["prompt_id"],
                prompt=f["prompt"],
                response=f.get("response_text", "")[:500],
                tools_used=f.get("tools_used", []),
                expected_behavior=_infer_expected(f),
                category=cat_name,
            ))

        analyses[cat_name] = CategoryAnalysis(
            category=cat_name,
            total=cat_data["total"],
            passed=cat_data["passed"],
            failed=cat_data["failed"],
            pass_rate=cat_data["pass_rate"],
            failure_examples=failure_examples,
            suggested_guidance_category=_map_to_guidance_category(cat_name),
        )

    return analyses


def summarize(analyses: dict[str, CategoryAnalysis]) -> str:
    """Generate a human-readable summary of analyses."""
    lines = []
    lines.append("=" * 60)
    lines.append("BENCHMARK ANALYSIS SUMMARY")
    lines.append("=" * 60)

    for cat, analysis in analyses.items():
        status = "PASS" if analysis.pass_rate >= 0.8 else "FAIL" if analysis.pass_rate < 0.5 else "WARN"
        lines.append(f"\n[{status}] {cat.upper()}")
        lines.append(f"  Pass rate: {analysis.pass_rate:.1%} ({analysis.passed}/{analysis.total})")

        if analysis.failure_examples:
            lines.append(f"  Failure examples:")
            for ex in analysis.failure_examples[:2]:
                lines.append(f"    - [{ex.prompt_id}] {ex.prompt[:60]}...")
                lines.append(f"      Response: {ex.response[:80]}...")

    lines.append("\n" + "=" * 60)
    overall = sum(a.passed for a in analyses.values())
    total = sum(a.total for a in analyses.values())
    lines.append(f"OVERALL: {overall}/{total} ({overall/total:.1%})" if total else "OVERALL: N/A")
    lines.append("=" * 60)
    return "\n".join(lines)


def _infer_expected(failure: dict) -> str:
    """Infer what the expected behavior was from a failed result."""
    v = failure.get("validator", {})
    vtype = v.get("type", "unknown")
    tools = v.get("tools", [])
    note = v.get("note", "")

    if note:
        return note
    if tools:
        return f"Should have used tool: {tools[0]}"
    return f"Validator type: {vtype}"


def _map_to_guidance_category(category: str) -> str:
    """Map benchmark category to guidance block name."""
    mapping = {
        "mandatory_tool": "mandatory_tool_use",
        "act_dont_ask": "act_dont_ask",
        "no_hallucination": "no_hallucination",
        "verification": "verification",
        "prerequisite": "prerequisite_checks",
        "path_accuracy": "path_accuracy",
        "context_grounding": "context_grounding",
        "auth_state": "credential_verification",
    }
    return mapping.get(category, category)


def print_analysis(run_id: str) -> None:
    """Load and print analysis for a run."""
    results = load_results(run_id)
    analyses = analyze_results(results)
    print(summarize(analyses))


if __name__ == "__main__":
    import fire
    fire.Fire({
        "analyze": analyze_results,
        "load": load_results,
        "print": print_analysis,
    })
