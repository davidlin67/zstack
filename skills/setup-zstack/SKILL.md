---
name: setup-zstack
description: Configure project-local zstack delegation preferences using available Codex models and reasoning options. Use for $setup-zstack, "configure zstack models", or "zstack budget".
---

# Setup zstack

Configure zstack's delegation preferences for this project in `.agents/zstack-models.md`. This is a file the zstack skills read, not a native Codex configuration file. It does not change the chat's model, install an automation, or override Codex permissions.

## Detect and preserve

Read the active instructions and the schemas of the delegation tools available in this session. They determine which models, reasoning efforts, and concurrency limits can actually be used. Do not probe invented model APIs, derive model IDs by editing strings, or assume a provider is available.

Read `.agents/zstack-models.md` if it exists. Preserve the user's supported choices and flag an unavailable override instead of silently substituting a model. Without a file, all roles inherit the parent model and effort.

## Choose preferences

Use choices already provided by the user. Ask only for preferences needed to complete the setup: inheritance or supported explicit overrides, and how many independent arena candidates or reviewers to run. Two candidates and one separate judge are useful starting points; the active concurrency limit determines how many run at once. Ask a short chat question when no question tool is available.

An `inherit-parent` or `auto` entry means omit both model and reasoning overrides. A requested model override is usable only when the active spawn tool accepts it and higher-priority instructions permit it. Some tools require a fresh context when an override is selected; use their documented options and include all necessary grounding in the brief.

Keep effort separate from the model ID. If a budget is requested, record it as a preference; use only supported effort values and do not silently change existing model choices. A preference file cannot change the parent chat's reasoning setting.

## Write and check

Write or update the project file with the selected values. With inherited defaults, its shape is:

```text
# zstack delegation preferences
# Read by zstack skills, not by the Codex configuration loader.
# Repeated inherited entries create independent candidates on the parent model.
# Model overrides require explicit user choice and active tool support.
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: inherit-parent
arena runners: inherit-parent, inherit-parent
arena cross-judge pool: inherit-parent
swarm workers: inherit-parent
interrogate reviewers: inherit-parent, inherit-parent
```

Validate each role against the available delegation tool and read back the finished file. Preserve unrelated content and keep a rerun idempotent. Report the path, selected preferences, and any unsupported choice. The skills read this file on use; do not promise it is an automatically applied Codex rule.

## Verification helpers

If the question involves proving app behavior and the project has no driver, mention `$create-verification-skill`. For a race or invariant that tests cannot reach, mention `$create-formal-verification-skill`. Generate either only when requested; setup does not require either workflow.
