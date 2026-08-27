#!/usr/bin/env python3
"""
postprocess_mineru.py - Post-process MinerU 3.4.5 output to fix 3 quality issues:

1. Heading hierarchy: Map section numbers to heading levels
   - X       -> #     (chapter)
   - X.Y     -> ##    (section)
   - X.Y.Z   -> ###   (subsection)
   - X.Y.Z.W -> ####  (sub-subsection) [only if NOT a bit field]
   - Chapter N -> #   (chapter)

2. Bit field flattening: Convert bit-field headings to bold inline labels
   Detects patterns:
   - [N], [N:M], [N : M]                    e.g. STATUS[0], CTRL[5:2], ARCH VER[1:0]
   - \\left[ ... \\right]                     e.g. $\\left[ X _ { d } \\right]$
   - [Name<sub>...</sub>]                    e.g. [X<sub>d</sub>], [VA<sub>d</sub>]
   - $<latex_name>$ [N:M]                    e.g. $X _ { m }$ [63 : 60]
   Output: **LABEL**\nDESCRIPTION  (label on its own line, description on next line)

3. Algorithm code blocks: Wrap ALL type=code entries in ``` blocks
   MinerU 3.4.5 bug: sub_type=algorithm entries are emitted as plain text.
   Fix: wrap code_body in ``` regardless of sub_type.

Usage:
    python3 postprocess_mineru.py <content_list.json> <output.md>
    python3 postprocess_mineru.py <directory_with_content_list>   # auto-detect, writes <basename>_fixed.md

Input:  content_list.json from MinerU 3.4.5 (md_output/<pdf_basename>/auto/<basename>_content_list.json)
Output: corrected Markdown file

Skips: type=header, type=footer, type=page_number (running heads/feet, not content)
Preserves: HTML tables (MinerU's existing behavior), images, equations (LaTeX), charts
"""
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Bit field detection
# ---------------------------------------------------------------------------
BIT_RANGE_RE = re.compile(r'\[\s*\d+\s*(?::\s*\d+\s*)?\]')
LATEX_BRACKET_RE = re.compile(r'\\left\[.*?\\right\]')
WHOLE_NAME_BRACKET_RE = re.compile(
    r'\[[A-Za-z][A-Za-z ]*(?:<sub>[^<]+</sub>)?\]'
)
SECTION_NUM_PREFIX_RE = re.compile(r'^\d+(?:\.\d+)*\s+')

# A bit field HEADING is short: just the name + bit designation.
# A description paragraph that happens to start with a bit-field pattern
# (e.g., "X<sub>t</sub>[31 : 16] Is the unsigned dst stride of ...") must NOT
# be treated as a heading. We use two guards:
#   1. Length: stripped text must be short (< 60 chars)
#   2. Position: the bracket match must be at the END of the text, OR the
#      bracket must wrap the ENTIRE content (no trailing sentence after it).
MAX_BITFIELD_HEADING_LEN = 60

def is_bit_field(text):
    """Return True if text looks like a bit field HEADING (not a description).

    A bit field heading is a SHORT text entry whose content (after an optional
    leading section number) is either:
      - <name>[<bit_range>]            (bracket at the end), e.g. STATUS[0], CTRL[5:2]
      - [<name><sub>...</sub>]         (bracket wraps entire content), e.g. [X<sub>d</sub>]
      - $\\left[ ... \\right]$          (LaTeX bracket wraps entire content)
    Descriptions like "X<sub>t</sub>[31 : 16] Is the unsigned dst stride of ..."
    are rejected because:
      (a) they exceed MAX_BITFIELD_HEADING_LEN, AND
      (b) the bracket is followed by non-trivial prose, not end-of-string.
    """
    if not text:
        return False
    t = SECTION_NUM_PREFIX_RE.sub('', text.strip())
    if len(t) >= MAX_BITFIELD_HEADING_LEN:
        return False

    # Case 1: bit range [N] or [N:M] at the END of the text
    m = BIT_RANGE_RE.search(t)
    if m:
        # Everything after the match must be whitespace only
        if t[m.end():].strip() == '':
            return True

    # Case 2: LaTeX \left[ ... \right] wrapping the whole content
    m = LATEX_BRACKET_RE.search(t)
    if m:
        before = t[:m.start()].strip()
        after = t[m.end():].strip()
        # The LaTeX bracket must be the whole content (allow leading $ ... $)
        # Accept: "$\left[ ... \right]$" or "$\left[ ... \right]$ something_short"
        if before in ('', '$') and after in ('', '$'):
            return True

    # Case 3: whole-name bracket [<name><sub>...</sub>] wrapping the entire content
    m = WHOLE_NAME_BRACKET_RE.search(t)
    if m:
        before = t[:m.start()].strip()
        after = t[m.end():].strip()
        if before == '' and after == '':
            return True

    return False

