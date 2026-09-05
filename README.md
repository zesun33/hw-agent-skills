# @zesun33/hw-agent-skills

> Portable AI agent skills, rubrics, and system prompts for digital hardware design and ML systems engineering.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Platform: Antigravity | Cursor | Claude](https://img.shields.io/badge/platforms-Antigravity%20%7C%20Cursor%20%7C%20Claude-blueviolet)](#quickstart)
[![Skills: 5 Core](https://img.shields.io/badge/skills-5%20verified-brightgreen)](#the-skills-pack)

`hw-agent-skills` gives coding agents (Claude Code, Cursor, Antigravity, OpenCode, Codex) the **cognitive engineering rubrics** needed to reason about register-transfer level (RTL) semantics, race conditions, self-checking verification testbenches, logic synthesis metrics, and GPU kernel roofline limits.

---

## ⚡ Quick Tour: Why Coding Agents Need `hw-agent-skills`

### The Cognitive Gap in General LLMs
| General Coding Agent (No Skills) | Hardware-Specialized Agent (With `hw-agent-skills`) |
| :--- | :--- |
| Uses blocking `=` in sequential blocks, creating simulation race conditions | Enforces strict assignment discipline: `<=` for sequential, `=` for combinational |
| Leaves `if`/`case` branches unassigned, silently inferring transparent latches | Flags incomplete branch coverage before synthesis |
| Generates visual-inspection testbenches that require human waveform viewing | Generates self-checking assertion suites with `$fatal` and timeout guards |
| Guesses performance bottlenecks in CUDA/Triton kernels | Mathematically calculates Operational Arithmetic Intensity ($I = \text{FLOPs}/\text{Byte}$) |

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

## Quickstart

### 1. Cursor IDE
This repo automatically exports its skills into Cursor's native `.cursor/rules/*.mdc` format:
```bash
python3 scripts/export_cursor_rules.py
```
Rules are placed in `.cursor/rules/` and automatically apply to relevant files (e.g. `*.v`, `*.sv`, `*.cu`, `*.tcl`).

### 2. Antigravity IDE & 2.0
Symlink or copy the `skills/` directory into your project's `.agents/skills/`:
```bash
mkdir -p .agents/skills
cp -r skills/* .agents/skills/
```

### 3. Claude Code / CLI
Pass the relevant `SKILL.md` directly into your system prompt or reference it via `@skills/<name>/SKILL.md`.

---

## Verification

Run the full verification suite (schema validation, unit tests, rule sync, and doc check):
```bash
./scripts/verify.sh
```
