---
name: contact-merge-dedup
description: Merge and deduplicate contacts from multiple sources (Excel XLSX, PDF, CSV) with US phone number normalization and conflict resolution. Used for Skin NV beauty bash campaign — 223 contacts merged from Excel + PDF.
version: 1.0.0
tags: [contacts, excel, pdf, csv, dedup, sms]
author: Hermes Agent
---

# Contact Merge & Deduplication

Merge contacts from multiple sources (Excel, PDF, CSV) into a single deduplicated list with US phone number normalization.

## When to Use

- Two or more contact lists need to be combined
- Phone numbers need standardization (+1 format)
- Same person may appear in multiple files with different numbers
- Importing into SimpleTexting, Mailchimp, or similar platform

## Prerequisites

```bash
pip3 install openpyxl pymupdf  # excel and pdf parsing
```

## Complete Working Script

```python
import openpyxl
import fitz
import re
import csv

# ============================================================
# US/NANP VALID AREA CODES
# Complete list — do not prune
# ============================================================
VALID_AREA_CODES = {
    201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 212, 213, 214, 215, 216, 217, 218, 219,
    224, 225, 226, 228, 229, 231, 234, 239, 240, 242, 246, 248, 249, 251, 252, 253, 254, 256,
    260, 262, 267, 269, 270, 272, 276, 281, 301, 302, 303, 304, 305, 307, 308, 309, 310, 312,
    313, 314, 315, 316, 317, 318, 319, 320, 321, 323, 325, 327, 330, 331, 334, 336, 337, 338,
    339, 341, 346, 347, 351, 352, 353, 360, 361, 364, 369, 380, 385, 386, 401, 402, 404, 405,
    406, 407, 408, 409, 410, 412, 413, 414, 415, 417, 419, 423, 424, 425, 430, 432, 435, 440,
    442, 443, 445, 447, 464, 469, 470, 475, 478, 479, 480, 484, 501, 502, 503, 504, 505, 507,
    508, 509, 512, 513, 515, 516, 517, 518, 520, 530, 531, 534, 539, 540, 541, 551, 557, 559,
    561, 562, 564, 567, 570, 571, 573, 574, 575, 580, 585, 586, 601, 602, 603, 605, 606, 607,
    608, 609, 610, 612, 614, 615, 616, 617, 618, 619, 620, 623, 626, 628, 630, 631, 636, 640,
    641, 646, 647, 649, 651, 657, 660, 661, 662, 667, 669, 678, 680, 681, 682, 689, 701, 702,
    703, 704, 706, 707, 708, 710, 712, 713, 714, 715, 716, 718, 719, 720, 724, 727, 731, 732,
    734, 737, 740, 743, 747, 752, 754, 757, 758, 760, 762, 763, 765, 769, 770, 772, 773, 774,
    775, 779, 781, 785, 786, 801, 802, 803, 804, 805, 806, 808, 810, 812, 813, 814, 815, 816,
    817, 818, 819, 820, 828, 830, 831, 832, 833, 835, 843, 845, 847, 848, 850, 852, 856, 857,
    858, 859, 860, 862, 863, 864, 865, 866, 870, 872, 878, 901, 903, 904, 906, 907, 908, 909,
    910, 912, 913, 914, 915, 916, 917, 918, 919, 920, 925, 928, 929, 931, 935, 936, 937, 939,
    940, 941, 947, 949, 951, 952, 954, 956, 959, 970, 971, 972, 973, 978, 979, 980, 984, 985,
    989,
    # US territories
    340, 441, 467, 664, 670, 671, 684, 758, 767, 784, 787, 868, 869, 876, 939
}

def is_valid_us_phone(digits):
    """Check if this is a valid NANP US phone number."""
    if len(digits) == 11 and digits[0] == '1':
        return int(digits[1:4]) in VALID_AREA_CODES
    elif len(digits) == 10:
        return int(digits[0:3]) in VALID_AREA_CODES
    return False

def normalize_phone(raw):
    """Normalize to +1XXXXXXXXXX format. Return None if invalid."""
    digits = re.sub(r'[^\d]', '', str(raw))
    if len(digits) == 11 and digits[0] == '1' and is_valid_us_phone(digits):
        return '+' + digits
    elif len(digits) == 10 and is_valid_us_phone(digits):
        return '+1' + digits
    return None

def format_phone_display(phone):
    """Format as +1 (XXX) XXX-XXXX"""
    d = re.sub(r'[^\d]', '', phone)
    if len(d) == 11:
        return f"+1 ({d[1:4]}) {d[4:7]}-{d[7:]}"
    return phone

def normalize_name(name):
    """Normalize name for matching: lowercase, strip, remove asterisks."""
    name = str(name).strip()
    name = re.sub(r' \*+', '', name)
    name = re.sub(r"[''']", '', name)
    return name.lower().strip()

# ============================================================
# READ EXCEL
# ============================================================
def read_excel(path):
    """Returns dict: normalized_name -> (original_name, phone)"""
    contacts = {}
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows(values_only=True):
        name, phone_raw = row[0], row[1]
        if name and name != 'NAME' and phone_raw:
            original_name = re.sub(r' \*+', '', str(name).strip())
            phone = normalize_phone(phone_raw)
            if phone:
                contacts[normalize_name(original_name)] = (original_name, phone)
    return contacts

# ============================================================
# READ PDF (alternating name/phone pattern)
# ============================================================
def read_pdf(path):
    """Returns dict: normalized_name -> (original_name, phone)"""
    contacts = {}
    doc = fitz.open(path)
    for page_num, page in enumerate(doc):
        lines = [l.strip() for l in page.get_text().split('\n') if l.strip()]
        # Page 1 has title + 2 header rows before pairs start at index 3
        # Pages 2+ start with name/phone pairs immediately
        start_idx = 3 if page_num == 0 else 0
        for i in range(start_idx, len(lines) - 1, 2):
            name = lines[i]
            phone_raw = lines[i+1]
            phone = normalize_phone(phone_raw)
            if phone and name:
                contacts[normalize_name(name)] = (name.strip(), phone)
    return contacts

# ============================================================
# MERGE with conflict resolution
# newer_source: 'pdf' or 'excel' — which source wins on name match with different numbers
# ============================================================
def merge_contacts(sources, newer_source='pdf'):
    """
    sources: list of (name, contacts_dict) tuples where contacts_dict
             maps normalized_name -> (original_name, phone)
    newer_source: which source wins when same name has different numbers
    Returns: final dict
    """
    final = {}
    for source_name, source_contacts in sources:
        for key, (name, phone) in source_contacts.items():
            if key in final:
                old_phone = final[key][1]
                if old_phone != phone:
                    # Conflict: same name, different number
                    final[key] = (name, phone, source_name) if source_name == newer_source \
                                 else (final[key][0], old_phone, final[key][2])
            else:
                final[key] = (name, phone, source_name)
    return final

# ============================================================
# WRITE OUTPUT CSV
# ============================================================
def write_csv(output_path, contacts):
    """Write contacts dict to SimpleTexting-compatible CSV."""
    sorted_contacts = sorted(contacts.items(), key=lambda x: x[1][0].lower())
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['First Name', 'Last Name', 'Phone', 'Source'])
        for key, (name, phone, source) in sorted_contacts:
            parts = name.split(maxsplit=1)
            first, last = (parts[0], parts[1]) if len(parts) == 2 else (name, '')
            writer.writerow([first, last, format_phone_display(phone), source])

# ============================================================
# EXAMPLE USAGE
# ============================================================
if __name__ == '__main__':
    excel = read_excel('/path/to/contacts.xlsx')
    pdf = read_pdf('/path/to/contacts.pdf')
    merged = merge_contacts([('excel', excel), ('pdf', pdf)], newer_source='pdf')
    write_csv('/path/to/output.csv', merged)
    print(f"Total: {len(merged)} contacts")
```

