---
name: pdf-bank-statement-to-financial-report
description: Extract bank statement data from PDFs (pymupdf), build interactive Excel budgets (openpyxl) and formatted PDF reports (reportlab). Includes income verification, print-friendly color palettes, and multi-section financial report generation.
---

# PDF Bank Statement Reader + Financial Report Builder

## What this skill does
Extracts transaction data from multi-page PDF bank statements using pymupdf (fitz), then builds two types of financial output:
1. **Interactive Excel workbook** (openpyxl) — budget tool with editable blue cells, auto-summing formulas, conditional formatting
2. **Formatted PDF financial report** (reportlab) — professional multi-section report with tables, section headers, page numbers

## Key patterns discovered through trial and error

### PDF extraction — locating deposit/payroll amounts
Bank statement PDFs from financial institutions typically show a **date line**, then **amount on the previous line**, then **description**. The SKIN NV payroll deposits were found at `lines[i-2]` for the dollar amount, not `lines[i-1]`.

```python
import fitz, re
for i, line in enumerate(lines):
    if 'SKIN NV' in line or 'PAYROLL' in line:
        amt_line = lines[i-2]  # amount is 2 lines before description
        amt_match = re.search(r'[\d,]+\.\d{2}', amt_line)
        if amt_match:
            val = float(amt_match.group().replace(',',''))
```

**Always print surrounding context (5 lines before to 3 lines after) when first searching a new bank's PDF format.** Different banks format differently.

### Income number verification — distrust initial user estimates
Bank statements are ground truth. When the user provides income figures, verify against the actual deposits before building budgets. User estimates of their own income are often approximate. In this case, the user initially estimated his income wrong by 2x and your partner's commission was treated as two separate line items (base + commission) when she's actually all-commission W2.

**Lesson:** Always read the actual bank statements to verify income before building any budgets.

### Color — print-friendly palette
Gold/yellow (`#C9A84C`) prints poorly on white paper. Blue on navy also fails. Use:
- **Section accent:** `#34495E` (dark blue-gray) — reads well on white paper
- **Navy:** `#1E3A5F` (headers, totals)
- **Red for warnings:** `#C0392B`
- **Green for positive:** `#1E8B4C`
- **Light gray:** `#F2F5F9` (zebra rows)

### Income convention used with the user
When the user said "$4,100 a month" he meant gross monthly. He gets $1,500 net per paycheck bi-weekly = $3,075/mo net. Always confirm gross vs. net and pay frequency before building formulas.

### Excel budget tool structure
- Blue-filled cells (`INPUT_BLUE`) = editable inputs
- All totals use `=SUM()` formulas referencing input cells
- Surplus cell has conditional formatting (green >0, red <0)
- Summary section rows reference subtotal cells directly
- When adding a new line item: update BOTH the `subtotal_row` SUM range AND the `rows_to_sum` summary dict AND the surplus formula cell

### PDF ReportLab — section title pattern
```python
story += section_title("Section N — Title Here")
story.append(p("Lead-in paragraph."))
story += sub_title("Sub-heading")
story.append(make_table(data, col_widths))
story.append(spacer(4))
story.append(p("Closing note.", ITALIC))
story.append(PageBreak())
```

### PDF text extraction gotchas
- `body(doc, "text")` does NOT exist — use `story.append(p("text"))` instead
- Section number references get stale — always renumber all subsequent sections when inserting a new one
- Table column alignments use uppercase strings: "LEFT", "RIGHT", "CENTER"

### Key numbers at end of PDF
Always update the Key Numbers section (Section 9) last — it must match every number in the body of the report.

## Files generated
- `/tmp/create_excel_budget.py` — Excel workbook generator
- `/tmp/create_pdf_report.py` — PDF report generator
- Output: `~/Desktop/Awesome-Family-Budget-Tool.xlsx` and `Awesome-Family-Financial-Report.pdf`

## Dependencies
```bash
pip install openpyxl pymupdf reportlab
```
