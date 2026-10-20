#!/usr/bin/env python3
"""
SLX to Digital Transpiler & Batch Converter:
Converts MATLAB/Simulink .slx block diagrams into HNeemann Digital .dig circuits.
"""
import re
import sys
import json
import zipfile
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

DIGITAL_JAR_PATH = Path("/Applications/Digital/Digital.jar")
BASE_DIR = Path(__file__).resolve().parent.parent # digital-circuits
SLX_BASE_DIR = BASE_DIR.parent / "matlab-simulink-examples"

def parse_position(pos_str: str):
    nums = [int(n.strip()) for n in pos_str.strip("[]").split(",") if n.strip()]
    if len(nums) == 4:
        return nums[0], nums[1], nums[2], nums[3] # left, top, right, bottom
    return 100, 100, 140, 140

def snap(val: float, step: int = 20) -> int:
    return int(round(val / step)) * step

def collect_destinations(element):
    dests = []
    dst_p = element.find("P[@Name='Dst']")
    if dst_p is not None and dst_p.text:
        dests.append(dst_p.text)
    for branch in element.findall("Branch"):
        dests.extend(collect_destinations(branch))
    return dests

def convert_slx_to_digital(slx_path: Path, output_dig_path: Path):
    with zipfile.ZipFile(slx_path) as z:
        if "simulink/systems/system_root.xml" in z.namelist():
            xml_data = z.read("simulink/systems/system_root.xml")
        elif "simulink/blockdiagram.xml" in z.namelist():
            xml_data = z.read("simulink/blockdiagram.xml")
        else:
            raise ValueError(f"No block diagram XML found in {slx_path}")

    root = ET.fromstring(xml_data)

    # 1. Collect all non-template blocks with SIDs
    blocks = {}
    for b in root.iter("Block"):
        sid = b.attrib.get("SID")
        if not sid:
            continue
        btype = b.attrib.get("BlockType")
        bname = b.attrib.get("Name", f"Block_{sid}").replace("\n", " ").strip()

        pos_p = b.find("P[@Name='Position']")
        pos = parse_position(pos_p.text) if pos_p is not None else (100, 100, 140, 140)

        op_p = b.find("P[@Name='Operator']")
        op = op_p.text if op_p is not None else ("AND" if btype == "Logic" else None)

        inputs_p = b.find("P[@Name='Inputs']")
        num_inputs = 2
        if inputs_p is not None and inputs_p.text:
            raw_inp = inputs_p.text.strip()
            if raw_inp.isdigit():
                num_inputs = int(raw_inp)
            elif "+" in raw_inp or "|" in raw_inp:
                num_inputs = len(raw_inp)

        blocks[sid] = {
            "sid": sid,
            "type": btype,
            "name": bname,
            "pos": pos,
            "operator": op,
            "inputs": num_inputs,
            "xml_el": b
        }

    if not blocks:
        raise ValueError(f"No valid blocks with SID in {slx_path}")

    # Determine bounding box
    min_x = min(b["pos"][0] for b in blocks.values())
    min_y = min(b["pos"][1] for b in blocks.values())

    digital_elements = []
    block_ports = {} # sid -> {"in": {1: (x, y), ...}, "out": {1: (x, y), ...}}

    for sid, b in blocks.items():
        btype = b["type"]
        bname = b["name"]
        left, top, right, bottom = b["pos"]

        # Grid-snap coordinates
        gx = snap((left - min_x) * 1.5) + 200
        gy = snap((top - min_y) * 1.5) + 160

        ports = {"in": {}, "out": {}}

        if btype == "Logic":
            op = (b["operator"] or "AND").upper()
            num_inp = b["inputs"]
            attrs = {}

            if op == "AND":
                elem_name = "And"
            elif op == "OR":
                elem_name = "Or"
            elif op == "XOR":
                elem_name = "XOr"
            elif op == "NAND":
                elem_name = "NAnd"
            elif op == "NOR":
                elem_name = "NOr"
            elif op == "NOT":
                elem_name = "Not"
                num_inp = 1
            else:
                elem_name = "And"

            if num_inp != 2 and elem_name != "Not":
                attrs["Inputs"] = str(num_inp)

            digital_elements.append({
                "name": elem_name,
                "x": gx,
                "y": gy,
                "attrs": attrs
            })

            if elem_name == "Not":
                ports["in"][1] = (gx, gy)
                ports["out"][1] = (gx + 40, gy)
            elif num_inp == 2:
                ports["in"][1] = (gx, gy)
                ports["in"][2] = (gx, gy + 40)
                ports["out"][1] = (gx + 60, gy + 20)
            else:
                for inp_idx in range(1, num_inp + 1):
                    ports["in"][inp_idx] = (gx, gy + (inp_idx - 1) * 20)
                ports["out"][1] = (gx + 60, gy + 20)

        elif btype in ["Inport", "ManualSwitch"]:
            digital_elements.append({
                "name": "In",
                "x": gx,
                "y": gy,
                "attrs": {"Label": bname}
            })
            ports["out"][1] = (gx, gy)

        elif btype == "Constant":
            # If variable name like s1, e1, x0 treat as In
            if re.match(r"^[a-zA-Z]", bname) and bname not in ["0", "1"]:
                digital_elements.append({
                    "name": "In",
                    "x": gx,
                    "y": gy,
                    "attrs": {"Label": bname}
                })
                ports["out"][1] = (gx, gy)
            else:
                val_p = b["xml_el"].find("P[@Name='Value']")
                val = "1" if val_p is not None and val_p.text == "1" else "0"
                digital_elements.append({
                    "name": "Const",
                    "x": gx,
                    "y": gy,
                    "attrs": {"Value": val}
                })
                ports["out"][1] = (gx, gy)

        elif btype in ["Outport", "Display"]:
            digital_elements.append({
                "name": "Out",
                "x": gx,
                "y": gy,
                "attrs": {"Label": bname}
            })
            ports["in"][1] = (gx, gy)

        elif btype in ["TransportDelay", "VariableTransportDelay", "Buffer"]:
            digital_elements.append({
                "name": "Delay",
                "x": gx,
                "y": gy,
                "attrs": {}
            })
            ports["in"][1] = (gx, gy)
            ports["out"][1] = (gx + 40, gy)

        elif btype in ["Clock", "PulseGenerator"]:
            digital_elements.append({
                "name": "Clock",
                "x": gx,
                "y": gy,
                "attrs": {"Label": bname}
            })
            ports["out"][1] = (gx, gy)

        block_ports[sid] = ports

    # 2. Parse Lines & Generate Orthogonal Manhattan Wires
    wires = []

    def add_ortho_wire(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if (x1, y1) == (x2, y2):
            return
        if x1 == x2 or y1 == y2:
            wires.append(((x1, y1), (x2, y2)))
        else:
            mid_x = snap((x1 + x2) / 2)
            if mid_x == x1 or mid_x == x2:
                wires.append(((x1, y1), (x1, y2)))
                wires.append(((x1, y2), (x2, y2)))
            else:
                wires.append(((x1, y1), (mid_x, y1)))
                wires.append(((mid_x, y1), (mid_x, y2)))
                wires.append(((mid_x, y2), (x2, y2)))

    for l in root.iter("Line"):
        src_p = l.find("P[@Name='Src']")
        if src_p is None or not src_p.text:
            continue

        src_parts = src_p.text.split("#out:")
        src_sid = src_parts[0]
        src_port_num = int(src_parts[1]) if len(src_parts) > 1 else 1

        if src_sid not in block_ports or src_port_num not in block_ports[src_sid]["out"]:
            continue
        src_pos = block_ports[src_sid]["out"][src_port_num]

        # Collect all destinations recursively through branches
        dests = collect_destinations(l)

        for dst_str in dests:
            dst_parts = dst_str.split("#in:")
            dst_sid = dst_parts[0]
            dst_port_num = int(dst_parts[1]) if len(dst_parts) > 1 else 1

            if dst_sid in block_ports and dst_port_num in block_ports[dst_sid]["in"]:
                dst_pos = block_ports[dst_sid]["in"][dst_port_num]
                add_ortho_wire(src_pos, dst_pos)

    # 3. Assemble Digital XML Document
    circuit = ET.Element("circuit")
    v = ET.SubElement(circuit, "version")
    v.text = "1"
    ET.SubElement(circuit, "attributes")

    visual_elems = ET.SubElement(circuit, "visualElements")
    for el in digital_elements:
        ve = ET.SubElement(visual_elems, "visualElement")
        en = ET.SubElement(ve, "elementName")
        en.text = el["name"]

        ea = ET.SubElement(ve, "elementAttributes")
        for ak, av in el["attrs"].items():
            entry = ET.SubElement(ea, "entry")
            s_k = ET.SubElement(entry, "string")
            s_k.text = ak
            if ak == "Inputs":
                s_v = ET.SubElement(entry, "int")
            else:
                s_v = ET.SubElement(entry, "string")
            s_v.text = av

        pos_el = ET.SubElement(ve, "pos")
        pos_el.attrib["x"] = str(el["x"])
        pos_el.attrib["y"] = str(el["y"])

    wires_el = ET.SubElement(circuit, "wires")
    seen_wires = set()
    for (x1, y1), (x2, y2) in wires:
        norm = ((min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2)))
        if norm in seen_wires:
            continue
        seen_wires.add(norm)

        w = ET.SubElement(wires_el, "wire")
        p1 = ET.SubElement(w, "p1")
        p1.attrib["x"] = str(x1)
        p1.attrib["y"] = str(y1)
        p2 = ET.SubElement(w, "p2")
        p2.attrib["x"] = str(x2)
        p2.attrib["y"] = str(y2)

    tree = ET.ElementTree(circuit)
    ET.indent(tree, space="  ")
    output_dig_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output_dig_path, encoding="utf-8", xml_declaration=True)
    return True

