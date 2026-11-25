# ztriage

ztriage supplies two Codex automation workflows for Slack issue reports: triage and evidence-based reproduction with an optional draft fix. These files are dormant setup and operational references, outside the skill discovery root.

1. Point Codex at [`FOR_AGENTS.md`](./FOR_AGENTS.md) and name the target repository.
2. Merge this pack into `.codex/automation-packs/ztriage/`, preserving destination-only files and reviewing conflicts.
3. Install shared zstack skills under the target repository's `.agents/skills/` using the repository's Codex setup instructions.
4. Keep user-owned settings outside the pack, for example in `.agents/ztriage/`. Adapt the [configuration example](./templates/configuration.example.yaml) and [feature map](./skills/reproduce-and-fix-issues/references/feature-map.example.md).
5. Choose report delivery: manual envelopes, an existing event adapter, or explicitly requested scheduled polling. Codex recurring automations do not supply a native Slack event trigger. Polling requires the [delivery contract](./references/delivery.md).
6. Verify dependencies, connected tools, thread safety, and the selected checkout's files before enabling normal traffic. Scheduling or changing a live automation requires the user's request; setup alone does not enable it.

Slack and tracker writes are permitted only within the explicitly configured automation scope. Missing tools or uncertain source coordinates stop the run without a write.
