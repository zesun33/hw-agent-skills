#!/usr/bin/env python3
"""Exports skills from skills/<name>/SKILL.md into .cursor/rules/<name>.mdc."""

import re
import sys
from pathlib import Path

GLOBS_MAP = {
    "rtl-reviewer": '["*.v", "*.sv", "*.vh"]',
    "verilog-testbench-writer": '["*_tb.v", "*_tb.sv", "tb_*.v", "test_*.v"]',
    "synthesis-triage": '["*.v", "*.sv", "*.ys", "*.sdc"]',
    "kernel-roofline-explainer": '["*.cu", "*.cuh", "*.py", "*.cpp"]',
    "asic-flow-operator": '["*.tcl", "*.sdc", "*.def", "*.lef", "*.v"]',
}

def parse_frontmatter(content: str):
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        return None, content
    raw_yaml, body = match.groups()
    metadata = {}
    for line in raw_yaml.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()
    return metadata, body

def export_skill(skill_dir: Path, out_dir: Path) -> Path:
    skill_file = skill_dir / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)

    name = skill_dir.name
    globs = GLOBS_MAP.get(name, '["*.v", "*.sv"]')
    desc = meta.get("description", f"Rule for {name}").replace('"', '\\"')

    mdc_content = f"""---
description: "{desc}"
globs: {globs}
alwaysApply: false
---

{body.strip()}
"""

    out_file = out_dir / f"{name}.mdc"
    out_file.write_text(mdc_content, encoding="utf-8")
    return out_file

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    out_dir = root / ".cursor" / "rules"
    out_dir.mkdir(parents=True, exist_ok=True)

    check_mode = "--check" in sys.argv

    exported = []
    for item in sorted(skills_dir.iterdir()):
        if item.is_dir() and (item / "SKILL.md").exists():
            out_file = export_skill(item, out_dir)
            exported.append(out_file)
            print(f"✔ Exported {item.name} -> .cursor/rules/{out_file.name}")

    print(f"\n✔ Successfully generated {len(exported)} Cursor .mdc rules!")

if __name__ == "__main__":
    main()
