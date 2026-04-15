#!/usr/bin/env python3
"""
Apply and verify patches for agentic self-improvement.

Applies guidance patches to prompt_builder.py with backup,
reverts on regression, and reports delta.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

HERMES_AGENT_DIR = Path(os.environ.get("HERMES_AGENT_DIR", os.path.expanduser("~/.hermes/hermes-agent")))
PROMPT_BUILDER = HERMES_AGENT_DIR / "agent" / "prompt_builder.py"
BACKUPS_DIR = Path(os.environ.get("SELF_IMPROVE_DIR", os.path.expanduser("~/.hermes/self-improvement/backups")))
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
PROPOSED_DIR = Path(os.environ.get("SELF_IMPROVE_DIR", os.path.expanduser("~/.hermes/self-improvement/proposed_patches")))
PROPOSED_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR = Path(os.environ.get("SELF_IMPROVE_DIR", os.path.expanduser("~/.hermes/self-improvement/results")))

from benchmark_runner import run_full_suite, load_all_benchmarks
from failure_analyzer import analyze_results
from patch_generator import (
    generate_full_guidance,
    get_guidance_constant_name,
    detect_model_type,
)


@dataclass
class PatchResult:
    applied: bool
    run_id: str
    before_rates: dict
    after_rates: dict
    delta: dict
    reverted: bool = False
    regression: Optional[str] = None
    patch_content: str = ""


def backup_prompt_builder(model_type: str) -> Path:
    """Backup the current prompt_builder.py."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{ts}_{model_type}.py"
    backup_path = BACKUPS_DIR / backup_name
    shutil.copy2(PROMPT_BUILDER, backup_path)
    return backup_path


def revert_to_backup(backup_path: Path, model_type: str) -> None:
    """Revert prompt_builder.py to a backup."""
    shutil.copy2(backup_path, PROMPT_BUILDER)


def apply_guidance_patch(guidance_text: str, model_type: str) -> bool:
    """Apply guidance text to the relevant GUIDANCE constant in prompt_builder.py."""
    if not PROMPT_BUILDER.exists():
        print(f"ERROR: {PROMPT_BUILDER} not found")
        return False

    const_name = get_guidance_constant_name(model_type)

    with open(PROMPT_BUILDER) as f:
        content = f.read()

    # Find the constant start
    pattern = rf'({const_name}\s*=\s*\()'
    match = re.search(pattern, content)
    if not match:
        print(f"ERROR: Could not find {const_name} in prompt_builder.py")
        return False

    # Find the end of the multiline string (matching closing paren)
    start_pos = match.end() - 1  # Position of opening (
    depth = 0
    end_pos = start_pos
    for i, c in enumerate(content[start_pos:], start_pos):
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                end_pos = i + 1
                break

    # Build new content
    new_content = content[:start_pos] + "(" + guidance_text + ")" + content[end_pos:]

    with open(PROMPT_BUILDER, "w") as f:
        f.write(new_content)

    return True


def extract_pass_rates_from_results(results: dict) -> dict:
    """Extract pass rates per category from results."""
    rates = {}
    for cat, data in results.get("categories", {}).items():
        if "pass_rate" in data:
            rates[cat] = data["pass_rate"]
    return rates


def run_benchmark_and_get_rates(
    categories: Optional[list[str]],
    model: str,
    parallel: int,
) -> tuple[dict, dict]:
    """Run benchmarks and return results + rates."""
    results = run_full_suite(categories=categories, model=model, parallel=parallel)
    rates = extract_pass_rates_from_results(results)
    return results, rates


def _get_default_model() -> str:
    """Read default model from config."""
    config_path = Path(os.environ.get("HERMES_CONFIG", os.path.expanduser("~/.hermes/config.yaml")))
    if config_path.exists():
        try:
            import yaml
            config = yaml.safe_load(config_path.read_text())
            model_val = config.get("model", {})
            # model may be a dict {"default": "...", "provider": "...", ...} or a string
            if isinstance(model_val, dict):
                return model_val.get("default", "gpt-4o")
            return model_val or "gpt-4o"
        except Exception:
            pass
    return "gpt-4o"


