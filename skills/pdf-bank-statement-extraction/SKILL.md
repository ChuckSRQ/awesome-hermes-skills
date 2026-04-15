---
name: pdf-bank-statement-extraction
description: Extract transaction data from PDF bank statements using PyMuPDF (fitz). For reconciling actual income/spending against user-provided estimates.
category: data-science
---

# PDF Bank Statement Extraction

Extract transaction data from PDF bank statements using PyMuPDF (fitz).

## When to Use

User provides bank statements as PDFs and you need to extract actual income, spending, or transaction data to validate or build a budget. Use this before relying on user-provided estimates — bank statements don't lie.

## Setup

```bash
pip install pymupdf  # provides `fitz` module
```

## Core Pattern

PDF bank statements typically store each transaction across 3 lines:
- Line i-2 or i-1: Date
- Line i-1 or i-2: Amount (formatted with `$` and commas)
- Line i: Description (payee name, e.g. "SKIN NV PAYROLL")

The exact offset varies by bank. Always print raw line context first.

## Step-by-Step

### Step 1 — Print raw context for one statement

```python
import fitz

pdf_path = "/path/to/Statement.pdf"
doc = fitz.open(pdf_path)
text = "".join(page.get_text() for page in doc)
doc.close()

lines = text.split('\n')
for i, line in enumerate(lines):
    if 'TARGET_STRING' in line:  # e.g. 'SKIN NV', 'PAYROLL', 'DEPOSIT'
        start = max(0, i - 6)
        end   = min(len(lines), i + 3)
        print(f"\n=== lines {i-5} to {i+2} ===")
        for j in range(start, end):
            marker = ">>> " if j == i else "    "
            print(f"{marker}[{j}] {lines[j]}")
```

### Step 2 — Identify the offset pattern

Common patterns:
- Amount on `i-2`, description on `i` (seen at Bank of America, Chase)
- Amount on `i-1`, description on `i` (seen at some CU statements)
- Date on `i-3`, amount on `i-2`, description on `i`

### Step 3 — Parse all statements

```python
import fitz, re
from collections import defaultdict

MONTHS = [
    ("November_2025",  "Statement_November_2025.pdf"),
    ("December_2025",  "Statement_December_2025.pdf"),
    # ...
]

TARGET = "SKIN NV"  # or whatever you're searching for

all_deposits = []

for month_name, pdf_name in MONTHS:
    pdf_path = f"/path/to/{pdf_name}"
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)
    doc.close()
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if TARGET in line:
            prev2 = lines[i-2].strip() if i >= 2 else ''
            prev1 = lines[i-1].strip() if i >= 1 else ''
            amt_match = re.search(r'[\d,]+\.\d{2}', prev2)
            if amt_match:
                val = float(amt_match.group().replace(',',''))
                all_deposits.append((month_name, val))
            else:
                amt_match = re.search(r'[\d,]+\.\d{2}', prev1)
                if amt_match:
                    val = float(amt_match.group().replace(',',''))
                    all_deposits.append((month_name, val))
```

### Step 4 — Summarize

```python
total = sum(v for _, v in all_deposits)
n = len(all_deposits)
print(f"Total: ${total:,.2f} across {n} deposits")
print(f"Average per deposit: ${total/n:,.2f}")

by_month = defaultdict(list)
for m, v in all_deposits:
    by_month[m].append(v)
for m in ["November_2025", "December_2025", ...]:
    vals = by_month[m]
    print(f"  {m}: {len(vals)} deposits = ${sum(vals):,.2f}")
```

## Common Pitfalls

- **PDFs from different months have different formatting** — especially the last page each month. Always check at least 2 months before assuming a pattern.
- **Negative amounts** — some banks show debits as negative numbers. Use `abs()` if needed.
- **Repeat transactions** — a deposit that appears twice in one month (bi-weekly payroll) is normal.
- **Missing pages** — a month with fewer deposits than expected might mean the last page was formatted differently.
- **Reconciling with user estimates** — if extracted amounts differ significantly from what the user says, flag it: the bank statement is ground truth.

## Key Takeaway

Always print raw line context before writing the parse loop. The time spent looking at 3 lines of raw output saves 30 minutes of debugging a wrong parse.
