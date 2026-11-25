# Report delivery and duplicate suppression

Each operational file handles one report envelope. Scheduled Codex runs do not automatically receive a Slack event. Do not leave template placeholders in a live prompt or invent trigger fields in the automation API.

## Envelope

A manual caller or an existing validated event adapter supplies:

```json
{
  "source_channel_id": "configured-channel-id",
  "message_ts": "root-message-timestamp",
  "thread_ts": ""
}
```

All timestamps are strings. A nonempty `thread_ts` must name the same root as `message_ts`; a new report is a top-level message, not a reply. Reject missing, malformed, or mismatched coordinates before any write. Compare the channel with configuration and fetch the actual root to verify it.

## Scheduled polling

Use polling only after the user explicitly chooses its cadence, initial watermark, and standalone-project or thread execution mode. Poll only the configured channel, paginate completely over the selected interval, ignore replies, and build validated envelopes for new roots. Do not process historical reports before the initial watermark unless requested. Limit each run to the configured batch and effort budget; later reports remain pending.

Configure a durable state path outside source control and disposable checkouts. Both workflows must be able to find it on the actual execution machine. If a run cannot access the same state or enforce exclusive processing, it must stop before external writes.

The delivery adapter must implement an atomic claim for `(repository, source_channel_id, root_timestamp, workflow)` and prevent overlapping owners. Use a tested local transaction/locking implementation or an existing queue that supplies equivalent guarantees. A prose claim, writing a JSON file without locking, or an expiring lease without fencing cannot enforce exclusivity. If no such implementation exists, leave polling disabled; this pack specifies the contract and does not ship a queue implementation.

Store per-report progress separately from the scan watermark. Persist discovered pending reports before advancing the watermark, and keep reproduction reports pending while waiting for triage. Expire missing verdicts only under the configured verdict budget. A later run resumes pending work rather than treating a scanned report as complete.

## Writes and recovery

Before every tracker, Slack, or PR write, recheck the live source and search for the recorded or discoverable artifact for this report. Store operation intent, returned artifact ids, workflow phase, and completion state durably. A trusted existing triage marker suppresses a duplicate verdict; an existing operations root or draft PR must be reused rather than recreated.

An atomic local claim does not make a remote write exactly once. After a timeout, process crash, or lost response, mark the operation uncertain and reconcile using the source permalink and artifact ids. Do not blindly retry an uncertain write. If reconciliation cannot establish its outcome, leave the report blocked for operator review. Retain dedupe records for the configured retention window; do not delete unresolved records.

The triage workflow may post one verdict per report. The reproduction workflow may post only the source updates permitted by its operational file. Retrying delivery does not reset those limits. Stop and release owned resources on request or budget exhaustion; preserve unresolved progress for the next run.