## Key Learnings (from Skin NV campaign)

**PDF parsing pitfalls:**
- Page 1 of PDF had 3 header rows before data; pages 2+ start directly with name/phone pairs
- Always verify pair count vs actual entries — Joanne Elayoubi was missed in first attempt
- OCR garbage names appear (e.g., "Troy Oichteneerter" was a mangled phone+name)

**Phone validation:**
- Area code list must be complete — missing 929 (NYC), 330 (Ohio), 236 (Canada), etc.
- PDF numbers often lack leading + (e.g., `18322886802` = `1` + `8322886802` not `183` area code)
- `683` and `656` are NOT valid NANP US area codes

**Name matching:**
- Normalize names (lowercase, strip asterisks, smart quotes) for dedup matching
- Some people appear with slightly different name spellings across sources
- "Alliyah" vs "Aliyah" = same person usually

**Output format for SimpleTexting:**
- Headers: `First Name`, `Last Name`, `Phone`
- Phone: +1XXXXXXXXXX or (XXX) XXX-XXXX — SimpleTexting parses both
- Google Sheets: prefix `+1` numbers with `'` to prevent formula interpretation

## Verified Valid NANP Area Codes Notes
- 929 = Brooklyn/Queens NYC (valid)
- 330 = Ohio Akron/Canton (valid)
- 236 = Canada BC (NOT US — reject)
- 332 = not a real area code
- 656 = Dominican Republic (NOT US — reject)
- 683 = not a real area code
- 727 = St. Petersburg/Clearwater FL (valid, Pinellas — neighbor to 813 Tampa)
- 832 = Houston TX (valid)
- 941 = Sarasota/Bradenton FL (valid)
