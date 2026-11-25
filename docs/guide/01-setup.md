# Set up zstack for Codex

This edition uses Codex skills directly. You can use the inherited parent model without configuring any model roles.

## Expose the skills

Inside this checkout, `.agents/skills/` contains relative links to the canonical `skills/` directory. Start a new Codex chat here and invoke `$zmode-help` or `$zmode`.

For another repository, run the installer from this checkout:

```bash
python3 /absolute/path/to/zstack/scripts/install-skills.py --project /absolute/path/to/your-repo --dry-run
python3 /absolute/path/to/zstack/scripts/install-skills.py --project /absolute/path/to/your-repo
```

Use `--user` instead for personal installation in `~/.agents/skills`. The script refuses to replace existing skills, and repeating it creates no duplicate links. Keep this checkout in place: linked skills use its files. Start a new chat after installation.

The root portable `plugin.json` can also be used by the Codex plugin system. Choose one installation method so the same skills do not appear twice. See the [platform contract](../harness/codex.md).

## Optional model preferences

```text
$setup-zstack
```

[`$setup-zstack`](../../skills/setup-zstack/SKILL.md) records explicit per-role choices in `.agents/zstack-models.md`. Skills read this file themselves. It is not a Codex settings file and cannot make an unavailable model runnable.

Every role defaults to `inherit-parent`. The coordinator omits the model override and lets the subagent inherit. A model or effort override applies only when you explicitly choose it and the current session supports it. Model diversity is optional; separate reviewers can use independent briefs on the same model.

For a cheaper run, ask for fewer candidates, narrower reviews, or a smaller scope. Parent model selection remains a Codex setting; setup does not silently rewrite it.

## Establish a verification path

When setup involves proving app behavior and no driver exists, it mentions [`$create-verification-skill`](../../skills/create-verification-skill/SKILL.md), which creates `.agents/skills/verify-<app>/` and proves a real flow works before handing it over.

For concurrency, retries, parsers, or state machines, [`$create-formal-verification-skill`](../../skills/create-formal-verification-skill/SKILL.md) can verify one property within stated bounds. These are optional additions, not prerequisites for every task. [Verify and ship](./06-verify-and-ship.md) explains both.

## Run a first task

```text
$zmode add a --json flag to this command. text output stays byte-identical. verify both.
```

The skill selects the Feature playbook and keeps a plan using the session's plan tool when available. Otherwise it tracks progress in concise updates.

For continuity, say “use `$zmode` for this task and follow-ups.” To make it a repository convention, add a short instruction to `AGENTS.md` that names the skill and when it applies. The skill does not require a persistent UI mode.

Next: [Route work through `$zmode`](./02-zmode.md).
