---
name: asic-flow-operator
description: Specialized skill for executing and debugging digital ASIC physical design flows (OpenROAD, OpenLane, Sky130). Guides agents through stage transitions from synthesis to floorplanning, placement, clock tree synthesis (CTS), routing, timing closure, and DRC/LVS physical verification.
---

# ASIC Flow Operator Skill

This skill guides coding agents through navigating and automating open-source digital Application-Specific Integrated Circuit (ASIC) physical design flows using tools like **OpenROAD**, **OpenLane**, and the **SkyWater 130nm (sky130)** process design kit (PDK).

---

## 1. The Physical Design Flow Pipeline

```text
[RTL Code (.v) + asserts guarded by `ifdef FORMAL`] 
       │
       ▼  Step 0: Formal lint + prove (SymbiYosys smtbmc+z3, -DFORMAL)
[PROVEN properties]
       │
       ▼  Step 1: Synthesis (Yosys, liberty-mapped nangate45 for P&R)
[Gate-level Netlist without operator expressions or port redeclarations]
       │
       ▼  Step 2: Floorplanning & IO Placement (OpenROAD / init_floorplan)
[Die / Core Boundary + Power Grid (PDN)]
       │
       ▼  Step 3: Global & Detailed Placement (OpenROAD / global_placement)
[Placed Standard Cells]
       │
       ▼  Step 4: Clock Tree Synthesis (OpenROAD / repair_clock_inverters)
[Balanced Low-Skew Clock Tree]
       │
       ▼  Step 5: Global & Detailed Routing (OpenROAD / global_route, triton_route)
[Fully Connected Wires + Vias]
       │
       ▼  Step 6: Signoff Verification (OpenSTA, Magic DRC, Netgen LVS)
[Clean GDSII Layout Ready for Tapeout]
```

---

## 2. Stage-by-Stage Operational Rules

### Stage 1: Floorplanning (`init_floorplan`)
- **Core Utilization**: Set initial target utilization to `35% - 55%`. Setting utilization $> 65\%$ on standard cells frequently causes unroutable congestion during detailed routing.
- **Aspect Ratio**: Keep core aspect ratio near 1.0 (square) unless pin density constraints dictate a rectangular floorplan.
- **Power Distribution Network (PDN)**: Ensure standard cell power rails (`VPWR`/`VGND`) connect reliably to top-level metal power stripes without creating DRC notch violations.

### Stage 2: Placement
- **Global Placement (`gpl`)**: Monitor target density. If wirelength is excessive, inspect macro placement and pin constraints.
- **Detailed Placement (`dpl`)**: Ensure legal placement into standard cell rows with zero cell overlap.

### Stage 3: Clock Tree Synthesis (CTS)
- **Goal**: Minimize clock skew and insertion delay across all flip-flops.
- Verify that clock buffers (`clkbuf_*`) are selected from balanced drive-strength cells.
- If hold violations surge after CTS, verify that clock latency across distant registers is balanced.

### Stage 4: Routing & DRC/LVS Signoff
- **Routing Congestion**: If detailed routing reports unresolved DRC antenna violations or open nets, back up to floorplanning and reduce cell density by 5–10%.
- **Design Rule Checking (DRC)**: Magic or KLayout DRC violations (min spacing, min area, enclosure) must reach 0.
- **Layout Versus Schematic (LVS)**: Netgen LVS must report `Netlists match uniquely`.

---

## 3. Timing Closure Playbook

| Issue Encountered | Diagnosis | Remediation Action |
| :--- | :--- | :--- |
| **Setup Violation ($WNS < 0$)** | Data path too slow for target clock period | 1. Upsize driving cells along critical path.<br>2. Buffer long wire segments.<br>3. Move cells closer together in placement.<br>4. Pipeline RTL. |
| **Hold Violation ($Hold\ Slack < 0$)** | Data path faster than clock skew | Insert delay buffers (`clkbuf` or paired inverters) on short data paths. |
| **Vacuous P&R pass (no DEF written)** | Netlist never linked (e.g. STA-0164) yet exit stayed 0 | Treat missing/empty DEF as failure; fix the netlist or liberty mapping, never the metrics parser. |
| **Generic target + P&R requested** | Operator expressions unreadable downstream | Fail fast: re-synthesize with `nangate45` (or supply a liberty) instead of running a vacuous flow. |
| **Routing Congestion** | Too many wires competing for routing tracks | Reduce floorplan target utilization or increase die area. |
| **Antenna Violation** | Long metal wire accumulates charge during fabrication | Insert antenna diodes near input gates. |

---

## 4. Checklist for Physical Design
- [ ] Is core utilization configured conservatively ($40\% - 55\%$)?
- [ ] Did placement complete with zero cell overlap errors?
- [ ] Did CTS balance clock skew to $< 5\%$ of clock period?
- [ ] Is detailed routing complete with 0 open nets and 0 shorts?
- [ ] Does static timing analysis report $WNS \ge 0$ and $TNS = 0$?
- [ ] Has DRC and LVS passed with zero violations (naming the deck/setup that produced the verdict)?
- [ ] Were FORMAL-guarded asserts proven (not merely linted) before signoff?
- [ ] Is the P&R input netlist liberty-mapped (not bare generic)?
- [ ] Does a DEF artifact exist on disk for every reported P&R "success"?
