# Zstack

Zwift’s Codex-native engineering workflows for design, implementation, verification, and review.

Start with **zmode**. Give it a goal and a checkable finish condition; it selects a playbook and works toward a verified result.

## Install

Skills are already discoverable in this checkout through `.agents/skills/`. Start a new Codex chat in this repository and invoke `$zmode`.

To use them in another repository, link this checkout's skills into that repository:

```bash
python3 /absolute/path/to/zstack/scripts/install-skills.py --project /absolute/path/to/your-repo --dry-run
python3 /absolute/path/to/zstack/scripts/install-skills.py --project /absolute/path/to/your-repo
```

For personal use across repositories, use `--user` instead of `--project`. The installer refuses collisions and can be rerun safely. Links follow this checkout, so keep it in place. Choose one installation method per project to avoid duplicate skill entries.

The root `plugin.json` also packages the skills for the Codex plugin system, including OpenAI interface metadata and `$setup-zstack` onboarding. See the [Codex platform contract](./docs/harness/codex.md) for packaging, tool behavior, and platform limits.

## Get started

1. Optionally run [`$setup-zstack`](./skills/setup-zstack/SKILL.md) to record per-role preferences. Every role inherits the parent chat's model by default.
2. Use [`$zmode`](./skills/zmode/SKILL.md) for a task that needs rigor, with a goal and a checkable finish condition.

```text
$zmode users get two notifications after a retry. reproduce first, then fix and verify.
```

The [guide](./docs/guide/README.md) walks through setup, design, verification, and longer runs. [`$zmode-help`](./skills/zmode-help/SKILL.md) answers questions without starting a run.

## Usage

`$zmode` reads your request, selects a playbook, and uses other skills as needed. Explicit invocation uses `$name`; an agent can also read the corresponding `skills/<name>/SKILL.md` and follow it. No slash-command aliases or custom subagent types need to be registered.

### Just use [`$zmode`](./skills/zmode/SKILL.md)

zmode is the entry point for rigorous engineering work. It includes twenty-two playbooks:

```
$zmode this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro
first, then fix and verify.
```

```
$zmode i'm going to bed. land the stack even if ci flakes. i want everything merged by
morning.
```

<details>
<summary>the twenty-two playbooks</summary>

| playbook | for |
|---|---|
| [investigation](./skills/zmode/playbooks/investigation.md) | a read-only question. how does x work, why was y built this way, are we sure. |
| [bug fix](./skills/zmode/playbooks/bug-fix.md) | reproduce a defect, root-cause it, and fix with runtime evidence. |
| [perf](./skills/zmode/playbooks/perf-issue.md) | trace a measured slowness and improve it against a baseline. |
| [hillclimb](./skills/zmode/playbooks/hillclimb.md) | sustained, scientific improvement of one metric against a target, looping hypotheses with before/after measurement and one commit per accepted win. |
| [runtime forensics](./skills/zmode/playbooks/runtime-forensics.md) | diagnose a live symptom (leak, idle-cpu spin, glitch) from instrumentation. |
| [trace forensics](./skills/zmode/playbooks/trace-forensics.md) | diagnose a captured profiling artifact (cpuprofile, trace, spindump, heap snapshot). |
| [feature](./skills/zmode/playbooks/feature.md) | new or changed behavior, built from a named data shape. |
| [refactoring](./skills/zmode/playbooks/refactoring.md) | a behavior-preserving change to structure or shape. |
| [prototype](./skills/zmode/playbooks/prototype.md) | a throwaway sketch to make a design or behavioral decision cheaply, or to settle an empirical fork by observing it. |
| [visual parity](./skills/zmode/playbooks/visual-parity.md) | pixel-exact ui equivalence between two implementations. |
| [authoring a skill](./skills/zmode/playbooks/authoring-a-skill.md) | writing or editing a SKILL.md. |
| [eval](./skills/zmode/playbooks/eval.md) | test how a skill or prompt change affects agent behavior, blinded. |
| [babysit](./skills/zmode/playbooks/babysit.md) | drive a pr or a stack to merge-ready: conflicts, review threads, ci. |
| [shipping](./skills/zmode/playbooks/shipping.md) | independently verify a green stack, then land the contiguous verified run bottom-up through github by default or origin when available. |
| [autonomous run](./skills/zmode/playbooks/autonomous-run.md) | drive a long task to completion without stopping. |
| [autopilot-full](./skills/zmode/playbooks/autopilot-full.md) | run independent prs to merged with one owner per pr. a swarm verifies each code-ready head, and every later change to the patch gets a fresh check. |
| [autopilot-stack](./skills/zmode/playbooks/autopilot-stack.md) | autopilot-full without the merge. build and verify prs for the operator to review and land, stacking a pr only on a pr it builds on. |
| [session pickup](./skills/zmode/playbooks/session-pickup.md) | resume or take over a prior agent's in-flight work. |
| [pause safely](./skills/zmode/playbooks/pause-safely.md) | suspend in-flight work cleanly so it can be resumed later. |
| [multi-phase plan](./skills/zmode/playbooks/multi-phase-plan.md) | work that spans phases or stacked PRs. |
| [worktree cleanup](./skills/zmode/playbooks/worktree-cleanup.md) | reclaim disk by pruning merged or abandoned worktrees and stale ios simulators, safety-gated. |
| [opening a pr](./skills/zmode/playbooks/opening-a-pr.md) | open a ready pr from small ordered commits with a conventional commits title and a briefing-style body. used when opening a pr is requested. |

