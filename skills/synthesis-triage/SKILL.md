---
name: synthesis-triage
description: Specialized skill for interpreting logic synthesis and static timing analysis (STA) reports from Yosys, OpenSTA, Vivado, and Design Compiler. Guides agents through cell count breakdown, inferred latch triage, timing slack analysis (WNS/TNS), and area-delay optimization.
---

# Synthesis Triage Skill

This skill guides coding agents through analyzing and optimizing logic synthesis reports and static timing analysis (STA) metrics produced by tools like Yosys, OpenSTA, Synopsys Design Compiler, or Vivado.

---

## 1. Synthesis Diagnostic Rubric

### 1. Inferred Latch Detection (High Priority)
- **Warning Sign**: Yosys reports `Latch inferred for signal '\output_reg'`.
- **Root Cause**: An `always @*` block leaves a variable unassigned in at least one branch of an `if` or `case` construct.
- **Action**: Fix the RTL by adding default assignments (`output_reg = 0;`) at the entry of the combinational block, or add a missing `default:` branch in `case`.

### 2. Cell Count & Area Analysis (Know Your Target)
- **FPGA targets** (`ice40`, `xilinx`, `intel`): cells are LUTs/FFs; `areaUm2` does not apply. `sky130` without a baked PDK errors honestly — use `nangate45` for ASIC-area answers.
- **Nangate45**: `areaUm2` (stat-JSON `area`, text fallback) is the tapeout-relevant footprint; track it across RTL changes like cell count.
- **Equivalence verdicts** (`yosys_equiv`): EQUIVALENT (own netlist proven) / NOT_EQUIVALENT (mutant caught — treat as P0) / INCONCLUSIVE (latch/FF SAT limits — never a pass, escalate to bounded proof).

### 2b. Netlist Compatibility for OpenROAD (P&R Readiness)
- **P&R readiness**: OpenROAD 2.0 rejects operator expressions and `output/reg` port redeclarations. Only liberty-mapped netlists (`nangate45`, never bare `generic`) flow into place-and-route; Yosys-side stripping handles the latter automatically.
When evaluating cell reports:
- **Look-Up Tables (LUTs)**: Combinational complexity. A sudden explosion in LUT count indicates deep nested muxes, unrolled large loops, or wide arithmetic operations.
- **Flip-Flops (FDRE / DFF)**: Sequential state registers. Count should exactly match the number of registered state bits in the RTL.
- **DSP Slices / Hard Multipliers**: Dedicated hardware multipliers. If multipliers are implemented in LUT logic instead of DSPs, check bitwidth thresholds and tool synthesis attributes (`(* use_dsp = "yes" *)`).
- **Block RAMs (BRAMs)**: Embedded memory arrays. If small memories synthesize into hundreds of distributed flip-flops instead of BRAMs, verify synchronous read timing.

### 3. Timing Slack & Critical Path Triage
STA reports revolve around two primary figures of merit:
- **Worst Negative Slack (WNS)**:
  - If $\text{WNS} \ge 0$: Design meets timing at target clock frequency.
  - If $\text{WNS} < 0$: Timing violation. The most critical path exceeds clock period by $|WNS|$.
- **Total Negative Slack (TNS)**:
  - Sum of negative slack across all violating paths. TNS indicates whether the failure is isolated to one path or represents a systemic architectural timing breakdown.
- **Setup Violation Remediation**:
  1. Insert pipeline register stages (break long combinational logic into multi-cycle stages).
  2. Restructure deep priority encoders (`if-else if-else`) into balanced tree structures (`case`).
  3. Pre-compute partial products or terms before wide additions.
- **Hold Violation Remediation**:
  - Hold violations are clock-period independent and usually fixed during physical design via buffer insertion on the data path.

---

## 2. Example: Triaging a Yosys Synthesis Log

### Sample Yosys Report
```text
=== Printing statistics ===
   Number of wires:                 124
   Number of wire bits:             482
   Number of public wires:           18
   Number of memories:                0
   Number of memory bits:             0
   Number of processes:               0
   Number of cells:                  85
     $_DFF_P_                        16
     $_NOT_                           8
     $_AND_                          24
     $_OR_                           18
     $_XOR_                          19

   Chip area for top module '\top': 85.000000
   Warning: Latch inferred for signal '\status' from process '\top.$proc$top.v:34$1'.
```

### Agent Triage Actions
1. **Latch Warning Found**: Inspect line 34 of `top.v`. Locate `status` register in combinational process. Add missing assignment to eliminate inferred latch.
2. **Registers**: 16 DFFs synthesized. Confirms two 8-bit registers or one 16-bit counter.
3. **Logic Depth**: 61 combinational gates (`AND`, `OR`, `XOR`). Good balance for low-latency paths.

---

## 3. Checklist for Synthesis Triage
- [ ] Are there any inferred latch warnings in the log?
- [ ] Does the flip-flop count match expected registered state variables?
- [ ] Is WNS non-negative ($\ge 0$ ns)?
- [ ] Are wide operators (multipliers, dividers) mapped to hard macros where appropriate?
- [ ] If timing failed, has pipelining or logic balancing been proposed?
