---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for $arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
---

# Arena

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Read the optional `arena runners` line in `.agents/zstack-models.md`. Without it, use three independent candidates that inherit the parent model and effort. Repeated `inherit-parent` or `auto` entries each count as a candidate. Honor an explicit model or effort choice only if the active delegation tool supports it and the active instructions permit it. Report an unavailable choice; do not invent a replacement ID or claim a multi-model comparison when every candidate inherits. Choose different design briefs or seeds when that improves exploration. Respect the active concurrency limit and launch later candidates as slots free up.
4. Give each candidate its own output location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle skill.

## Phase B: Fan out

Use the available Codex subagent spawn tool (for example, `collaboration.spawn_agent` when exposed). Give each candidate the task, the shared grounding, its own output path, and instructions to produce the artifact plus a short rationale naming the alternatives it rejected. Pass ordinary task instructions explicitly; a file in `agents/` is not a registered subagent type. Use separate worktrees or disjoint output directories because local delegates share the filesystem. Track the returned IDs and drain their results using the available wait and messaging tools. If delegation is unavailable, report that the independent candidate comparison could not run rather than presenting sequential self-review as an arena.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all Phase B candidates complete, ask a fresh subagent to judge without editing. Use the optional `arena cross-judge pool` preference when supported, otherwise inherit the parent model and effort. Independence means a separate brief and context, not a claimed different vendor. Give the judge the rubric and candidate artifacts, without your preferred winner or the candidates' self-scores. The judge scores each candidate by path label on each rubric criterion and recommends a base. A different supported model is useful only when the user explicitly selected it; say when model diversity was unavailable. If no delegation is available, mark the independent judgment missing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