</details>



when invoked it:

1. matches your task to a [playbook](./skills/zmode/playbooks/) and tracks its steps with an available plan tool or concise progress updates.
2. routes to the other skills as the steps fire.
3. writes unslopped replies framed for the consumer and the maintainer.

the full rules and playbooks live in [`skills/zmode/SKILL.md`](./skills/zmode/SKILL.md).

To keep the workflow active for a task, say "use `$zmode` for this task and its follow-ups." For a repository-wide convention, add a short instruction to its `AGENTS.md`. A skill is a reusable workflow, not a persistent UI mode.

Long runs continue in the active chat until their finish condition is met. Use available Codex goal tools only when the user explicitly requests a goal; scheduled automations are for recurring work. Neither is a substitute for watching an active job through completion.

## Akills

[`$zmode`](./skills/zmode/SKILL.md) runs most of these for you when a step needs them (`why`, `architect`, `arena`, `swarm`, `interrogate`, `unslop`, `no-comments`, `technical-writing`, `tdd`, and the principles). the table below is for when you want one directly:

```
$how do we cancel runs? do we have an n+1 when we look up every run to cancel?
```

```
$interrogate review this pr.
```

<details>
<summary>all skills</summary>

| skill | use it when |
|---|---|
| [`$zmode`](./skills/zmode/SKILL.md) | default entry point for any non-trivial task. |
| [`$zmode-help`](./skills/zmode-help/SKILL.md) | you're new to zstack, or unsure which skill, playbook, or principle fits. finds out what you're trying to do, answers that part, and hands you a prompt to type. runs only when you type `$zmode-help`. |
| [`$in-your-own-words`](./skills/in-your-own-words/SKILL.md) | you want the agent to play back your goal and the problem before it starts. runs only when you type `$in-your-own-words`. |
| [`$sharpen`](./skills/sharpen/SKILL.md) | you want a prompt made deeper, not bigger, before you send it: what a top professional would do that you didn't ask for, the raw material they'd start from, their methods and tools, and an outside check that the result is right. hands back the rewritten prompt, which asks the agent to prototype any choice an experiment can settle and leaves product and preference choices to you. doesn't do the task. runs only when you type `$sharpen`. |
| [`$reframe`](./skills/reframe/SKILL.md) | you can't name what you're building, so you can't ask an agent for it clearly. starts from your files and your own words. if they could describe more than one problem, it lists the two or three it could be, with the sign that tells each apart, and picks the likeliest. then it gives 8 to 12 expert terms ranked by how much they'd change what you build, each tied to the part of your description it names and to a real project whose link it checked. borrows terms from 2 or 3 neighboring fields that solved the same problem under other names, says where each analogy breaks, then rewrites your description with the new words. runs only when you type `$reframe`. |
| [`$how`](./skills/how/SKILL.md) | you want a walkthrough of how a subsystem works. |
| [`$why`](./skills/why/SKILL.md) | you want to know why something was built this way. answers from the record, not the code: the commits and pr discussions that introduced it and each later change, and other sources when that trail is thin. cites what the authors wrote, marks its own inferences, and says what the record does not answer. |
| [`$recall`](./skills/recall/SKILL.md) | you're starting or resuming work and want your recent context on a topic rebuilt from your own chat history and the shared record, handed back as a tight current-state brief. |
| [`$ketchup`](./skills/ketchup/SKILL.md) | you want what changed in this chat since your last message, in plain words and small visuals, with every item waiting on you listed and decidable from the reply alone, even when that makes the reply long. |
| [`$ketchup-video`](./skills/ketchup-video/SKILL.md) | you want the `$ketchup` catch-up as a short subtitled video of slides, with the calls waiting on you as text under it. |
| [`$blast-radius`](./skills/blast-radius/SKILL.md) | you have a small-looking change and want to know what else it could break, with the one fact it's safe because of proven by running code, not asserted. |
| [`$architect`](./skills/architect/SKILL.md) | you're about to write code that crosses a function boundary and want the caller's usage, types, and module shape settled first. |
| [`$arena`](./skills/arena/SKILL.md) | you want N parallel attempts at the same thing, then to grab the best parts of each. |
| [`$swarm`](./skills/swarm/SKILL.md) | you want N parallel workers across different slices or races, then one aggregated report. |
| [`$interrogate`](./skills/interrogate/SKILL.md) | you have a diff and want independent reviewers to try to break it, keeping only findings a run proves. |
| [`$automate-me`](./skills/automate-me/SKILL.md) | you want your own `-mode` skill, drafted from how you've actually worked. |
| [`$make-bot-ui`](./skills/make-bot-ui/SKILL.md) | you want a page whose controls call a supported bot webhook through a local server, with credentials kept server-side. |
| [`$setup-zstack`](./skills/setup-zstack/SKILL.md) | you want to record supported explicit delegation preferences for this project. |
| [`$reflect`](./skills/reflect/SKILL.md) | a long task landed and you want the recipe captured as a skill edit. |
| [`$correct`](./skills/correct/SKILL.md) | you keep correcting agents for the same mistakes. mines history for mistake classes, fixes each at the highest level that works (architecture, then types, lint, and ci, then tests, with docs last), and keeps a table pairing each rule with what enforces it. |
| [`$teach`](./skills/teach/SKILL.md) | you want to actually understand a change or subsystem, not just have it summarized. runs how + why and weaves one plain explanation, built up diagram by diagram. |
| [`$tdd`](./skills/tdd/SKILL.md) | you're fixing a bug and there's a cheap local test path. write the failing test first, then the fix. |
| [`$benchmark-checklist`](./skills/benchmark-checklist/SKILL.md) | you ran a benchmark or measured a speedup or regression. vets the number (limiter, tuning, errors, repeat runs, end-to-end relevance) before you report or act on it. |
| [`$no-comments`](./skills/no-comments/SKILL.md) | strip comments before review; spawns Comment Reviewer, fixes accepted findings, offers encodings for claimed constraints. |
| [`$typescript-best-practices`](./skills/typescript-best-practices/SKILL.md) | you're reading or editing typescript. grounds the type-system-discipline principle in syntax. |
| [`$figure-it-out`](./skills/figure-it-out/SKILL.md) | no bundled playbook fits. designs a rigorous, auditable playbook for the task. |
| [`$show-me-your-work`](./skills/show-me-your-work/SKILL.md) | you want a reviewable decision trail. logs decisions to a tsv you can commit. |
| [`$create-verification-skill`](./skills/create-verification-skill/SKILL.md) | your project has no scripted way to prove app behavior. generates a project-local verify skill with a feature map, for any language or platform. |
| [`$maintain-verification-skill`](./skills/maintain-verification-skill/SKILL.md) | your verify skill's feature map has drifted from the app. source wave + one live pass, at most one PR of proven corrections. |
| [`$create-formal-verification-skill`](./skills/create-formal-verification-skill/SKILL.md) | tests can't reach the case that breaks a race, retry, state machine, parser, or unsafe code. verifies one property with the tool that fits and generates a project-local skill to recheck it on every change. |
| [`$maintain-formal-verification-skill`](./skills/maintain-formal-verification-skill/SKILL.md) | code your formal verification covers has changed since it was last checked. updates the model, harness, or properties to match the code, reruns, and says whether each failure is drift in the verification or a bug in the code. |
| [`$statechart`](./skills/statechart/SKILL.md) | someone who owns the behavior needs to see it, not read a spec. checks a tla+ model, draws what the user sees as a mermaid statechart, marks each state that breaks a rule, and gives the shortest path to each one. |
| [`$unslop`](./skills/unslop/SKILL.md) | you're cleaning up writing. removes AI tells. |
| [`$bro`](./skills/bro/SKILL.md) | you want the last message restated in plain human language, no jargon. |
| [`$technical-writing`](./skills/technical-writing/SKILL.md) | layered doc standard (Diátaxis + Google developer style + STE + Global English) for docs, RFCs, readmes, PR descriptions, commit messages. |

