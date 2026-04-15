---
name: pnc-bank-statement-analysis
description: Extract and analyze transaction data from PNC Bank Virtual Wallet PDF statements. Uses pymupdf for text extraction, handles multi-line transaction format, and filters internal transfers.
author: Hermes Agent
license: MIT
tags: [PDF, banking, pymupdf, financial-analysis]
---

# PNC Bank Statement PDF Analysis

Use this skill when analyzing PNC Bank Virtual Wallet PDF statements.

## PNC Statement Format (Virtual Wallet)

Transactions appear with **date, amount, and description on separate lines**:
```
Date
Amount
Description (may span multiple lines until next date or empty line)
```

**Key account numbers:**
- SPEND account (x9308): daily spending, payroll deposits land here
- RESERVE account (x9316): fixed bills (rent, daycare)
- GROWTH account (x9324): long-term savings

**Internal transfers to filter out** (NOT external spending):
- `Online Transfer To XXXXX9308` / `Online Transfer To XXXXX9316` / `Online Transfer To XXXXX9324`
- `Funds Transfer To Acct 1212729308` / `Funds Transfer To Acct 1212729316`
- `Funds Transfer From Acct 1212729308` / `Funds Transfer From Acct 1212729316`

**Statement periods don't match calendar months.** A "December 2025" statement might run Nov 6 - Dec 3. Always use the statement's own period dates, not the filename.

## Extraction Approach

### Recommended: Use statement summary totals first
For high-level budget analysis, the statement's own totals are cleaner than summing parsed transactions:
```python
import re
beg_bal = re.search(r'Beginning\s+balance\s+\$?([\d,]+\.\d{2})', text)
total_deposits = re.search(r'There were \d+ Deposits and Other\s+Additions totaling \$?([\d,]+\.\d{2})', text)
total_deductions = re.search(r'There were \d+ (?:Banking Machine/Debit Card )?(?:deductions|Checks and other deductions)\s+totaling \$?([\d,]+\.\d{2})', text)
```

### For detailed transaction parsing (line-by-line)
```python
import re

def parse_pnc_transactions(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    
    transactions = []
    lines = text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        # Date pattern: MM/DD
        if re.match(r'^\d{2}/\d{2}$', line):
            date_str = line
            i += 1
            # Skip blank lines
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines):
                amount_match = re.search(r'\$?([\d,]+\.\d{2})', lines[i])
                amount = float(amount_match.group(1).replace(',', '')) if amount_match else 0
                i += 1
                # Collect multi-line description
                desc_lines = []
                while i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line:
                        i += 1
                        continue
                    # Next date or amount ends current transaction
                    if re.match(r'^\d{2}/\d{2}$', next_line):
                        break
                    if re.match(r'^\$?[\d,]+\.\d{2}$', next_line):
                        break
                    desc_lines.append(next_line)
                    i += 1
                desc = ' '.join(desc_lines).strip()
                if desc:
                    transactions.append({'date': date_str, 'amount': amount, 'desc': desc})
                continue
        i += 1
    
    return transactions
```

## Common Fixed Expense Patterns (Reserve Account)

**Rent** ( Zel To Cosmas Oguejiofor ):
```python
rent = re.findall(r'(\d{2}/\d{2}).*?Zel To Cosmas.*?([\d,]+\.\d{2})', text)
```

**Daycare** (Tle Odessa BlueC):
```python
daycare = re.findall(r'(\d{2}/\d{2}).*?(?:Odessa Bluec|Tle).*?([\d,]+\.\d{2})', text)
```

## Critical: Line Offset for Payroll Deposits

**PNC PDF text extraction has a line-offset issue.** When searching for a description like `SKIN NV LLC`, the actual **amount is NOT on the line before it** — it's **2 lines before** the description line. The line immediately before the description is the **date**.

Correct pattern for payroll deposits:
```
[amount at i-2]  ← THIS IS THE DOLLAR AMOUNT
[date at i-1]    ← NOT the amount
[description at i]  ← SKIN NV LLC, PROPERTYWORKS, etc.
```

Correct extraction code:
```python
for i, line in enumerate(lines):
    stripped = line.strip()
    if 'SKIN NV' in stripped or 'PROPERTYWORKS' in stripped:
        prev2 = lines[i-2].strip() if i >= 2 else ''
        amt_match = re.search(r'[\d,]+\.\d{2}', prev2)
        if amt_match:
            val = float(amt_match.group().replace(',',''))
```

**Why this matters:** Using `i-1` (one line before) will get the date string, not the amount. Always use `i-2` for dollar amounts in PNC Virtual Wallet statements.

### Verified Employer Description Strings
- **SkinNV payroll:** `SKIN NV LLC XXXXXXXXXXX39-0` or `Direct Deposit - Payroll Skin Nv 2 Ll`
- **PropertyWorks payroll:** `PROPERTYWORKS XXXXXXXXXX6611X` or `PROPERTYWORKS XXXXXXXXXX2319X`
- **Internal transfers between own accounts:** `Online Transfer From XXXXX9316`, `Funds Transfer From Acct 1212729316`

## Known Limitations

- Multi-line descriptions can be noisy (e.g., page headers mixed into descriptions)
- `Activity Detail` section parsing is fragile; prefer summary totals for budget summaries
- "Other" category in raw data often includes internal transfers — always filter `Online Transfer To XXXXX` and `Funds Transfer To Acct 121272` before categorizing as spending
- The `i-2` line offset applies specifically to **payroll direct deposits** in the PNC Virtual Wallet format. Other transaction types may have different spacing.
