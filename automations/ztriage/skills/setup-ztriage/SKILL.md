---
name: setup-ztriage
description: Configure Ztriage's Slack triage and reproduction workflows, project skills, delivery mode, and automation settings when installing or updating the Ztriage pack.
---

# Set up Ztriage

This is a dormant direct-read instruction file. Start from the pack's `FOR_AGENTS.md`; do not register Ztriage's operational directories as public skills. Setup does not authorize creating, updating, or enabling a live automation. Never put secrets in prompts or committed files.

## Install and preserve local work

Use the target repository named by the user or infer it from the active checkout. Ask only if it is ambiguous. Merge the complete source pack into `<target-repository>/.codex/automation-packs/ztriage/`. Preserve destination-only files, user-owned settings, and local edits. Review differing source-managed files and merge them; ask before replacement only when ownership cannot be resolved. If already reading the target copy, verify it in place.

Use the repository's Codex installation workflow to make these shared zstack skills available under the target's `.agents/skills/`:

- `why`, `tdd`, `unslop`
- `principle-separate-before-serializing-shared-state`
- `principle-minimize-reader-load`
- `principle-guard-the-context-window`
- `principle-sequence-verifiable-units`
- `principle-fix-root-causes`
- `principle-prove-it-works`

Verify each project's readable `SKILL.md` and its references in the actual automation checkout. A symlink must resolve there; a link to this machine's external checkout is not portable. Do not count skills inherited in the current conversation or a user-only install. Preserve existing project skills rather than replacing them. Shared role preferences, if needed, belong in `.agents/zstack-models.md` and default to inheriting the parent model.

The pack lives outside `.agents/skills/` and is read directly by its stable repository-relative paths. Do not use plugin cache paths in live prompts.

## Configure the target

Read `../../FOR_AGENTS.md`, `../../templates/configuration.example.yaml`, and `../reproduce-and-fix-issues/references/feature-map.example.md` from the copied pack. Create user-owned copies outside it, for example:

- `.agents/ztriage/configuration.yaml`
- `.agents/ztriage/feature-map.md`
- `.agents/ztriage/routing.md`

Preserve existing configuration on refresh. Keep secrets in the configured secret manager or environment. Keep durable processing state outside source control and outside disposable worktrees. Commit secret-free pack, dependency, and configuration files when required by the chosen checkout, but do not commit on the user's behalf without authorization.

Resolve the source Slack channel, optional operations channel, repository/default branch, triage identity, tracker target and supported actions, routing map, control adapter, feature map, status strings, PR URL form, and bounded effort budgets. Use connected tools to resolve known values before asking. Resolve any remaining value that affects a write before enabling it.

Use only model choices supported by the current Codex surface. Inherit the parent's model for delegated work unless the user or applicable project instructions explicitly select an available override. If a scheduler requires explicit model/reasoning fields, use the actual supported project choice; never copy another product's model slug or invent one.

## Check connected capabilities

Discover the configured Slack and tracker connector tools and inspect their current schemas. Triage needs thread reads and replies, usable attachment reads, tracker search/read/create/update, and compensation for an issue created by this run when its Slack handoff fails. Reproduction also needs repository/history access, draft PR creation, the control adapter, and optional operations-thread posting/editing.

Prefer connected Slack tools. A configured `ZTRIAGE_SLACK_BOT_TOKEN` may fill a narrow attachment or operations-edit gap; do not display it or pass it to a delegate. Never use undocumented endpoints. Missing capabilities block the corresponding workflow rather than silently changing its behavior.

If routing or owner pings are wanted, adapt `../triage-issue-reports/references/routing.example.md` outside the pack. Default pings off; permit only configured feature owners or strongly evidenced regression authors.

Read `../reproduce-and-fix-issues/references/control-adapter.md` and verify the completed feature map. Run its harmless setup check: start the correct app, navigate a mapped feature, exercise disposable state, inspect read-only state, capture a screenshot and short recording, and clean up. If any required capability is unavailable, leave reproduction disabled.

Codex subagents commonly inherit tools and environment access. A prompt prohibition is not credential isolation. If tool isolation cannot remove Slack writes and credentials, perform Slack-sensitive work in the coordinator. Do not claim that a worker lacks tools merely because its prompt forbids them.

## Choose report delivery

Read `../../references/delivery.md`. The installed Codex `automation_update` tool supports recurring schedules; do not invent a Slack-message trigger parameter. Choose one delivery mode supported by the user's environment:

- Manual invocation with a complete report envelope.
- An existing event adapter that supplies and validates that envelope.
- Scheduled polling, explicitly authorized by the user, with durable state, overlap protection, a fixed initial watermark, and a bounded batch.

If the user wants event-driven delivery but no event adapter exists, explain the missing capability and leave scheduling untouched. Do not silently replace events with polling. Scheduling is not required to prepare and verify this pack.

## Prepare and manage automations

Build each complete prompt from `../../FOR_AGENTS.md`, finished configuration, the delivery contract, and the matching template in `../../templates/`. Point each prompt at its exact operational file under `.codex/automation-packs/ztriage/`. Verify files are readable in the execution checkout and committed if that checkout needs committed files. Apply `$unslop` to the final prompt and names. Keep each prompt within 10,000 estimated tokens; keep secrets and notification preferences out of it.

When the user asks to schedule or update:

1. Discover `automation_update` and follow its current schema. Do not call a guessed backend, construct protocol links, or write automation TOML directly.
2. For an existing automation, inspect `$CODEX_HOME/automations/*/automation.toml` (falling back to `~/.codex/automations/*/automation.toml` when unset) to identify its id, view it through the tool, and preserve fields the user did not ask to change. Never create a duplicate as an update workaround.
3. Prefer a thread heartbeat for recurring follow-up. Use standalone local project jobs only when the user explicitly requests separate tasks or standalone project work; discover `list_projects` to resolve the real project id.
4. Use the user's local timezone and schedule. For a standalone job, supply the tool's required supported model/reasoning and execution fields. Do not assume the schema accepts Slack events, trigger payloads, webhooks, or environment variables.
5. Create or retain the appropriate paused state until delivery, capability, and thread-safety checks pass. Reuse existing authorization: do not ask for a second approval when the user already authorized this exact configuration.
6. If the management tool is unavailable, deliver the prepared prompt and state that scheduling was not completed.

No live automation creation or external test post is part of authoring this pack. Perform a harmless live test only when the user has authorized that test channel/report and the associated writes.

## Validate before normal traffic

Verify the actual execution checkout, dependencies, prompt paths, and non-secret config. Then verify:

1. Triage freezes root coordinates and posts exactly one verdict as a reply.
2. Exactly one configured marker appears, under the configured triage identity.
3. Reproduction accepts only that identity and preserves the same source coordinates.
4. No source-channel root post occurs, including error handling.
5. Missing coordinates, a deleted parent, or failed preflight produces no Slack or tracker writes.
6. Workers have no Slack write access; otherwise use the coordinator.
7. Duplicate delivery and overlapping runs do not create duplicate tickets, verdicts, operations roots, or PRs. Ambiguous write outcomes stop for reconciliation.

Enable normal traffic only after the relevant checks pass and the user has authorized that live automation. Record remaining blocks explicitly.