def batch_convert():
    inv_path = SLX_BASE_DIR / "simulink_inventory.json"
    if not inv_path.is_file():
        print("Inventory not found. Run extract_simulink_inventory.py first.")
        return

    with open(inv_path, encoding="utf-8") as f:
        inv = json.load(f)

    # Categories to batch convert
    category_dest = {
        "Boolean Algebra & Basic Gates": BASE_DIR / "boolean_algebra",
        "Arithmetic (Adders)": BASE_DIR / "combinational",
        "Hazards & Glitches": BASE_DIR / "hazards",
        "Multiplexers & Demultiplexers": BASE_DIR / "combinational"
    }

    success = 0
    failed = 0
    skipped = 0

    print("Starting batch conversion from SLX to Digital...")

    for item in inv:
        cat = item["category"]
        if cat not in category_dest:
            skipped += 1
            continue

        bcount = len(item["blocks"])
        if bcount == 0 or bcount > 40: # skip empty or huge complex subsystems
            skipped += 1
            continue

        slx_file = SLX_BASE_DIR / item["file"]
        dest_dir = category_dest[cat]
        model_name = item["name"]
        out_dig = dest_dir / f"{model_name}.dig"
        out_svg = dest_dir / f"{model_name}.svg"

        try:
            convert_slx_to_digital(slx_file, out_dig)
            # Validate and export SVG using Digital.jar
            if DIGITAL_JAR_PATH.is_file():
                cmd = [
                    "java", "-cp", str(DIGITAL_JAR_PATH), "CLI", "svg",
                    "-dig", str(out_dig),
                    "-svg", str(out_svg),
                    "-highContrast", "-hideTest", "-noPinMarker"
                ]
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if res.returncode == 0:
                    print(f"  [OK] {slx_file.name} -> {out_dig.relative_to(BASE_DIR)} + SVG")
                    success += 1
                else:
                    print(f"  [WARN] {slx_file.name} converted to .dig but SVG export warned: {res.stderr.decode()[:60]}")
                    success += 1
            else:
                success += 1
        except Exception as e:
            print(f"  [FAIL] {slx_file.name}: {e}")
            failed += 1

    print(f"\nBatch conversion complete: {success} successful, {failed} failed, {skipped} skipped.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        batch_convert()
    elif len(sys.argv) == 3:
        convert_slx_to_digital(Path(sys.argv[1]), Path(sys.argv[2]))
    else:
        print("Usage:")
        print("  python3 slx_to_digital.py <input.slx> <output.dig>")
        print("  python3 slx_to_digital.py --batch")
