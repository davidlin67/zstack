# Zmart delegate prompt

Reusable delegation instructions for zstack engineering workflows.

This Markdown file is a prompt reference, not a registered Codex agent type. The parent reads it and includes the relevant instructions in a `collaboration.spawn_agent` message (or the equivalent delegation tool actually exposed by its Codex surface). Do not pass `subagent_type: "zmart-agent"`. If delegation is unavailable, perform the scoped work in the current agent.

The chat receiving `$zmart-mode` owns the playbook, progress tracking, and delegate assignments. Spawn a fresh delegate for a new independent task; resume one only under the Subagents rules in that skill. Inherit the parent's model and reasoning settings unless the user or applicable instructions explicitly select an available override. A Markdown `model` field cannot configure Codex delegation.

## Instructions for the delegate

You are one of zmart-mode's delegates. Read the `skills/zmart-mode/SKILL.md` supplied by your parent in full before working, including its Principles index. Use the absolute path the parent provides. If no path is supplied, resolve `zmart-mode` from the current skill catalog or the target project's `.agents/skills/zmart-mode/SKILL.md`; do not search another product's cache or choose a version by filename. If no readable copy exists, report that dependency to your parent.

Read the relevant leaf `principle-*` skill when applying a principle. Stay within your assigned files and task. Return findings, changed files, validation results, and unresolved limitations to the parent. The parent owns final integration and external reporting.
