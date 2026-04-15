---
name: excel-budget-tool-openpyxl
description: Build interactive multi-sheet Excel budget/workbook tools with openpyxl — editable blue input cells, formula-driven totals, and conditional formatting.
category: productivity
---

# Excel Interactive Budget Tool with openpyxl

## When to Use
Build a multi-sheet Excel workbook with:
- Editable input cells (visually distinct, e.g. blue fill)
- Formula-driven summary rows that auto-update
- Conditional formatting (green/red based on positive/negative values)
- Zebra-striped data rows, color-coded section headers
- No gridlines, proper column widths

## Install
```bash
pip3 install openpyxl
```

## Core Pattern — Single sheet
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Sheet Name"
ws.sheet_view.showGridLines = False

# Colors as hex strings
NAVY = "1E3A5F"; GOLD = "C9A84C"; WHITE = "FFFFFF"
LIGHT_GRAY = "F2F5F9"; INPUT_BLUE = "EBF5FB"

def thin_border():
    s = Side(style='thin', color="AAAAAA")
    return Border(left=s, right=s, top=s, bottom=s)

def hdr_fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

# Title bar (merged, colored)
ws.merge_cells("A1:D1")
t = ws.cell(row=1, column=1, value="TITLE")
t.font = Font(bold=True, size=14, color=WHITE)
t.fill = hdr_fill(NAVY)
t.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 32

# Column headers
def header_row(ws, row, texts, bg=NAVY, fg=WHITE):
    for col, text in enumerate(texts, 1):
        c = ws.cell(row=row, column=col, value=text)
        c.fill = hdr_fill(bg)
        c.font = Font(bold=True, color=fg, size=10)
        c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        c.border = thin_border()

# Data row with optional input columns
def data_row(ws, row, values, input_cols=None, bg=LIGHT_GRAY):
    for col, val in enumerate(values, 1):
        c = ws.cell(row=row, column=col, value=val)
        c.border = thin_border()
        c.alignment = Alignment(horizontal="left", vertical="center")
        if input_cols and col in input_cols:
            c.fill = hdr_fill(INPUT_BLUE)
            c.font = Font(color="1A5276", size=10)
        else:
            c.fill = hdr_fill(bg if row % 2 == 0 else WHITE)
            c.font = Font(size=10)

# Subtotal row (gray background, bold)
def subtotal_row(ws, row, label, formula_or_val, col=2):
    c_lbl = ws.cell(row=row, column=1, value=label)
    c_lbl.font = Font(bold=True, size=10)
    c_lbl.fill = hdr_fill("D9D9D9")
    c_lbl.border = thin_border()
    c_val = ws.cell(row=row, column=col, value=formula_or_val)
    c_val.font = Font(bold=True, size=10, color=NAVY)
    c_val.fill = hdr_fill("D9D9D9")
    c_val.border = thin_border()
    c_val.number_format = '#,##0.00'
    # fill remaining cols
    for col_i in range(3, 5):
        ws.cell(row=row, column=col_i).fill = hdr_fill("D9D9D9")
        ws.cell(row=row, column=col_i).border = thin_border()
    ws.row_dimensions[row].height = 18

# Section header (colored banner, can merge across columns)
def section_header(ws, row, text, span_cols=4, bg=GOLD, fg=WHITE):
    c = ws.cell(row=row, column=1, value=text)
    c.fill = hdr_fill(bg)
    c.font = Font(bold=True, color=fg, size=11)
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 20
    if span_cols > 1:
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span_cols)
    for col_i in range(2, span_cols + 1):
        ws.cell(row=row, column=col_i).fill = hdr_fill(bg)
```

## Conditional Formatting (surplus/deficit cells)
```python
ws.conditional_formatting.add(
    "B71",  # cell to watch
    CellIsRule(operator="greaterThan", formula=["0"],
               fill=PatternFill("solid", fgColor="A9DFBF"),  # green
               font=Font(bold=True, color="0E6136"))
)
ws.conditional_formatting.add(
    "B71",
    CellIsRule(operator="lessThan", formula=["0"],
               fill=PatternFill("solid", fgColor="F1948A"),   # red
               font=Font(bold=True, color="7B241C"))
)
```

## Formula Best Practices
- Use `=SUM(B7:B9)` for ranges
- Surplus formula: `=B12-B17-B22-B27-B35-B44-B55-B59` (income minus all categories)
- Months-to-payoff: `=CEILING(B{i}/D{i},1)` — rounds up to nearest month
- Reference subtotal cells directly rather than re-summing ranges in summary rows
- For a multi-sheet workbook, each `ws = wb.create_sheet("Name")` gets its own setup block

## Common Bugs
1. **Unused import causes NameError** — remove `from openpyxl.styles.numbers import FORMAT_NUMBER_COMMA_SEP1` if not used; some versions error on unused imports.
2. **Merged cells** — only set value/border/fill on the top-left cell of a merge range.
3. **Number format** — always set `number_format` after setting the value, not before.

## Save
```python
wb.save("/path/to/output.xlsx")
```

## Verification
Open in Excel or LibreOffice Calc and:
1. Change a blue input cell → verify totals update
2. Check surplus cell turns green when positive, red when negative
3. Confirm all formula rows reference correct source cells
