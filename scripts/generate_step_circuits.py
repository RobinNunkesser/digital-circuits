#!/usr/bin/env python3
"""
Generates valid, standalone Digital (.dig) circuit files for each synthesis step:
- AusdruckSchaltnetz_Step1.dig (Out y)
- AusdruckSchaltnetz_Step2.dig (Root OR gate -> Out y)
- AusdruckSchaltnetz_Step3.dig (Level 2 AND & OR gates -> Root OR -> Out y)
- AusdruckSchaltnetz_Step4.dig (Input x0, inverter, Stage 1 gates -> Stage 2 -> Out y)
- AusdruckSchaltnetz_Step5.dig (Full circuit with all inputs x0, x1, x2)
"""
from pathlib import Path
import subprocess

CIRCUITS_DIR = Path(__file__).resolve().parent.parent / "boolean_algebra"
DIGITAL_JAR = Path("/Applications/Digital/Digital.jar")

def create_step1_dig():
    return """<?xml version="1.0" encoding="utf-8"?>
<circuit>
  <version>1</version>
  <attributes/>
  <visualElements>
    <visualElement>
      <elementName>Out</elementName>
      <elementAttributes>
        <entry>
          <string>Label</string>
          <string>y</string>
        </entry>
      </elementAttributes>
      <pos x="680" y="320"/>
    </visualElement>
  </visualElements>
  <wires>
    <wire>
      <p1 x="640" y="320"/>
      <p2 x="680" y="320"/>
    </wire>
  </wires>
</circuit>
"""

def create_step2_dig():
    return """<?xml version="1.0" encoding="utf-8"?>
<circuit>
  <version>1</version>
  <attributes/>
  <visualElements>
    <visualElement>
      <elementName>Or</elementName>
      <elementAttributes/>
      <pos x="580" y="300"/>
    </visualElement>
    <visualElement>
      <elementName>Out</elementName>
      <elementAttributes>
        <entry>
          <string>Label</string>
          <string>y</string>
        </entry>
      </elementAttributes>
      <pos x="680" y="320"/>
    </visualElement>
  </visualElements>
  <wires>
    <wire>
      <p1 x="540" y="300"/>
      <p2 x="580" y="300"/>
    </wire>
    <wire>
      <p1 x="540" y="340"/>
      <p2 x="580" y="340"/>
    </wire>
    <wire>
      <p1 x="640" y="320"/>
      <p2 x="680" y="320"/>
    </wire>
  </wires>
</circuit>
"""

def create_step3_dig():
    return """<?xml version="1.0" encoding="utf-8"?>
<circuit>
  <version>1</version>
  <attributes/>
  <visualElements>
    <visualElement>
      <elementName>And</elementName>
      <elementAttributes/>
      <pos x="460" y="240"/>
    </visualElement>
    <visualElement>
      <elementName>Or</elementName>
      <elementAttributes/>
      <pos x="460" y="360"/>
    </visualElement>
    <visualElement>
      <elementName>Or</elementName>
      <elementAttributes/>
      <pos x="580" y="300"/>
    </visualElement>
    <visualElement>
      <elementName>Out</elementName>
      <elementAttributes>
        <entry>
          <string>Label</string>
          <string>y</string>
        </entry>
      </elementAttributes>
      <pos x="680" y="320"/>
    </visualElement>
  </visualElements>
  <wires>
    <!-- Gate 2 inputs -->
    <wire>
      <p1 x="400" y="240"/>
      <p2 x="460" y="240"/>
    </wire>
    <wire>
      <p1 x="400" y="280"/>
      <p2 x="460" y="280"/>
    </wire>
    <!-- Gate 4 inputs -->
    <wire>
      <p1 x="400" y="360"/>
      <p2 x="460" y="360"/>
    </wire>
    <wire>
      <p1 x="400" y="400"/>
      <p2 x="460" y="400"/>
    </wire>
    <!-- Gate 2 to Gate 5 -->
    <wire>
      <p1 x="520" y="260"/>
      <p2 x="540" y="260"/>
    </wire>
    <wire>
      <p1 x="540" y="260"/>
      <p2 x="540" y="300"/>
    </wire>
    <wire>
      <p1 x="540" y="300"/>
      <p2 x="580" y="300"/>
    </wire>
    <!-- Gate 4 to Gate 5 -->
    <wire>
      <p1 x="520" y="380"/>
      <p2 x="540" y="380"/>
    </wire>
    <wire>
      <p1 x="540" y="380"/>
      <p2 x="540" y="340"/>
    </wire>
    <wire>
      <p1 x="540" y="340"/>
      <p2 x="580" y="340"/>
    </wire>
    <!-- Gate 5 to Out -->
    <wire>
      <p1 x="640" y="320"/>
      <p2 x="680" y="320"/>
    </wire>
  </wires>
</circuit>
"""

