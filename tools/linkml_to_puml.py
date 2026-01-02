#!/usr/bin/env python3
"""
Robust linkml_to_puml.py

- Always emits a PUML class for every LinkML `classes` entry.
- Emits attributes for each slot, shows identifier/multivalued markers.
- Emits relationships when a slot.range is another class.
- Writes one combined PUML file.

Usage:
  python tools/linkml_to_puml.py <input.linkml.yaml> <output_puml>
"""
import sys
from pathlib import Path
import yaml

def safe_load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)

def normalize_name(n: str) -> str:
    return str(n).replace(" ", "_").replace("-", "_")

def attribute_line(sname: str, sdef: dict) -> str:
    """Return a single attribute line for a class box."""
    r = sdef.get("range", "string")
    mult = sdef.get("multivalued", False)
    ident = sdef.get("identifier", False)
    prefix = "+" if ident else "-"
    suffix = "[]" if mult else ""
    desc = sdef.get("description", "")
    # Keep description short and safe (escape newlines)
    desc_short = str(desc).replace("\n", " ").strip()
    if desc_short:
        return f"  {prefix} {sname} : {r}{suffix}  // {desc_short[:120]}"
    else:
        return f"  {prefix} {sname} : {r}{suffix}"

def class_to_puml(name: str, cdef: dict, slots: dict) -> str:
    lines = []
    lines.append(f"class {name} {{")
    for sname in (cdef.get("slots") or []):
        sdef = slots.get(sname, {}) or {}
        lines.append(attribute_line(sname, sdef))
    lines.append("}")
    return "\n".join(lines)

def generate_puml_from_linkml(linkml: dict, out_puml: Path):
    classes = linkml.get("classes", {}) or {}
    slots = linkml.get("slots", {}) or {}
    enums = linkml.get("enums", {}) or {}

    lines = ["@startuml", f"title Auto-generated diagram from {out_puml.name}", "skinparam classAttributeIconSize 0", ""]

    # Emit enums as a small package (optional)
    if enums:
        lines.append('package "Enums" {')
        for ename, edef in enums.items():
            vals = edef.get("permissible_values", []) or []
            lines.append(f'class {ename} <<enumeration>> {{')
            for v in vals[:40]:
                # safe representation of enum values
                lines.append(f'  {v}')
            lines.append("}")
        lines.append("}")
        lines.append("")

    # Emit every class, even empty
    for cname, cdef in classes.items():
        lines.append(class_to_puml(cname, cdef or {}, slots))
        lines.append("")

    # Emit relationships for slots whose range is another class
    rels = []
    for sname, sdef in slots.items():
        rng = sdef.get("range")
        if isinstance(rng, str) and rng in classes:
            # find classes that own this slot
            for cname, cdef in classes.items():
                if sname in (cdef.get("slots") or []):
                    mult = sdef.get("multivalued", False)
                    multiplicity = '"0..*"' if mult else '"1"'
                    rels.append(f'{cname} --> {rng} : {sname}')
    if rels:
        lines.append("\n".join(rels))
        lines.append("")

    lines.append("@enduml")

    out_puml.parent.mkdir(parents=True, exist_ok=True)
    out_puml.write_text("\n".join(lines), encoding="utf-8")

    return {
        "classes_emitted": list(classes.keys()),
        "relations_emitted": rels,
        "out": str(out_puml),
    }

def main(argv):
    if len(argv) < 3:
        print("Usage: tools/linkml_to_puml.py <input.linkml.yaml> <output_puml>")
        sys.exit(2)

    input_path = Path(argv[1])
    out_arg = Path(argv[2])

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}")
        sys.exit(1)

    doc = safe_load(input_path)
    if doc is None:
        print("ERROR: empty or invalid LinkML file")
        sys.exit(1)

    if out_arg.suffix.lower() == ".puml" or out_arg.name.endswith(".puml"):
        out_puml = out_arg
    else:
        out_puml = out_arg / (input_path.stem + ".puml")

    result = generate_puml_from_linkml(doc, out_puml)

    print("--- linkml_to_puml.py summary ---")
    print("Classes emitted:", len(result["classes_emitted"]))
    for c in result["classes_emitted"][:200]:
        print(" -", c)
    print("Relations emitted:", len(result["relations_emitted"]))
    for r in result["relations_emitted"][:200]:
        print(" -", r)
    print("Wrote:", result["out"])

if __name__ == "__main__":
    main(sys.argv)