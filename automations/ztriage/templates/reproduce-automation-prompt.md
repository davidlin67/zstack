# Reproduce automation prompt

> Prompt source for Codex setup. Resolve every placeholder before use. Scheduling requires the user's request; use the discovered `automation_update` tool and its current schema.

Read and follow `.codex/automation-packs/ztriage/skills/reproduce-and-fix-issues/SKILL.md` for this run.

Configuration source. Include this repository-relative path only when it is committed in the same target repository. Otherwise paraphrase the configured values. Never use a plugin source or cache path:

```text
{{ZTRIAGE_CONFIG_PATH}}
```

Report envelope supplied by a validated caller or delivery adapter:

```json
{
	"source_channel_id": "{{SLACK_CHANNEL_ID}}",
	"message_ts": "{{SLACK_MESSAGE_TS}}",
	"thread_ts": "{{SLACK_THREAD_TS_OR_EMPTY}}"
}
```

Read `.codex/automation-packs/ztriage/references/delivery.md`. Process only new top-level reports in the configured source channel. Codex schedules do not supply Slack event payloads: scheduled polling requires configured durable state and atomic claims; without a working delivery adapter, stop before writes. Use the configured repository, default branch, issue tracker, control adapter, feature map, and draft pull request capability.

Treat the source channel and root thread timestamp as immutable. If either is missing or does not match configuration, stop without posting.

Wait for a configured triage marker from the configured triage identity in this exact thread. Proceed only for `[ztriage:bug]` or `[ztriage:performance]`.

Require the configured control-adapter skill before attempting a repro. Reproduce the exact discriminating symptom twice through the real UI. Verify existing pull requests or commits without authoring over them. Attempt a bounded fix only after a confirmed repro and the operational file's fix gate.

The coordinator is the only Slack poster. Every child prompt must forbid `SendSlackMessage`, `PostToSlack`, `chat.postMessage`, and all other Slack writes. Children return findings only.

Never post a root message in the source channel.
