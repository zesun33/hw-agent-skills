"""Unit tests for hw-agent-skills schema and export integrity."""

import unittest
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
RULES_DIR = ROOT / ".cursor" / "rules"

EXPECTED_SKILLS = [
    "rtl-reviewer",
    "verilog-testbench-writer",
    "synthesis-triage",
    "kernel-roofline-explainer",
    "asic-flow-operator",
]

class TestSkillsSchema(unittest.TestCase):
    def test_all_expected_skills_exist(self):
        for name in EXPECTED_SKILLS:
            skill_file = SKILLS_DIR / name / "SKILL.md"
            self.assertTrue(skill_file.exists(), f"Missing skill file: {skill_file}")

    def test_frontmatter_structure(self):
        for name in EXPECTED_SKILLS:
            content = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
            self.assertIsNotNone(match, f"{name}/SKILL.md missing valid YAML frontmatter")

            raw_yaml, body = match.groups()
            self.assertIn(f"name: {name}", raw_yaml)
            self.assertIn("description:", raw_yaml)
            self.assertGreater(len(body.strip()), 500, f"{name} body content is too short")

    def test_cursor_rules_generated(self):
        for name in EXPECTED_SKILLS:
            rule_file = RULES_DIR / f"{name}.mdc"
            self.assertTrue(rule_file.exists(), f"Missing exported Cursor rule: {rule_file}")
            rule_content = rule_file.read_text(encoding="utf-8")
            self.assertIn("globs:", rule_content)
            self.assertIn("description:", rule_content)

    def test_rtl_reviewer_contains_rules(self):
        content = (SKILLS_DIR / "rtl-reviewer" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Assignment Discipline", content)
        self.assertIn("Branch Coverage", content)
        self.assertIn("Reset Protocol", content)
        self.assertIn("Clock Domain Crossing", content)

    def test_roofline_contains_formulas(self):
        content = (SKILLS_DIR / "kernel-roofline-explainer" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Arithmetic Intensity", content)
        self.assertIn("Memory Bound", content)
        self.assertIn("Compute Bound", content)
        self.assertIn("A100", content)

if __name__ == "__main__":
    unittest.main()