</details>



### Examples

Start a task with [`$zmode`](./skills/zmode/SKILL.md) and let it select the playbook. Invoke a narrower skill directly when its outcome matches the task.


<details>
<summary>all the examples</summary>

```
bug fix:           $zmode this pr has a subtle bug where the scroll drifts every 750ms even
                   when idle. repro first, then fix and verify.
perf:              $zmode a big list takes a second or two to load even though we virtualize.
                   run a cpu trace and tell me why.
feature:           $zmode build a small feature behind a feature flag. verify it really works.
prototype:         $zmode build two prototypes of the markdown renderer so we can compare.
                   spawn an agent for each.
multi-phase:       $zmode open source these skills as a plugin. nothing internal leaks, work
                   in a temp dir, show me the dependency graph first.
overnight run:     $zmode i'm going to bed. land the stack even if ci flakes. i want
                   everything merged by morning.
babysit:           $zmode check on pr 123. anything outstanding?
visual parity:     $zmode the row spacing is too tall when this flag is on. the second image
                   is correct. repro and fix until it matches.
figure it out:     $zmode i'm stepping away. migrate every caller from the synchronous store
                   to the new async one, keeping behavior identical. i want to trust it was done
                   right when i'm back.
how:               $how do we cancel runs? do we have an n+1 when we look up every run to cancel?
why:               $why is this feature flag not on yet?
architect:         design this instrumentation to be high signal with no false positives. $architect
                   this first.
arena:             $arena take my prompt to the arena verbatim. i want to compare their proposals
                   with yours.
swarm:             $swarm check every package under packages/ against its check.sh. one worker per
                   package. one report.
interrogate:       $interrogate review this pr.
tdd:               $tdd implement
unslop:            can we unslop and tighten the new changes?
reflect:           $reflect that took too long. capture what we learned so the next run doesn't
                   repeat it.
correct:           $correct
show-me-your-work: $show-me-your-work keep a decision trail i can review when i'm back.
automate-me:       $automate-me
help:              $zmode-help which skill should i use to review this branch?
```