def apply_and_verify(
    categories: Optional[list[str]] = None,
    model: str = "default",
    parallel: int = 4,
    mode: str = "suggest",
) -> PatchResult:
    """
    Main apply-and-verify loop.

    1. Run baseline benchmarks
    2. Generate guidance patch
    3. Backup prompt_builder.py
    4. Apply patch
    5. Re-run benchmarks
    6. If regression -> revert
    7. If improvement -> keep
    """
    # Resolve model
    if model == "default":
        model = _get_default_model()
    model_type = detect_model_type(model)

    run_id = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # Step 1: Baseline run
    print(f"[{run_id}] Running baseline benchmarks...")
    baseline_results, before_rates = run_benchmark_and_get_rates(categories, model, parallel)
    baseline_run_id = baseline_results.get("run_id", run_id)

    print("\nBaseline pass rates:")
    for cat, rate in sorted(before_rates.items()):
        print(f"  {cat}: {rate:.1%}")
    print()

    # Step 2: Generate patch
    analyses = analyze_results(baseline_results)
    guidance_text = generate_full_guidance(analyses, model_type)

    if not guidance_text.strip():
        print("No guidance patches needed -- all categories at 100%")
        return PatchResult(
            applied=False,
            run_id=run_id,
            before_rates=before_rates,
            after_rates=before_rates,
            delta={},
            patch_content="",
        )

    const_name = get_guidance_constant_name(model_type)
    patch_content = f"{const_name} += ({guidance_text}\n)"

    # Write proposed patch
    patch_file = PROPOSED_DIR / f"{run_id}.diff"
    patch_file.write_text(patch_content)
    print(f"Proposed patch written to: {patch_file}")

    if mode == "suggest":
        print("\n" + "=" * 60)
        print("PATCH CONTENT (--mode=suggest, not applied)")
        print("=" * 60)
        print(patch_content)
        print("=" * 60)
        return PatchResult(
            applied=False,
            run_id=run_id,
            before_rates=before_rates,
            after_rates=before_rates,
            delta={},
            patch_content=patch_content,
        )

    # mode == "apply"
    print(f"[{run_id}] Applying patch in --mode=apply...")

    # Step 3: Backup
    backup_path = backup_prompt_builder(model_type)
    print(f"Backed up to: {backup_path}")

    # Step 4: Apply
    success = apply_guidance_patch(guidance_text, model_type)
    if not success:
        print("FAILED to apply patch")
        return PatchResult(
            applied=False,
            run_id=run_id,
            before_rates=before_rates,
            after_rates=before_rates,
            delta={},
            patch_content=patch_content,
        )

    print(f"Patch applied to {PROMPT_BUILDER}")

    # Step 5: Re-run benchmarks
    print(f"[{run_id}] Re-running benchmarks after patch...")
    after_results, after_rates = run_benchmark_and_get_rates(categories, model, parallel)

    print("\nAfter-patch pass rates:")
    for cat, rate in sorted(after_rates.items()):
        delta = rate - before_rates.get(cat, 0)
        marker = "+" if delta > 0 else "" if delta == 0 else ""
        print(f"  {cat}: {rate:.1%} ({marker}{delta:+.1%})")

    # Step 6: Check for regression
    regression = None
    reverted = False
    for cat in before_rates:
        before = before_rates.get(cat, 0)
        after = after_rates.get(cat, 0)
        if after < before:
            regression = f"{cat}: {before:.1%} -> {after:.1%}"
            break

    delta = {cat: after_rates.get(cat, 0) - before_rates.get(cat, 0) for cat in before_rates}

    if regression:
        # Step 7: Revert
        print(f"\n!!! REGRESSION DETECTED: {regression}")
        print(f"Reverting to backup: {backup_path}")
        revert_to_backup(backup_path, model_type)
        reverted = True
        print("Reverted.")

        return PatchResult(
            applied=True,
            run_id=run_id,
            before_rates=before_rates,
            after_rates=after_rates,
            delta=delta,
            reverted=True,
            regression=regression,
            patch_content=patch_content,
        )

    # No regression -- keep patch
    print("\nNo regression detected. Patch kept.")
    print(f"Baseline run results: {baseline_run_id}")
    print(f"After-patch run results: {after_results.get('run_id', 'unknown')}")

    return PatchResult(
        applied=True,
        run_id=run_id,
        before_rates=before_rates,
        after_rates=after_rates,
        delta=delta,
        reverted=False,
        patch_content=patch_content,
    )


def revert_last(model_type: str = "openai") -> bool:
    """Revert to the most recent backup."""
    backups = sorted(BACKUPS_DIR.glob(f"*_{model_type}.py"), key=lambda p: p.stat().st_mtime)
    if not backups:
        print(f"No backups found for {model_type}")
        return False

    latest = backups[-1]
    print(f"Reverting to: {latest}")
    revert_to_backup(latest, model_type)
    print("Reverted.")
    return True


if __name__ == "__main__":
    import fire
    fire.Fire({
        "apply": apply_and_verify,
        "revert": revert_last,
    })
