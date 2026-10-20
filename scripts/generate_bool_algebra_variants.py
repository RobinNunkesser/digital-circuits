#!/usr/bin/env python3
"""
Generates all specialized SVG variants of AusdruckSchaltnetz for 004_BoolescheAlgebra.qmd
from the authentic Digital IEC export (with & and >=1 symbols):
1. Highlight steps: Highlight_None, Highlight_OR, Highlight_Level2, Highlight_Inputs
2. Signal propagation states: Eval_000, Eval_001
3. AusdruckSchaltnetz_Full.svg
"""
import copy
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CIRCUITS_DIR = BASE_DIR / "boolean_algebra"
TEMPLATE_SVG = CIRCUITS_DIR / "AusdruckSchaltnetz.svg"

# ET Namespace helper
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# Palette
DARK_STROKE = "#0f172a"
MUTED_GRAY = "#94a3b8"
ACCENT_GOLD = "#e7ad52"
SIG_LOW = "#7c3aed"    # Purple for 0
SIG_HIGH = "#0284c7"   # Cyan/Blue for 1

def load_template():
    tree = ET.parse(TEMPLATE_SVG)
    root = tree.getroot()
    return tree, root

def set_element_style(element, stroke_color, fill_color=None, stroke_width=None):
    for el in element.iter():
        if "stroke" in el.attrib and el.attrib["stroke"] not in ["none"]:
            el.attrib["stroke"] = stroke_color
        if "fill" in el.attrib:
            if el.attrib["fill"] not in ["none", "#ffffff", "white"]:
                el.attrib["fill"] = fill_color if fill_color else stroke_color
        if stroke_width and "stroke-width" in el.attrib:
            el.attrib["stroke-width"] = str(stroke_width)

def style_svg(tree, active_indices, highlight_color=ACCENT_GOLD, default_color=DARK_STROKE, stroke_width=5.0):
    root = tree.getroot()
    g = root[0]
    for i, child in enumerate(g):
        if i == 23:  # hide test block
            child.attrib["display"] = "none"
            continue
        if i in active_indices:
            set_element_style(child, highlight_color, stroke_width=stroke_width)
        else:
            set_element_style(child, default_color)

def generate_variants():
    # 1. Full clean normalized SVG (all dark)
    full_tree, full_root = load_template()
    g_full = full_root[0]
    for i, child in enumerate(g_full):
        if i == 23:
            child.attrib["display"] = "none"
            continue
        set_element_style(child, DARK_STROKE)
    full_path = CIRCUITS_DIR / "AusdruckSchaltnetz_Full.svg"
    full_tree.write(full_path, encoding="utf-8", xml_declaration=True)
    print(f"Generated {full_path.name}")

    # 2. Highlight_None: identical to clean full circuit
    p_hl_none = CIRCUITS_DIR / "AusdruckSchaltnetz_Highlight_None.svg"
    full_tree.write(p_hl_none, encoding="utf-8", xml_declaration=True)
    print(f"Generated {p_hl_none.name}")

    # 3. Highlight_OR: Gate 5 (OR) and output wire 11 + pin y
    # Gate 5 is index 21, wire 11, pin y is index 22
    t_or, _ = load_template()
    style_svg(t_or, active_indices=[11, 21, 22], highlight_color=ACCENT_GOLD, default_color=MUTED_GRAY, stroke_width=6.0)
    p_hl_or = CIRCUITS_DIR / "AusdruckSchaltnetz_Highlight_OR.svg"
    t_or.write(p_hl_or, encoding="utf-8", xml_declaration=True)
    print(f"Generated {p_hl_or.name}")

    # 4. Highlight_Level2: Gate 2 (AND, idx 18, wire 9) & Gate 4 (OR, idx 20, wire 10)
    t_l2, _ = load_template()
    style_svg(t_l2, active_indices=[9, 10, 18, 20], highlight_color=ACCENT_GOLD, default_color=MUTED_GRAY, stroke_width=6.0)
    p_hl_l2 = CIRCUITS_DIR / "AusdruckSchaltnetz_Highlight_Level2.svg"
    t_l2.write(p_hl_l2, encoding="utf-8", xml_declaration=True)
    print(f"Generated {p_hl_l2.name}")

    # 5. Highlight_Inputs: x0, x1, x2, NOT, Gate 1, Gate 3, and input wires 0..8
    t_inp, _ = load_template()
    style_svg(t_inp, active_indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 19],
              highlight_color=ACCENT_GOLD, default_color=MUTED_GRAY, stroke_width=6.0)
    p_hl_inp = CIRCUITS_DIR / "AusdruckSchaltnetz_Highlight_Inputs.svg"
    t_inp.write(p_hl_inp, encoding="utf-8", xml_declaration=True)
    print(f"Generated {p_hl_inp.name}")

    # 6. Eval_000: x2=0, x1=0, x0=0 -> y=0
    # Inverter output (wires 3, 4) is HIGH (1) -> SIG_HIGH (#0284c7)
    # All other wires (0, 1, 2, 5, 6, 7, 8, 9, 10, 11) are LOW (0) -> SIG_LOW (#7c3aed)
    t_e0, r_e0 = load_template()
    g_e0 = r_e0[0]
    for i, child in enumerate(g_e0):
        if i == 23:
            child.attrib["display"] = "none"
            continue
        set_element_style(child, DARK_STROKE)
    # Color wires
    for w_idx in [3, 4]:
        set_element_style(g_e0[w_idx], SIG_HIGH, stroke_width=5.0)
    for w_idx in [0, 1, 2, 5, 6, 7, 8, 9, 10, 11]:
        set_element_style(g_e0[w_idx], SIG_LOW, stroke_width=5.0)
    p_e0 = CIRCUITS_DIR / "AusdruckSchaltnetz_Eval_000.svg"
    t_e0.write(p_e0, encoding="utf-8", xml_declaration=True)
    print(f"Generated {p_e0.name}")

    # 7. Eval_001: x2=0, x1=0, x0=1 -> y=1
    # x0 rail (wires 0, 1, 2) is HIGH
    # Gate 4 out (wire 10) is HIGH
    # Gate 5 out (wire 11) is HIGH
    # All other wires (3, 4, 5, 6, 7, 8, 9) are LOW
    t_e1, r_e1 = load_template()
    g_e1 = r_e1[0]
    for i, child in enumerate(g_e1):
        if i == 23:
            child.attrib["display"] = "none"
            continue
        set_element_style(child, DARK_STROKE)
    # High wires
    for w_idx in [0, 1, 2, 10, 11]:
        set_element_style(g_e1[w_idx], SIG_HIGH, stroke_width=5.0)
    # Low wires
    for w_idx in [3, 4, 5, 6, 7, 8, 9]:
        set_element_style(g_e1[w_idx], SIG_LOW, stroke_width=5.0)
    p_e1 = CIRCUITS_DIR / "AusdruckSchaltnetz_Eval_001.svg"
    t_e1.write(p_e1, encoding="utf-8", xml_declaration=True)
    print(f"Generated {p_e1.name}")

if __name__ == "__main__":
    generate_variants()