</details>

## Agent briefs

[`agents/zmode-agent.md`](./agents/zmode-agent.md) and [`agents/comment-reviewer.md`](./agents/comment-reviewer.md) are reusable briefs. The coordinator reads the relevant brief and passes its instructions to an available Codex subagent tool. Markdown files do not register a `subagent_type`.

Subagents inherit the parent model. An explicit user choice can be applied only if the session supports it. Give parallel writers distinct file ownership or separate worktrees; spawning an agent alone does not isolate its filesystem.

## Principles

twenty-four short skills, one principle each. `zmode` indexes them inline and reads that index at task start. the standalone files are there so other skills can reference a principle by name, and so the index can point at the full rule for each.

<details>
<summary>all twenty-four principles</summary>

| principle | group | rule |
|---|---|---|
| [laziness-protocol](./skills/principle-laziness-protocol/SKILL.md) | core | Bias toward deletion and the smallest change that solves the problem. |
| [foundational-thinking](./skills/principle-foundational-thinking/SKILL.md) | core | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious. |
| [redesign-from-first-principles](./skills/principle-redesign-from-first-principles/SKILL.md) | core | Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on. |
| [attack-the-premise](./skills/principle-attack-the-premise/SKILL.md) | core | Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it. |
| [subtract-before-you-add](./skills/principle-subtract-before-you-add/SKILL.md) | core | Remove dead weight, redundant validators, and stub references first, then build on the simpler base. |
| [minimize-reader-load](./skills/principle-minimize-reader-load/SKILL.md) | core | Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. |
| [outcome-oriented-execution](./skills/principle-outcome-oriented-execution/SKILL.md) | core | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code. |
| [experience-first](./skills/principle-experience-first/SKILL.md) | core | Choose user delight over implementation convenience; ship fewer polished features over more rough ones. |
| [exhaust-the-design-space](./skills/principle-exhaust-the-design-space/SKILL.md) | core | Build 2-3 competing prototypes and compare side by side before committing. |
| [build-the-lever](./skills/principle-build-the-lever/SKILL.md) | core | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun. |
| [model-the-domain](./skills/principle-model-the-domain/SKILL.md) | architecture | Encode the domain in a structure instead of scattered conditionals. |
| [boundary-discipline](./skills/principle-boundary-discipline/SKILL.md) | architecture | Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions. |
| [type-system-discipline](./skills/principle-type-system-discipline/SKILL.md) | architecture | Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas. |
| [make-operations-idempotent](./skills/principle-make-operations-idempotent/SKILL.md) | architecture | Converge to the same end state regardless of partial prior runs. |
| [migrate-callers-then-delete-legacy-apis](./skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | architecture | Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. |
| [separate-before-serializing-shared-state](./skills/principle-separate-before-serializing-shared-state/SKILL.md) | architecture | Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant. |
| [prove-it-works](./skills/principle-prove-it-works/SKILL.md) | verification | Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'. |
| [fix-root-causes](./skills/principle-fix-root-causes/SKILL.md) | verification | Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate. |
| [sequence-verifiable-units](./skills/principle-sequence-verifiable-units/SKILL.md) | verification | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer. |
| [test-behavior-not-implementation](./skills/principle-test-behavior-not-implementation/SKILL.md) | verification | Apply when you write, change, or keep a test. Assert what the code's users can observe, so the test fails when that behavior breaks and keeps passing when only the internals change. |
| [explain-the-number](./skills/principle-explain-the-number/SKILL.md) | verification | Apply before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think. |
| [guard-the-context-window](./skills/principle-guard-the-context-window/SKILL.md) | delegation | Route bulk to subagents; keep summaries in the main thread, not raw payloads. |
| [never-block-on-the-human](./skills/principle-never-block-on-the-human/SKILL.md) | delegation | Proceed, present the result, let the human course-correct after the fact; reserve confirmation for irreversible actions. |
| [encode-lessons-in-structure](./skills/principle-encode-lessons-in-structure/SKILL.md) | meta | Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. |

</details>

## Tools and customization

Use the tools actually available in the session. Browser verification can use a connected browser tool, an existing harness, or the project's CLI. Skill authoring uses Codex's `skill-creator` when available. Cleanup can be performed directly; this edition does not require Cursor team plugins.

To create a personal workflow, use [`$automate-me`](./skills/automate-me/SKILL.md). To capture lessons, use [`$reflect`](./skills/reflect/SKILL.md). Model preferences from [`$setup-zstack`](./skills/setup-zstack/SKILL.md) live in `.agents/zstack-models.md`. Skills read them explicitly; the file does not change Codex settings or grant access to a model.

## Automations

The dormant [Ztriage pack](./automations/ztriage/README.md) triages Slack issue reports and reproduces confirmed bugs. Point Codex at [`FOR_AGENTS.md`](./automations/ztriage/FOR_AGENTS.md) and name a target repository to set it up. Codex scheduling and connected Slack capabilities must be available; no automation or external message is enabled just by installing this collection.

## Development

```bash
python3 scripts/validate-codex.py
```

The validator needs Python 3 and PyYAML (`python3 -m pip install pyyaml` if absent). Runtime tools have their own tests under `skills/zmode/scripts/` and `skills/statechart/scripts/`. See [AGENTS.md](./AGENTS.md) for contribution guidance and [the file review](./docs/codex-file-review.tsv) for migration coverage.

## notices

Source attribution is retained in [NOTICE.md](./NOTICE.md).
