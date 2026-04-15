# Guidance Anatomy

How guidance blocks are structured and where they get inserted.

## Target File

`~/.hermes/hermes-agent/agent/prompt_builder.py`

## Model-Type to Guidance Constant Mapping

| Model Type | Constant Name | Provider |
|------------|--------------|----------|
| `openai` | `OPENAI_MODEL_EXECUTION_GUIDANCE` | OpenAI GPT, Codex |
| `anthropic` | `ANTHROPIC_MODEL_EXECUTION_GUIDANCE` | Claude (Anthropic) |
| `gemini` | `GEMINI_MODEL_EXECUTION_GUIDANCE` | Gemini (Google) |
| `minimax` | `MINIMAX_MODEL_EXECUTION_GUIDANCE` | MiniMax |

## Guidance Constant Format

The constants are multiline strings (parenthesized) at the top of `prompt_builder.py`:

```python
OPENAI_MODEL_EXECUTION_GUIDANCE = (
    "# Execution discipline\n"
    "<tool_persistence>\n"
    ...
)
```

## Block Anatomy

Each guidance category is wrapped in XML-style tags:

```xml
<category_name>
Guidance text here. Can span multiple lines.
Each line is a rule or example.
</category_name>
```

## Categories

### mandatory_tool_use

Lists categories of prompts that MUST use a tool.

```xml
<mandatory_tool_use>
NEVER answer these from memory or mental computation -- ALWAYS use a tool:
- Arithmetic, math, calculations -> use terminal or execute_code
- Hashes, encodings, checksums (MD5, SHA, base64) -> use terminal
- Current time, date, timezone -> use terminal
- System state: OS, CPU, memory, disk, ports -> use terminal
- File contents, line counts -> use read_file or terminal
- Git history, branches, diffs -> use terminal
- Current facts (weather, news, versions) -> use web_search
Your memory and user profile describe the USER, not the system you are running on.
</mandatory_tool_use>
```

### act_dont_ask

When to act without asking for clarification.

```xml
<act_dont_ask>
When a question has an obvious default interpretation, act immediately:
- "Is port 443 open?" -> check THIS machine
- "What OS am I running?" -> check the live system
- "What time is it?" -> run `date`
Only ask for clarification when ambiguity genuinely changes the tool choice.
</act_dont_ask>
```

### no_hallucination

Don't answer from profile/memory when system state is unknown.

```xml
<no_hallucination>
NEVER answer from memory, training data, or stored user profile:
- Your memory and user profile describe the USER, not the system you run on
- OS version, software versions, file locations -- verify with tools
- Recent activity -- check, not recall
If you cannot verify with a tool, say you cannot know.
</no_hallucination>
```

### verification

Verify outputs before finalizing.

```xml
<verification>
Before finalizing:
- Correctness: does output satisfy every requirement?
- Completeness: did you check all requested paths?
- Errors: did tools return errors? Report them explicitly.
- File existence: if not found, say so clearly.
</verification>
```

### prerequisite_checks

Check prerequisites before acting.

```xml
<prerequisite_checks>
Before taking action:
- Verify directory exists before listing files
- Verify file exists before reading
- Verify credentials valid before API calls
- Verify git repo before running git commands
</prerequisite_checks>
```

### path_accuracy

Verify paths before using.

```xml
<path_accuracy>
ALWAYS verify paths before using:
- Files exist: `ls` or `test -f`
- Directories exist: `ls -d` or `test -d`
- Token/config files exist before reading
</path_accuracy>
```

### context_grounding

Check actual context, don't assume.

```xml
<context_grounding>
ALWAYS verify current context:
- Current directory: `pwd`
- Git branch: `git branch`
- Git repository status: `git status`
Context from other sessions does not apply here.
</context_grounding>
```

### credential_verification

Verify credentials before API use.

```xml
<credential_verification>
Before API calls:
1. Verify credential file exists
2. Verify valid JSON
3. Verify not expired
4. Verify required scopes present
5. Report failure explicitly if any check fails
</credential_verification>
```

## How Patches Are Applied

The `apply_and_verify.py` script:

1. Finds the GUIDANCE constant for the detected model type
2. Appends new category blocks to it
3. Backs up the file first
4. Reverts if any category regresses

## Existing Guidance (v0.8.0 PR #6120)

v0.8.0 ships with these blocks in `OPENAI_MODEL_EXECUTION_GUIDANCE`:
- `<tool_persistence>`
- `<mandatory_tool_use>`
- `<act_dont_ask>`
- `<prerequisite_checks>`
- `<verification>`
- `<missing_context>`

The self-improvement skill generates additional blocks for categories the benchmark finds failing.
