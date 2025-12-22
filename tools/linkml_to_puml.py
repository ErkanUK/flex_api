#!/usr/bin/env python3
"""
Simple LinkML -> PlantUML converter.
Usage:
  pip install pyyaml
  python tools/linkml_to_puml.py docs/flexibility_products.linkml.yaml docs/diagrams/flex_model.puml
"""
import sys
import yaml
from pathlib import Path

def safe_load(path):
    with open(path, 'r', encoding='utf-8') as fh:
        return yaml.safe_load(fh)

def make_plantuml(schema):
    classes = schema.get('classes', {}) or {}
    slots = schema.get('slots', {}) or {}

    lines = ['@startuml', 'title Flex API / LinkML model']
    # Create classes with attributes
    for cname, cdef in classes.items():
        lines.append(f'class {cname} {{')
        # try slots on class: cdef.get('slots') is list of slot names
        for s in cdef.get('slots', []) or []:
            # slot may be a dict or a name; normalize
            sname = s if isinstance(s, str) else s.get('name', '<slot>')
            sdef = slots.get(sname, {})
            r = sdef.get('range', sdef.get('range_name', 'string'))
            # annotate identifier/multivalued
            suffix = ''
            if sdef.get('multivalued', False):
                suffix = '[]'
            if sdef.get('identifier', False):
                prefix = '+'
            else:
                prefix = '-'
            lines.append(f'  {prefix} {sname}: {r}{suffix}')
        lines.append('}')
    # Try to infer simple relationships where a slot.range is a class name
    for sname, sdef in slots.items():
        r = sdef.get('range')
        if isinstance(r, str) and r in classes:
            # find which classes use this slot
            for cname, cdef in classes.items():
                if sname in (cdef.get('slots') or []):
                    mult = sdef.get('multivalued', False)
                    arrow = '"1" --> "0..*"' if mult else '"1" --> "1"'
                    lines.append(f'{cname} --> {r} : {sname}')
    lines.append('@enduml')
    return '\n'.join(lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: linkml_to_puml.py <input_linkml.yaml> <output.puml>")
        sys.exit(2)
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    schema = safe_load(input_path)
    puml = make_plantuml(schema)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(puml, encoding='utf-8')
    print(f"Wrote {output_path}")

if __name__ == '__main__':
    main()