#!/usr/bin/env python3
"""Validates YAML frontmatter and structural integrity of hw-agent-skills."""

import os
import re
import sys
from pathlib import Path

REQUIRED_SKILLS = [
    "rtl-reviewer",
    "verilog-testbench-writer",
    "synthesis-triage",
    "kernel-roofline-explainer",
    "asic-flow-operator",
]

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

def validate_skill(skill_dir: Path) -> bool:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        print(f"❌ [FAIL] Missing SKILL.md in {skill_dir.name}")
        return False

    content = skill_file.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)

    if not meta:
        print(f"❌ [FAIL] {skill_dir.name}/SKILL.md: Missing or malformed YAML frontmatter")
        return False

    if "name" not in meta:
        print(f"❌ [FAIL] {skill_dir.name}/SKILL.md: Missing 'name' in frontmatter")
        return False

    if meta["name"] != skill_dir.name:
        print(f"❌ [FAIL] {skill_dir.name}/SKILL.md: Frontmatter name '{meta['name']}' does not match directory '{skill_dir.name}'")
        return False

    if "description" not in meta or len(meta["description"]) < 20:
        print(f"❌ [FAIL] {skill_dir.name}/SKILL.md: Description must be at least 20 characters")
        return False

    if len(body.strip()) < 200:
        print(f"❌ [FAIL] {skill_dir.name}/SKILL.md: Body content too short (< 200 characters)")
        return False

    # Check for core sections
    if "# " not in body:
        print(f"❌ [FAIL] {skill_dir.name}/SKILL.md: Missing top-level title")
        return False

    print(f"✔ [PASS] {skill_dir.name}: Valid frontmatter and rubric body ({len(body)} chars)")
    return True

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"

    if not skills_dir.exists():
        print("❌ [FAIL] skills/ directory not found")
        sys.exit(1)

    all_passed = True
    found_skills = []

    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            found_skills.append(item.name)
            if not validate_skill(item):
                all_passed = False

    for req in REQUIRED_SKILLS:
        if req not in found_skills:
            print(f"❌ [FAIL] Missing required skill: {req}")
            all_passed = False

    if not all_passed:
        print("\n❌ Skill validation failed.")
        sys.exit(1)

    print(f"\n✔ All {len(found_skills)} skills validated successfully!")

if __name__ == "__main__":
    main()