def clean_label(text):
    """Strip leading section number and collapse whitespace from a bit field label."""
    t = SECTION_NUM_PREFIX_RE.sub('', text.strip())
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

# ---------------------------------------------------------------------------
# Section heading detection
# ---------------------------------------------------------------------------
SECTION_NUM_RE = re.compile(r'^(\d+(?:\.\d+)*)\s+\S')
CHAPTER_RE = re.compile(r'^Chapter\s+\d+', re.IGNORECASE)

def get_heading_level(text):
    """Return heading level (1-4) for a section-numbered heading, else None.

    X       -> 1
    X.Y     -> 2
    X.Y.Z   -> 3
    X.Y.Z.W -> 4
    Chapter N -> 1
    """
    t = text.strip()
    if CHAPTER_RE.match(t):
        return 1
    m = SECTION_NUM_RE.match(t)
    if not m:
        return None
    parts = m.group(1).split('.')
    return min(len(parts), 4)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
SKIPPABLE_TYPES = {'header', 'footer', 'page_number'}

def _flatten_caption(cap):
    """caption/footnote fields can be a list or a string; normalize to a single string."""
    if not cap:
        return ''
    if isinstance(cap, list):
        return ' '.join(str(c).strip() for c in cap if c and str(c).strip())
    return str(cap).strip()

def _is_empty_text_entry(e):
    return e.get('type') == 'text' and not (e.get('text', '') or '').strip()

def _is_next_heading_or_bitfield(entries, j):
    """Check if entry at index j is a heading or bit field (i.e., should stop description search)."""
    if j >= len(entries):
        return True
    ne = entries[j]
    if ne.get('type') in SKIPPABLE_TYPES:
        return False  # skip past these
    if ne.get('type') != 'text':
        return True  # non-text entry ends the description search
    nt = (ne.get('text', '') or '').strip()
    if not nt:
        return False  # empty text - keep looking
    if is_bit_field(nt) or get_heading_level(nt) is not None:
        return True
    return False

