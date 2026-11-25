---
name: no-comments
description: "Review scoped comments independently, fix accepted findings, and offer executable checks for claimed constraints."
---

# No comments

Ask an independent comment reviewer to inspect the scope. Act on accepted findings after checking their evidence.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Spawn an available Codex subagent with a brief to read `../../agents/comment-reviewer.md` (resolved from this skill directory in the installed collection) and review the scope. Supply the resolved absolute path; the Markdown file is a brief, not a registered subagent type. If delegation is unavailable, run its review directly and mark the missing independent pass. Use the available delegation tools and inherit the parent model and reasoning effort unless the user explicitly configures an available override. Respect the active concurrency limit. Do not restate its rules.
2. Inspect the report against the assigned scope and the reviewer's keep rules. Reject application-code edits, scope escapes, removals covered by a keep rule, unsupported `REFACTOR` flags, and conclusions without evidence. Inspect missed lint and TypeScript suppressions; correctness or safety suppressions require fixing the underlying issue before removal. Trace a symbol or use `$why` when a claim such as `IMPORTANT` or `do not remove` depends on history. Resolve uncertain keep decisions before editing. Apply accepted comment removals yourself. If the report needs correction, rerun once with the specific defect named; after a second rejected report, report the review incomplete.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run `$architect` once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principle-fix-root-causes** and **principle-redesign-from-first-principles** skills guide intent only. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards.
5. Preserve comments covered by the reviewer's keep rules, including legal notices and public API contracts. For a real constraint that can be enforced, offer the smallest in-scope type, runtime check, test, or CI rule. Use existing authorization when it covers that change; otherwise request approval for the concrete proposal. Encode the constraint before removing its comment. Leave unsupported or out-of-scope changes open rather than deleting an unresolved constraint.
6. Report reviewed files, accepted comment removals and their count, resolved and open `REFACTOR` findings, exclusions, verification, and any remaining constraint proposal.
