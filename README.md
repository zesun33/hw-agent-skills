# @zesun33/hw-agent-skills

> Portable AI agent skills, rubrics, and system prompts for digital hardware design and ML systems engineering.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![CI](https://github.com/zesun33/hw-agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/zesun33/hw-agent-skills/actions/workflows/ci.yml)
[![Platform: Universal AI IDEs](https://img.shields.io/badge/platforms-Cursor%20%7C%20Windsurf%20%7C%20Copilot%20%7C%20Claude-blueviolet)](#quickstart)
[![Skills: 5 Core](https://img.shields.io/badge/skills-5%20verified-brightgreen)](#the-skills-pack)

`hw-agent-skills` gives coding agents and AI IDEs (**Cursor**, **Windsurf**, **GitHub Copilot / OpenAI Codex**, **Claude Code**, **Google Antigravity**, **OpenCode**, **Cline**) the **cognitive engineering rubrics** needed to reason about register-transfer level (RTL) semantics, race conditions, self-checking verification testbenches, logic synthesis metrics, and GPU kernel roofline limits.

---

## ⚡ Quick Tour: Why Coding Agents Need `hw-agent-skills`

### The Cognitive Gap in General LLMs
| General Coding Agent (No Skills) | Hardware-Specialized Agent (With `hw-agent-skills`) |
| :--- | :--- |
| Uses blocking `=` in sequential blocks, creating simulation race conditions | Enforces strict assignment discipline: `<=` for sequential, `=` for combinational |
| Leaves `if`/`case` branches unassigned, silently inferring transparent latches | Flags incomplete branch coverage before synthesis |
| Generates visual-inspection testbenches that require human waveform viewing | Generates self-checking assertion suites with `$fatal` and timeout guards |
| Guesses performance bottlenecks in CUDA/Triton kernels | Mathematically calculates Operational Arithmetic Intensity (I = FLOPs / Byte) |

---

## The Skills Pack

| Skill | Focus Area | What the Agent Does | File |
| :--- | :--- | :--- | :--- |
| **`rtl-reviewer`** | Verilog / SystemVerilog Audit | Audits RTL for blocking/non-blocking races, transparent latches, reset protocols, and clock domain crossings (CDC). | [`skills/rtl-reviewer/SKILL.md`](skills/rtl-reviewer/SKILL.md) |
| **`verilog-testbench-writer`** | Verification & Testbenches | Generates self-checking testbenches with parametric clocks, reset pulses, `$fatal` assertions, and watchdog timeout guards. | [`skills/verilog-testbench-writer/SKILL.md`](skills/verilog-testbench-writer/SKILL.md) |
| **`synthesis-triage`** | Logic Synthesis & STA | Interprets Yosys/OpenSTA reports, identifies inferred latches, maps cell counts (LUTs, FFs, DSPs), and triages timing slack (WNS/TNS). | [`skills/synthesis-triage/SKILL.md`](skills/synthesis-triage/SKILL.md) |
| **`kernel-roofline-explainer`** | GPU & ML Acceleration | Computes Arithmetic Intensity, knee points, and memory-bound vs. compute-bound classification on A100/H100 GPUs. | [`skills/kernel-roofline-explainer/SKILL.md`](skills/kernel-roofline-explainer/SKILL.md) |
| **`asic-flow-operator`** | Digital ASIC Physical Design | Navigates the OpenROAD/Sky130 flow: Floorplanning, Placement, CTS, Routing, and timing closure remediation. | [`skills/asic-flow-operator/SKILL.md`](skills/asic-flow-operator/SKILL.md) |

---

## Quickstart & IDE Setup

### 1. Cursor IDE
This repo automatically exports its skills into Cursor's native `.cursor/rules/*.mdc` format:
```bash
python3 scripts/export_cursor_rules.py
```
Rules are placed in `.cursor/rules/` and automatically apply to relevant files (e.g. `*.v`, `*.sv`, `*.cu`, `*.tcl`).

### 2. GitHub Copilot & OpenAI Codex (VS Code)
Include the rubrics in `.github/copilot-instructions.md` or reference the skill files in your prompt:
```bash
cat skills/rtl-reviewer/SKILL.md >> .github/copilot-instructions.md
```

### 3. Windsurf (Codeium)
Add relevant skill rubrics directly into `.windsurfrules` in your workspace root.

### 4. Google Antigravity IDE & 2.0
Symlink or copy the `skills/` directory into your project's `.agents/skills/`:
```bash
mkdir -p .agents/skills
cp -r skills/* .agents/skills/
```

### 5. Claude Code / OpenCode / CLI
Pass the relevant `SKILL.md` directly into your system prompt or reference it via `@skills/<name>/SKILL.md`.

---

## Verification

Run the full 5-gate verification suite (spec lock, schema validation, unit tests, Cursor rule sync, and doc check):
```bash
./scripts/verify.sh
```

To run a specific gate:
```bash
./scripts/verify.sh --gate 2   # Schema & frontmatter validation
./scripts/verify.sh --gate 3   # Unit tests
```
