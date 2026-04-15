#!/usr/bin/env python3
"""
Benchmark runner for agentic self-improvement.

Runs prompts via `hermes chat` as subprocesses, captures trajectories,
validates against expected behaviors, and writes results to disk.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

# Paths — all configurable via environment variables
HERMES_HOME = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")))
SKILL_DIR = HERMES_HOME / "skills" / "agentic-self-improvement"
RESULTS_DIR = Path(os.environ.get("SELF_IMPROVE_DIR", HERMES_HOME / "self-improvement" / "results"))
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class BenchmarkPrompt:
    id: str
    prompt: str
    validator: dict
    ground_truth: Optional[str] = None
    expected_behavior: Optional[str] = None


@dataclass
class BenchmarkResult:
    prompt_id: str
    prompt: str
    category: str
    tool_used: bool = False
    tools_used: list = field(default_factory=list)
    tool_outputs: list = field(default_factory=list)
    response_text: str = ""
    exit_code: int = 0
    passed: bool = False
    error: str = ""
    duration_seconds: float = 0.0


def load_benchmark_category(category_name: str) -> list[BenchmarkPrompt]:
    """Load prompts from a benchmark YAML file."""
    yaml_path = SKILL_DIR / "BENCHMARKS" / f"{category_name}.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"Benchmark file not found: {yaml_path}")

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    prompts = []
    for item in data.get("prompts", []):
        prompts.append(BenchmarkPrompt(
            id=item["id"],
            prompt=item["prompt"],
            validator=item.get("validator", {}),
            ground_truth=item.get("ground_truth"),
            expected_behavior=item.get("expected_behavior"),
        ))
    return prompts


def load_all_benchmarks(categories: Optional[list[str]] = None) -> dict[str, list[BenchmarkPrompt]]:
    """Load all benchmark categories, optionally filtered by category list."""
    benchmarks_dir = SKILL_DIR / "BENCHMARKS"
    all_files = list(benchmarks_dir.glob("*.yaml"))

    if categories:
        all_files = [f for f in all_files if f.stem in categories]

    result = {}
    for yaml_file in all_files:
        category = yaml_file.stem
        result[category] = load_benchmark_category(category)

    return result


def run_prompt_via_hermes(
    prompt: str,
    model: str,
    timeout: int = 60,
) -> tuple[str, list[dict], int, float, str]:
    """
    Run a single prompt via `hermes chat` as a subprocess.

    Returns: (response_text, tool_calls, exit_code, duration, stderr)
    """
    cmd = [
        "hermes", "chat",
        "-q", prompt,
        "-Q",
        "--model", model,
    ]

    start = time.time()
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(input=prompt, timeout=timeout)
        duration = time.time() - start
        exit_code = proc.returncode

        # Parse tool calls from output
        tool_calls = _parse_tool_calls_from_output(stdout)
        response_text = _extract_response_text(stdout)

        return response_text, tool_calls, exit_code, duration, stderr

    except subprocess.TimeoutExpired:
        proc.kill()
        duration = time.time() - start
        return "", [], -1, duration, "Timeout"
    except Exception as e:
        duration = time.time() - start
        return "", [], -1, duration, str(e)


def _parse_tool_calls_from_output(stdout: str) -> list[dict]:
    """Extract tool calls from hermes output."""
    tool_calls = []
    for line in stdout.splitlines():
        try:
            obj = json.loads(line)
            if isinstance(obj, dict) and obj.get("type") == "tool_call":
                tool_calls.append(obj)
            elif isinstance(obj, dict) and "tool" in obj:
                tool_calls.append(obj)
        except json.JSONDecodeError:
            pass

    # Also detect "preparing X..." tool previews that Hermes renders as text
    tool_names = ["terminal", "write_file", "read_file", "search_files",
                  "skill_view", "patch", "execute_code", "memory"]
    import re
    patterns = [
        r"preparing\s+(\w+)",
        r"[\U0001F300-\U0001F9FF].*\s(preparing\s+)?(\w+)",
    ]
    for line in stdout.splitlines():
        for pat in patterns:
            matches = re.findall(pat, line, re.IGNORECASE)
            for match in matches:
                tool = match if isinstance(match, str) else [m for m in match if m][-1]
                tool = tool.strip()
                if tool in tool_names:
                    tool_calls.append({"tool": tool, "type": "tool_call", "source": "text_preview"})

    return tool_calls


def _extract_response_text(stdout: str) -> str:
    """Extract the final response text from hermes output."""
    lines = stdout.splitlines()
    response_parts = []
    for line in reversed(lines):
        try:
            json.loads(line)
            break  # Hit JSON, stop
        except json.JSONDecodeError:
            response_parts.insert(0, line)
    return "\n".join(response_parts).strip()


def validate_result(result: BenchmarkResult, prompt: BenchmarkPrompt) -> bool:
    """Validate a benchmark result against the expected validator."""
    validator = prompt.validator
    vtype = validator.get("type", "")

    if vtype == "tool_used":
        required_tools = validator.get("tools", [])
        if required_tools:
            if not any(t in result.tools_used for t in required_tools):
                return False
        return result.tool_used

    elif vtype == "command_contains":
        expected = validator.get("command_contains", [])
        if not expected:
            return result.tool_used
        text = result.response_text.lower()
        outputs = " ".join(result.tool_outputs).lower()
        return any(kw in text or kw in outputs for kw in expected)

    elif vtype == "refused_to_answer":
        refused_phrases = ["cannot", "don't know", "no way to know", "unable to determine", "can't determine"]
        text_lower = result.response_text.lower()
        if any(phrase in text_lower for phrase in refused_phrases):
            return True
        return result.tool_used

    elif vtype == "tool_used_or_refused":
        if result.tool_used:
            return True
        refused_phrases = ["cannot", "don't know", "no way", "unable"]
        return any(p in result.response_text.lower() for p in refused_phrases)

    elif vtype == "tool_output_verified":
        expected = validator.get("expected_output", "")
        return expected in result.response_text or any(expected in out for out in result.tool_outputs)

    elif vtype == "error_detected":
        return result.exit_code != 0 or "error" in result.response_text.lower() or "not found" in result.response_text.lower()

    elif vtype == "two_step_verification":
        return result.tool_used and bool(result.response_text)

    elif vtype == "conditional_tool_use":
        if result.tool_used:
            return True
        return "not exist" in result.response_text.lower()

    elif vtype == "refused_or_tool_used":
        required_tools = validator.get("tools", [])
        if result.tool_used and required_tools:
            return any(t in result.tools_used for t in required_tools)
        refused_phrases = ["cannot", "don't know", "no way", "unable"]
        return any(p in result.response_text.lower() for p in refused_phrases)

    elif vtype == "non_empty_or_explicit_not_found":
        if "not found" in result.response_text.lower() or "does not exist" in result.response_text.lower():
            return True
        return bool(result.response_text.strip())

    elif vtype == "two_step":
        return result.tool_used

    elif vtype == "sequence":
        return result.tool_used

    elif vtype == "exit_code_check":
        return result.exit_code == 0

    # Default: if tools were used, consider it passed
    return result.tool_used


def _get_default_model() -> str:
    """Read the default model from config."""
    config_path = HERMES_HOME / "config.yaml"
    if config_path.exists():
        try:
            with open(config_path) as f:
                import yaml as yaml2
                config = yaml2.safe_load(f)
                model_val = config.get("model", {})
                if isinstance(model_val, dict):
                    return model_val.get("default", "gpt-4o")
                return model_val or "gpt-4o"
        except Exception:
            pass
    return "gpt-4o"


def run_benchmark(
    category: str,
    model: str = "default",
    parallel: int = 4,
    timeout: int = 60,
) -> dict:
    """Run all prompts in a category. Returns a dict with results and summary."""
    prompts = load_benchmark_category(category)
    if not prompts:
        return {"category": category, "error": f"No prompts found for category: {category}"}

    if model == "default":
        model = _get_default_model()

    results = []
    for prompt in prompts:
        response_text, tool_calls, exit_code, duration, stderr = run_prompt_via_hermes(
            prompt.prompt, model, timeout=timeout
        )

        tools_used = [tc.get("tool", tc.get("name", "")) for tc in tool_calls]
        tool_outputs = [tc.get("output", "") for tc in tool_calls]

        result = BenchmarkResult(
            prompt_id=prompt.id,
            prompt=prompt.prompt,
            category=category,
            tool_used=len(tool_calls) > 0,
            tools_used=tools_used,
            tool_outputs=tool_outputs,
            response_text=response_text,
            exit_code=exit_code,
            duration_seconds=duration,
            error=stderr if stderr else "",
        )
        result.passed = validate_result(result, prompt)
        results.append(result)

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    run_id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_dir = RESULTS_DIR / f"{run_id}_{category}"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "results.json", "w") as f:
        json.dump({
            "run_id": run_id,
            "model": model,
            "overall_passed": passed,
            "overall_total": total,
            "overall_pass_rate": passed / total if total > 0 else 0,
            "categories": {
                category: {
                    "category": category,
                    "model": model,
                    "total": total,
                    "passed": passed,
                    "failed": total - passed,
                    "pass_rate": passed / total if total > 0 else 0,
                    "results": [asdict(r) for r in results],
                }
            },
            "timestamp": datetime.now().isoformat(),
        }, f, indent=2)

    return {
        "category": category,
        "model": model,
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total > 0 else 0,
        "results": [asdict(r) for r in results],
        "results_dir": str(output_dir),
    }


def run_full_suite(
    categories: Optional[list[str]] = None,
    model: str = "default",
    parallel: int = 4,
    timeout: int = 60,
) -> dict:
    """Run all benchmark categories. Returns a dict with per-category results and summary."""
    benchmarks = load_all_benchmarks(categories)
    if not benchmarks:
        return {"error": "No benchmarks found"}

    if model == "default":
        model = _get_default_model()

    run_id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    all_results = {}
    overall_passed = 0
    overall_total = 0

    for category, prompts in benchmarks.items():
        cat_result = run_benchmark(category, model, parallel, timeout)
        all_results[category] = cat_result
        if "total" in cat_result:
            overall_passed += cat_result["passed"]
            overall_total += cat_result["total"]

    output_dir = RESULTS_DIR / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "results.json", "w") as f:
        json.dump({
            "run_id": run_id,
            "model": model,
            "overall_passed": overall_passed,
            "overall_total": overall_total,
            "overall_pass_rate": overall_passed / overall_total if overall_total > 0 else 0,
            "categories": all_results,
            "timestamp": datetime.now().isoformat(),
        }, f, indent=2)

    return {
        "run_id": run_id,
        "model": model,
        "overall_passed": overall_passed,
        "overall_total": overall_total,
        "overall_pass_rate": overall_passed / overall_total if overall_total > 0 else 0,
        "categories": all_results,
        "results_dir": str(output_dir),
    }


if __name__ == "__main__":
    import fire
    fire.Fire({
        "run": run_benchmark,
        "run_all": run_full_suite,
        "list": load_all_benchmarks,
    })
