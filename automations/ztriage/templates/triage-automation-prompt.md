# Triage automation prompt

> Prompt source for Codex setup. Resolve every placeholder before use. Scheduling requires the user's request; use the discovered `automation_update` tool and its current schema.

Read and follow `.codex/automation-packs/ztriage/skills/triage-issue-reports/SKILL.md` for this run.

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

Read `.codex/automation-packs/ztriage/references/delivery.md`. Process only new top-level reports in the configured source channel. Codex schedules do not supply Slack event payloads: scheduled polling requires configured durable state and atomic claims; without a working delivery adapter, stop before writes.

Treat the source channel and root thread timestamp as immutable. If either is missing or does not match configuration, stop without posting or writing to the issue tracker.

The committed operational file owns classification, attachment review, cause tracing, routing, dedupe, tracker writes, and the final verdict. Post no progress messages. Never post a root message in the source channel.

The coordinator is the only Slack poster. Any delegated worker must be read-only, return findings only, and receive an explicit ban on every Slack write action.

End the single verdict with exactly one configured marker:

```text
[ztriage:bug]
[ztriage:performance]
[ztriage:other]
```

A bug or performance marker may add `tracker=<URL>`.