# ---------------------------------------------------------------------------
# Main processor
# ---------------------------------------------------------------------------
def process(entries):
    """Process content_list entries and emit corrected Markdown."""
    out = []
    i = 0
    n = len(entries)

    while i < n:
        e = entries[i]
        etype = e.get('type')

        # Skip running headers/footers/page numbers
        if etype in SKIPPABLE_TYPES:
            i += 1
            continue

        # ---------------- TEXT ----------------
        if etype == 'text':
            text = (e.get('text', '') or '').strip()
            if not text:
                i += 1
                continue

            # Bit field -> bold label on its own line + description on next line
            if is_bit_field(text):
                label = clean_label(text)
                # Find next non-skippable, non-heading, non-bitfield text entry as description
                j = i + 1
                description = ''
                consumed_idx = None
                while j < n:
                    if _is_next_heading_or_bitfield(entries, j):
                        break
                    ne = entries[j]
                    if ne.get('type') == 'text':
                        nt_text = (ne.get('text', '') or '').strip()
                        if nt_text:
                            description = nt_text
                            consumed_idx = j
                            break
                    j += 1

                if description:
                    # Label on its own line (no trailing \n so join puts no blank line before description)
                    out.append(f"**{label}**")
                    out.append(f"{description}\n")
                    # Consume the description entry; continue AFTER it
                    i = consumed_idx + 1 if consumed_idx is not None else i + 1
                else:
                    out.append(f"**{label}**\n")
                    i += 1
                continue

            # Section heading -> proper level
            level = get_heading_level(text)
            if level is not None:
                hashes = '#' * level
                out.append(f"{hashes} {text}\n")
                i += 1
                continue

            # Plain paragraph
            out.append(f"{text}\n")
            i += 1
            continue

        # ---------------- CODE ----------------
        if etype == 'code':
            body = (e.get('code_body', '') or '').strip()
            cap = _flatten_caption(e.get('code_caption'))
            foot = _flatten_caption(e.get('code_footnote'))

            if cap:
                out.append(f"{cap}\n")

            if body:
                # Preserve existing code fence if code_body already starts with ```
                if body.startswith('```'):
                    if not body.endswith('```'):
                        body = body + '\n```'
                    out.append(f"{body}\n")
                else:
                    out.append(f"```\n{body}\n```\n")

            if foot:
                out.append(f"{foot}\n")

            i += 1
            continue

        # ---------------- TABLE ----------------
        if etype == 'table':
            body = (e.get('table_body', '') or '').strip()
            cap = _flatten_caption(e.get('table_caption'))
            foot = _flatten_caption(e.get('table_footnote'))

            if cap:
                out.append(f"{cap}\n")
            if body:
                out.append(f"{body}\n")
            if foot:
                out.append(f"{foot}\n")
            i += 1
            continue

        # ---------------- IMAGE ----------------
        if etype == 'image':
            img_path = e.get('img_path', '')
            cap = _flatten_caption(e.get('image_caption'))
            foot = _flatten_caption(e.get('image_footnote'))

            if cap:
                out.append(f"{cap}\n")
            if img_path:
                out.append(f"![]({img_path})\n")
            if foot:
                out.append(f"{foot}\n")
            i += 1
            continue

        # ---------------- EQUATION ----------------
        if etype == 'equation':
            text = (e.get('text', '') or '').strip()
            if text:
                # Equation text already includes $$ delimiters from MinerU
                out.append(f"{text}\n")
            i += 1
            continue

        # ---------------- CHART ----------------
        if etype == 'chart':
            img_path = e.get('img_path', '')
            cap = _flatten_caption(e.get('chart_caption'))
            foot = _flatten_caption(e.get('chart_footnote'))

            if cap:
                out.append(f"{cap}\n")
            if img_path:
                out.append(f"![]({img_path})\n")
            if foot:
                out.append(f"{foot}\n")
            i += 1
            continue

        # Unknown type - skip
        i += 1

    return '\n'.join(out)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def find_content_list(dir_path):
    """Find the *_content_list.json file in a directory (excluding *_content_list_v2.json)."""
    p = Path(dir_path)
    candidates = sorted(p.glob('*_content_list.json'))
    # Exclude _v2 variant
    candidates = [c for c in candidates if not c.name.endswith('_v2.json')]
    if not candidates:
        raise FileNotFoundError(f"No *_content_list.json found in {dir_path}")
    return candidates[0]

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg1 = sys.argv[1]
    arg1_path = Path(arg1)

    # Auto-detect: if arg1 is a directory, find content_list.json inside
    if arg1_path.is_dir():
        clpath = find_content_list(arg1_path)
        # Output: <dir>/<basename>_fixed.md
        basename = clpath.name.replace('_content_list.json', '')
        outpath = arg1_path / f"{basename}_fixed.md"
    elif arg1_path.is_file() and arg1_path.suffix == '.json':
        clpath = arg1_path
        if len(sys.argv) >= 3:
            outpath = Path(sys.argv[2])
        else:
            outpath = arg1_path.parent / arg1_path.name.replace('_content_list.json', '_fixed.md')
    else:
        print(f"Error: {arg1} is not a directory or JSON file")
        sys.exit(1)

    print(f"Reading: {clpath}")
    with open(clpath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Processing {len(data)} entries...")
    result = process(data)

    print(f"Writing: {outpath}")
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(result)

    # Report stats
    lines = result.count('\n') + 1
    chars = len(result)
    print(f"Done: {lines} lines, {chars} chars")

    # Quick stats on output
    h1 = result.count('\n# ') + (1 if result.startswith('# ') else 0)
    h2 = result.count('\n## ') + (1 if result.startswith('## ') else 0)
    h3 = result.count('\n### ') + (1 if result.startswith('### ') else 0)
    h4 = result.count('\n#### ') + (1 if result.startswith('#### ') else 0)
    bold_labels = len(re.findall(r'\n\*\*[^*]+\[[^*]*\*\*\n', result))
    code_blocks = result.count('```\n')
    print(f"  # headings:   {h1}")
    print(f"  ## headings:  {h2}")
    print(f"  ### headings: {h3}")
    print(f"  #### headings: {h4}")
    print(f"  Bit field bold labels: {bold_labels}")
    print(f"  Code blocks (``` pairs): {code_blocks // 2}")

if __name__ == '__main__':
    main()
