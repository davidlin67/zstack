# Working on zstack

zstack is Zwift’s Codex-native engineering workflow collection. Its main workflow is `$zmode`. Keep the engineering principles and playbooks usable without Cursor or Claude Code.

- Public skills live in `skills/<name>/SKILL.md`. `.agents/skills/` links expose the same sources to Codex in this checkout; keep one source of truth.
- Read the relevant skill and references before changing its workflow. Use `$skill-name` in examples. Preserve explicit-only invocation in `agents/openai.yaml`.
- Use the tools actually offered by the session. Do not invent tools, model identifiers, custom agent types, cloud isolation, scheduled triggers, or access to history.
- Subagents inherit the parent model by default. Only apply an explicit user model choice if the current tool schema supports it. Agent briefs in `agents/` are prompt references, not registered agent types.
- Role preferences, when configured, live in `.agents/zstack-models.md`; they are instructions, not Codex configuration keys.
- Keep automations dormant unless setup or scheduling is requested. External messages, publishing, merging, and destructive actions need authorization within the task.
- Keep source attribution in `NOTICE.md` and preserve existing user changes. Do not install skills outside this checkout while developing it.

Run `python3 scripts/validate-codex.py` after changes. For runtime changes, also run the affected package's tests and typecheck; see its `package.json`. The statechart tests require Node.js with TypeScript support, Java, and the TLC tooling documented by the skill. The PR watcher uses Bun.

The platform contract is documented in `docs/harness/codex.md`. Keep product branding consistent with zstack and Zwift. Model-checker fixtures are test data, not agent instructions; preserve their semantics when updating names or paths.