def create_step4_dig():
    return """<?xml version="1.0" encoding="utf-8"?>
<circuit>
  <version>1</version>
  <attributes/>
  <visualElements>
    <visualElement>
      <elementName>In</elementName>
      <elementAttributes>
        <entry>
          <string>Label</string>
          <string>x_0</string>
        </entry>
      </elementAttributes>
      <pos x="160" y="140"/>
    </visualElement>
    <visualElement>
      <elementName>Not</elementName>
      <elementAttributes/>
      <pos x="220" y="180"/>
    </visualElement>
    <visualElement>
      <elementName>And</elementName>
      <elementAttributes/>
      <pos x="340" y="220"/>
    </visualElement>
    <visualElement>
      <elementName>And</elementName>
      <elementAttributes/>
      <pos x="460" y="240"/>
    </visualElement>
    <visualElement>
      <elementName>And</elementName>
      <elementAttributes/>
      <pos x="340" y="340"/>
    </visualElement>
    <visualElement>
      <elementName>Or</elementName>
      <elementAttributes/>
      <pos x="460" y="360"/>
    </visualElement>
    <visualElement>
      <elementName>Or</elementName>
      <elementAttributes/>
      <pos x="580" y="300"/>
    </visualElement>
    <visualElement>
      <elementName>Out</elementName>
      <elementAttributes>
        <entry>
          <string>Label</string>
          <string>y</string>
        </entry>
      </elementAttributes>
      <pos x="680" y="320"/>
    </visualElement>
  </visualElements>
  <wires>
    <!-- x_0 distribution -->
    <wire>
      <p1 x="160" y="140"/>
      <p2 x="200" y="140"/>
    </wire>
    <wire>
      <p1 x="200" y="140"/>
      <p2 x="240" y="140"/>
    </wire>
    <wire>
      <p1 x="200" y="140"/>
      <p2 x="200" y="180"/>
    </wire>
    <wire>
      <p1 x="200" y="180"/>
      <p2 x="220" y="180"/>
    </wire>
    <wire>
      <p1 x="240" y="140"/>
      <p2 x="240" y="280"/>
    </wire>
    <wire>
      <p1 x="240" y="280"/>
      <p2 x="240" y="400"/>
    </wire>
    <wire>
      <p1 x="240" y="280"/>
      <p2 x="460" y="280"/>
    </wire>
    <wire>
      <p1 x="240" y="400"/>
      <p2 x="460" y="400"/>
    </wire>
    <!-- not x_0 distribution -->
    <wire>
      <p1 x="260" y="180"/>
      <p2 x="280" y="180"/>
    </wire>
    <wire>
      <p1 x="280" y="180"/>
      <p2 x="280" y="260"/>
    </wire>
    <wire>
      <p1 x="280" y="260"/>
      <p2 x="280" y="380"/>
    </wire>
    <wire>
      <p1 x="280" y="260"/>
      <p2 x="340" y="260"/>
    </wire>
    <wire>
      <p1 x="280" y="380"/>
      <p2 x="340" y="380"/>
    </wire>
    <!-- Stubs for Gate 1 and Gate 3 other inputs -->
    <wire>
      <p1 x="280" y="220"/>
      <p2 x="340" y="220"/>
    </wire>
    <wire>
      <p1 x="280" y="340"/>
      <p2 x="340" y="340"/>
    </wire>
    <!-- Gate 1 to Gate 2 -->
    <wire>
      <p1 x="400" y="240"/>
      <p2 x="460" y="240"/>
    </wire>
    <!-- Gate 3 to Gate 4 -->
    <wire>
      <p1 x="400" y="360"/>
      <p2 x="460" y="360"/>
    </wire>
    <!-- Gate 2 & 4 to Gate 5 -->
    <wire>
      <p1 x="520" y="260"/>
      <p2 x="540" y="260"/>
    </wire>
    <wire>
      <p1 x="540" y="260"/>
      <p2 x="540" y="300"/>
    </wire>
    <wire>
      <p1 x="540" y="300"/>
      <p2 x="580" y="300"/>
    </wire>
    <wire>
      <p1 x="520" y="380"/>
      <p2 x="540" y="380"/>
    </wire>
    <wire>
      <p1 x="540" y="380"/>
      <p2 x="540" y="340"/>
    </wire>
    <wire>
      <p1 x="540" y="340"/>
      <p2 x="580" y="340"/>
    </wire>
    <!-- Gate 5 to Output -->
    <wire>
      <p1 x="640" y="320"/>
      <p2 x="680" y="320"/>
    </wire>
  </wires>
</circuit>
"""

def generate_all_step_files():
    steps = {
        "AusdruckSchaltnetz_Step1.dig": create_step1_dig(),
        "AusdruckSchaltnetz_Step2.dig": create_step2_dig(),
        "AusdruckSchaltnetz_Step3.dig": create_step3_dig(),
        "AusdruckSchaltnetz_Step4.dig": create_step4_dig(),
    }
    
    # Step 5 is identical to AusdruckSchaltnetz.dig
    src_step5 = (CIRCUITS_DIR / "AusdruckSchaltnetz.dig").read_text(encoding="utf-8")
    steps["AusdruckSchaltnetz_Step5.dig"] = src_step5

    for filename, content in steps.items():
        dig_path = CIRCUITS_DIR / filename
        dig_path.write_text(content, encoding="utf-8")
        print(f"Wrote {dig_path}")
        
        # Export SVG with Digital CLI
        svg_path = dig_path.with_suffix(".svg")
        cmd = [
            "java", "-cp", str(DIGITAL_JAR), "CLI", "svg",
            "-dig", str(dig_path),
            "-svg", str(svg_path),
            "-highContrast"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Exported {svg_path.name}")
        else:
            print(f"Error exporting {filename}: {res.stderr}")

if __name__ == "__main__":
    generate_all_step_files()
