#!/usr/bin/env python3
"""
Generates clean vector SVG diagrams for the switch circuits in 004_BoolescheAlgebra.qmd:
- Schalter_Einfach.svg (single switch)
- Schalter_AND.svg (series switches)
- Schalter_OR.svg (parallel switches)
- Schalter_NOT.svg (bypass switch)
"""
from pathlib import Path

DEST_DIR = Path(__file__).resolve().parent.parent / "boolean_algebra"
DEST_DIR.mkdir(parents=True, exist_ok=True)

STROKE = "#0f172a"
STROKE_WIDTH = 3
FONT_FAMILY = "system-ui, -apple-system, sans-serif"

def header(width=340, height=180):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}px">
  <defs>
    <style>
      .wire {{ stroke: {STROKE}; stroke-width: {STROKE_WIDTH}; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
      .component {{ stroke: {STROKE}; stroke-width: {STROKE_WIDTH}; fill: #ffffff; }}
      .lbl {{ font-family: {FONT_FAMILY}; font-size: 16px; font-weight: bold; fill: {STROKE}; text-anchor: middle; }}
      .lbl-sub {{ font-family: {FONT_FAMILY}; font-size: 13px; font-weight: bold; fill: {STROKE}; text-anchor: middle; }}
    </style>
  </defs>
'''

def footer():
    return "</svg>\n"

def draw_battery(x, y, label="Spannungsquelle"):
    return f'''  <!-- Voltage Source -->
  <circle cx="{x}" cy="{y}" r="22" class="component"/>
  <line x1="{x-8}" y1="{y-8}" x2="{x+8}" y2="{y-8}" class="wire"/>
  <line x1="{x}" y1="{y-16}" x2="{x}" y2="{y}" class="wire"/>
  <line x1="{x-8}" y1="{y+10}" x2="{x+8}" y2="{y+10}" class="wire"/>
  <text x="{x+35}" y="{y+5}" class="lbl" style="text-anchor: start; font-size: 14px;">{label}</text>
'''

def draw_lamp(x, y, label="l"):
    return f'''  <!-- Lamp -->
  <circle cx="{x}" cy="{y}" r="20" class="component"/>
  <line x1="{x-14}" y1="{y-14}" x2="{x+14}" y2="{y+14}" class="wire"/>
  <line x1="{x-14}" y1="{y+14}" x2="{x+14}" y2="{y-14}" class="wire"/>
  <text x="{x+32}" y="{y+6}" class="lbl" style="text-anchor: start; font-size: 18px; font-style: italic;">{label}</text>
'''

def draw_switch(x1, y, x2, label="s", open_angle=True):
    sw_len = x2 - x1
    arm_x = x1 + sw_len - 4 if not open_angle else x1 + sw_len * 0.8
    arm_y = y if not open_angle else y - 18
    return f'''  <!-- Switch {label} -->
  <circle cx="{x1}" cy="{y}" r="4" class="component"/>
  <circle cx="{x2}" cy="{y}" r="4" class="component"/>
  <line x1="{x1+2}" y1="{y-2}" x2="{arm_x}" y2="{arm_y}" class="wire"/>
  <text x="{(x1+x2)/2}" y="{y+24}" class="lbl" style="font-size: 18px; font-style: italic;">{label}</text>
'''

def make_simple():
    svg = header(320, 180)
    svg += '<path d="M 50,68 L 50,30 L 120,30" class="wire"/>\n'
    svg += draw_switch(120, 30, 180, "s")
    svg += '<path d="M 180,30 L 250,30 L 250,70" class="wire"/>\n'
    svg += draw_lamp(250, 90, "l")
    svg += '<path d="M 250,110 L 250,150 L 50,150 L 50,112" class="wire"/>\n'
    svg += draw_battery(50, 90)
    svg += footer()
    (DEST_DIR / "Schalter_Einfach.svg").write_text(svg, encoding="utf-8")

def make_and():
    svg = header(380, 180)
    svg += '<path d="M 50,68 L 50,30 L 100,30" class="wire"/>\n'
    svg += draw_switch(100, 30, 160, "s₁")
    svg += '<path d="M 160,30 L 200,30" class="wire"/>\n'
    svg += draw_switch(200, 30, 260, "s₂")
    svg += '<path d="M 260,30 L 310,30 L 310,70" class="wire"/>\n'
    svg += draw_lamp(310, 90, "l")
    svg += '<path d="M 310,110 L 310,150 L 50,150 L 50,112" class="wire"/>\n'
    svg += draw_battery(50, 90)
    svg += footer()
    (DEST_DIR / "Schalter_AND.svg").write_text(svg, encoding="utf-8")

def make_or():
    svg = header(380, 220)
    svg += '<path d="M 50,88 L 50,30 L 100,30 L 100,50 L 130,50" class="wire"/>\n'
    svg += '<path d="M 100,30 L 100,90 L 130,90" class="wire"/>\n'
    svg += draw_switch(130, 50, 190, "s₁")
    svg += draw_switch(130, 90, 190, "s₂")
    svg += '<path d="M 190,50 L 220,50 L 220,30 L 300,30 L 300,90" class="wire"/>\n'
    svg += '<path d="M 190,90 L 220,90 L 220,30" class="wire"/>\n'
    svg += draw_lamp(300, 110, "l")
    svg += '<path d="M 300,130 L 300,180 L 50,180 L 50,132" class="wire"/>\n'
    svg += draw_battery(50, 110)
    svg += footer()
    (DEST_DIR / "Schalter_OR.svg").write_text(svg, encoding="utf-8")

def make_not():
    svg = header(380, 210)
    # Voltage source left, lamp right with series resistor/load wire, switch in parallel to bypass lamp
    svg += '<path d="M 50,88 L 50,30 L 150,30 L 300,30 L 300,90" class="wire"/>\n'
    svg += '<path d="M 150,30 L 150,60" class="wire"/>\n'
    svg += draw_switch(150, 60, 150, "s", open_angle=True) # or horizontal
    # Let horizontal parallel branch:
    svg_not = header(380, 210)
    svg_not += '<path d="M 50,88 L 50,30 L 130,30" class="wire"/>\n'
    svg_not += '<!-- Parallel switch branch -->\n'
    svg_not += '<path d="M 130,30 L 130,80 L 160,80" class="wire"/>\n'
    svg_not += draw_switch(160, 80, 220, "s")
    svg_not += '<path d="M 220,80 L 250,80 L 250,170" class="wire"/>\n'
    svg_not += '<!-- Main lamp branch -->\n'
    svg_not += '<path d="M 130,30 L 310,30 L 310,80" class="wire"/>\n'
    svg_not += draw_lamp(310, 100, "l")
    svg_not += '<path d="M 310,120 L 310,170 L 50,170 L 50,132" class="wire"/>\n'
    svg_not += draw_battery(50, 110)
    svg_not += footer()
    (DEST_DIR / "Schalter_NOT.svg").write_text(svg_not, encoding="utf-8")

def main():
    make_simple()
    make_and()
    make_or()
    make_not()
    print("Generated switch circuit SVGs.")

if __name__ == "__main__":
    main()
