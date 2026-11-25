# Ztriage automation requirements

Ztriage is zstack's issue-report workflow for Codex. Configure two cooperating workflows in one Slack issue channel. These requirements describe the intended operation; setup alone does not authorize live scheduling or external writes.

## Triage issue reports

- Process each new top-level report through the validated delivery mode chosen during setup, preserving its original thread coordinates.
- Read the thread and attachments, classify the report, and trace the likely owning layer before routing. Categories are bug, performance issue, feature request, question or feedback, and reroute.
- Search the configured tracker for duplicates, update a confident duplicate, and create a ticket only for a clear net-new bug.
- Require Slack thread read and reply access, the configured tracker integration, and any configured routing map.
- Post exactly one source-thread verdict ending with `[ztriage:bug]`, `[ztriage:performance]`, or `[ztriage:other]`. Bug and performance markers may include the tracker URL.
- Never post a root message in the source channel.

## Reproduce and fix confirmed bugs

- Process the same validated report envelope and wait for a trusted triage marker in the original thread.
- Stop when someone clearly owns the fix. When a pull request or merged commit may fix the report, verify it instead of creating a competing change.
- Use the configured control adapter and feature map to reproduce the exact symptom twice through the real UI. Capture screenshots, video, and a read-only state cross-check.
- After confirmed reproduction, attempt at most one bounded root-cause fix. Use TDD when a test is cheap, check the blast radius, and open a draft pull request only after before-and-after proof passes.
- Require Slack thread access, repository and history access, draft pull request creation, the configured tracker, and the control adapter.
- Keep source and optional operations-thread updates concise and supported by evidence.
- Never post a root message in the source channel. Never merge or deploy.

## Shared boundaries

- Keep source-channel and root-thread coordinates immutable.
- Treat utility and debug bots as evidence, not delegation or fix ownership.
- Subagents may help only when Slack credentials and write capabilities can be excluded. A prompt prohibition alone is not isolation.
- Copy this entire pack to `.codex/automation-packs/ztriage/` in the target repository. Its `SKILL.md` files are direct operational references, not registered public skills.
- Expose shared zstack dependencies such as `why`, `tdd`, `unslop`, and the required principles through project skills under `.agents/skills/`.
- Make each live prompt read its operational file directly by a stable repository-relative path. Avoid plugin cache paths, copied excerpts, and implicit discovery.
- Keep user-owned configuration, feature maps, routing maps, and secrets outside the copied pack so refreshes cannot overwrite them.
- Stop without writes when required coordinates, tracker access, control capabilities, or the feature map are missing or uncertain.

## Target configuration

Resolve these values during setup:

- Source Slack channel and optional operations channel.
- Repository, default branch, and tracker type, team, project, labels, and intake status.
- Optional routing-map path and trusted triage Slack identity.
- Required control skill or adapter and completed feature-map path.
- Available model preferences for triage, reproduction, code, and media review; inherit the parent by default.
- Status strings for seen, reproducing, reproduced, blocked, fixing, failed, and pull request opened.
- Budgets for polling, verdict wait, follow-up, reproduction, rejection, and fixes.
- Optional bot-token capability limited to file downloads or editable operations status.

Adapt the [configuration example](./templates/configuration.example.yaml) and [feature-map example](./skills/reproduce-and-fix-issues/references/feature-map.example.md) into user-owned files, such as `.agents/ztriage/`. Store secret values in a secret manager or environment.

## Setup entry point

1. Use the named or active target repository; ask only when it is ambiguous.
2. Treat this file's directory as the source pack and merge it into `<target-repository>/.codex/automation-packs/ztriage/`.
3. Preserve destination-only files, unrelated files, and user-owned configuration. Review source-managed conflicts and merge local edits; ask before replacement only when ownership is unresolved.
4. Verify that the copied `FOR_AGENTS.md` and `skills/setup-ztriage/SKILL.md` exist.
5. Read and follow the copied `.codex/automation-packs/ztriage/skills/setup-ztriage/SKILL.md` directly.

Install shared dependencies through the repository's Codex workflow under `.agents/skills/`. Verify their `SKILL.md` files are readable in the target checkout. A user-only install or instructions inherited by the current chat do not establish project availability. Keep Ztriage's operational files outside the public discovery root.

Report which pack, dependency, and secret-free configuration files must be committed for the selected checkout. Do not commit unless requested. Create or update a live automation only when the user explicitly asks.

Codex scheduling does not supply native Slack-message triggers. Choose manual report envelopes, an existing event adapter, or explicitly requested scheduled polling with durable duplicate suppression. Polling must satisfy the [delivery contract](./references/delivery.md); do not invent event-trigger API fields.

When scheduling is requested, discover `automation_update` and follow its current schema. Prefer a thread heartbeat; use standalone project runs only when explicitly requested. Preserve existing automation ids and unrelated settings, avoid duplicates, and verify the finished prompts and operational paths before scheduling.
