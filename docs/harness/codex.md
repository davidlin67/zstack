# Codex platform contract

This edition runs directly in Codex. Skills contain Codex instructions; no Cursor or Claude adapter is required. The portable package uses the `zstack` identity and Zwift branding. Its primary workflow is `$zmode`.

## Discovery and installation

The canonical public skill sources are `skills/<name>/SKILL.md`. Relative symlinks in `.agents/skills/` make those sources discoverable inside this checkout. Codex supports symlinked skill folders. For another repository or personal use, `scripts/install-skills.py` creates links only when no conflicting entry exists.

The portable root `plugin.json` supplies plugin identity. Its `extensions.com.openai` object supplies interface metadata and onboarding. Plugin hosts discover the real directories in `skills/`; the `.agents/skills/` links are only for repository discovery. There is no Cursor manifest or generated second skill tree.

To distribute this as a local plugin instead of linking individual skills, add it to a Codex marketplace using the documented marketplace format, then install it through the plugin UI. A marketplace entry is a catalog entry, not installation. Do not enable both the plugin and linked copies of the same skills in one project.

## Invocation and persistent instructions

Explicit skill invocation uses `$skill-name`. An agent can also read a bundled skill's `SKILL.md` and follow it. Skills formerly marked explicit-only preserve that policy in `agents/openai.yaml` with `policy.allow_implicit_invocation: false`. Public skill instructions remain in `SKILL.md`, not in the interface metadata.

Repository conventions belong in `AGENTS.md`. Ask to use `$zmode` for a task and follow-ups, or add a scoped repository instruction when persistence is wanted. The skill does not create a persistent UI mode.

## Tools and delegates

Tool availability depends on the Codex surface and session. Use the schema actually exposed; the names below describe capabilities, not a promise that every session has them.

| Work | Codex approach |
| --- | --- |
| Read, search, edit, execute | Available filesystem/shell tools; prefer `rg` for searches and a patch tool for edits. |
| Delegate | Available collaboration tools, such as `spawn_agent`, `send_message`, and `wait_agent`; otherwise do the work directly and keep a separate review pass. |
| Use an agent brief | Read `agents/zmode-agent.md` or `agents/comment-reviewer.md` and put the relevant instructions and paths in a worker brief. These files do not register agent types. |
| Isolate writers | Assign disjoint files or create and name a worktree before delegating. Spawning an agent does not isolate the filesystem. |
| Track a plan | Use a plan tool when available; otherwise keep a short checklist and progress updates. |
| Ask a question | Use an available question tool or ask in chat. Continue independent authorized work while an optional answer is pending. |
| Inspect prior chats | Discover thread tools first and scope retrieval to the task. Use supplied transcripts when tools are absent. Do not guess private history paths. |
| Verify a UI or CLI | Prefer an existing verification skill or harness, then available browser/app tools or the project's CLI. Do not assume Cursor control skills are installed. |
| Open or inspect a PR | Use available forge tools or an authenticated CLI. Publishing and external messages stay within the user's authorization. |

Delegates inherit the parent model and effort. `.agents/zstack-models.md` contains optional explicit project preferences that skills read themselves. It is not native Codex configuration, cannot grant model access, and does not change parent settings. Apply overrides only when chosen by the user and supported by the active tool. A session may require a fresh context for overrides; pass all grounding in the brief. Independent review works with the same model and separate briefs.

## Long runs and automations

Keep a requested task running in the current chat until its finish condition is met or a real blocker requires input. Use goal tools only when the user explicitly asks for a goal. Do not invent a `/loop` command or create an automation just to monitor an active job.

For requested scheduled or recurring work, discover the Codex automation tool and follow its actual schema. The dormant Ztriage pack uses this approach. Native scheduling does not imply Slack event triggers or webhook wakes. Polling needs a real durable delivery/claim adapter; see the pack's [delivery contract](../../automations/ztriage/references/delivery.md).

Local execution requires the execution host to remain available. A skill cannot promise that work will continue after the host sleeps or the app exits. Remote execution and service connections must be available and configured in the current environment.

## Sources and assets

Platform choices were checked against the current bundled Codex manual and the tools exposed in this session on November 25, 2026. The relevant official guides cover [skills](https://developers.openai.com/codex/skills), [repository instructions](https://developers.openai.com/codex/guides/agents-md), and [portable plugin structure](https://developers.openai.com/plugins/build/plugins#plugin-structure).

The repository has no image assets. The guide uses text and Mermaid diagrams. Source attribution is kept in [NOTICE.md](../../NOTICE.md). The statechart corpus is executable test data and retains its original model semantics; recorded source paths use the zstack package name.

The [migration inventory](../codex-file-review.tsv) accounts for all 554 original non-Git files, including preserved OS metadata, and the files added by the migration. Git internals, dependency installs, and Python bytecode are outside the source review. Rows marked preserved were reviewed and needed no platform change.
