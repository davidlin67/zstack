---
name: zmode-help
description: Guides users through zstack setup, $zmode, and picking the skill, playbook, or principle for a task. Type $zmode-help with a question.
---

# zmode help

zstack is Zwift's Codex workflow collection. Its engineering workflow is **zmode**.

Answer the user's question about zstack, give a prompt they can send, and link the local file that supports the answer. Read the routed file before explaining it. Prefer the installed Codex-native source over upstream documentation, whose tool instructions may differ.

For a help question, explain without starting the task. A message such as "use zstack to fix this bug" asks for action: read [`zmode`](../zmode/SKILL.md) and do the work. If the need is unclear, ask one concise question covering setup, starting a task, choosing a skill, fixing a run, or customization.

## Get set up

Follow the checkout's [README](../../README.md) and [setup guide](../../docs/guide/01-setup.md). Codex discovers repository skills under `.agents/skills/`; this collection's installer also supports a user-level destination. Do not run another harness's marketplace commands.

Invoke a skill as `$skill-name`, such as `$zmode`. The optional `$setup-zstack` writes project-local `.agents/zstack-models.md` preferences. Missing preferences mean delegates inherit the parent model and effort. The file is read by zstack; it is not native Codex model configuration or an always-applied rule. An override works only when explicitly chosen and accepted by the active tool and instructions.

Existing explicit-only skills retain that policy in `agents/openai.yaml`. They can still be followed when the user requests them or a selected workflow composes them. Follow a skill by reading its instructions and performing its steps; do not invent a skill-execution API.

For cost questions, explain that independent candidates, reviewers, and reruns consume extra tokens. Fewer candidate or reviewer entries reduce fan-out. Model and reasoning options depend on the active Codex session, so inspect the available tools instead of advertising a fixed model catalog.

## Start a task

`$zmode` chooses a playbook, tracks its steps, and uses other skills when relevant. A good prompt states the goal, constraints, and an executable check for done. Read [`references/prompting.md`](references/prompting.md) before rewriting a prompt.

Codex does not require Cursor's Custom Mode shortcut or `/loop`. Start a new task with `$zmode` and let the current run work to the stated finish condition within its tools and permissions. A skill file alone does not schedule future wakeups or ensure it remains in context forever. A recurring future task uses an available Codex Automations tool only when the user asks for scheduling. Following a running job to completion stays in the current task.

Subagent brief files such as [`zmode-agent`](../../agents/zmode-agent.md) are ordinary Markdown. Supply their resolved paths in a Codex delegation brief when needed; do not treat the filename as a registered `subagent_type`. Delegates may share the filesystem, so give writers isolated worktrees or disjoint paths and respect the active concurrency limit. If a required tool is unavailable, report the gap and use a concrete supported fallback.

## Pick a skill

Use `$zmode` for a task that needs its engineering workflow. Invoke a narrower skill when the user asks for a narrower outcome. Read the target skill and provide one adapted example.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`$zmode`](../zmode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`$in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`$sharpen`](../sharpen/SKILL.md) |
| Learn the expert words for what they're building, including words borrowed from neighboring fields, with every cited source checked, and get their description rewritten with them | [`$reframe`](../reframe/SKILL.md) |
| Know how code works now, or where new code should live | [`$how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`$why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`$teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`$recall`](../recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`$ketchup`](../ketchup/SKILL.md) |
| Catch up like `$ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`$ketchup-video`](../ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`$blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`$architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`$arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, with independent Codex subagents | [`$swarm`](../swarm/SKILL.md) |
| Have independent reviewers review a diff and try to break it | [`$interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`$tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`$typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`$no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`$unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`$technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`$bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`$create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`$maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`$create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`$maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`$statechart`](../statechart/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`$benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`$figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`$show-me-your-work`](../show-me-your-work/SKILL.md) |
| Configure supported delegation preferences | [`$setup-zstack`](../setup-zstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`$automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`$reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`$correct`](../correct/SKILL.md) |
| Build a page whose buttons call a supported bot webhook | [`$make-bot-ui`](../make-bot-ui/SKILL.md) |
| Find their way around zstack | `$zmode-help` |


If a neighboring skill is missing from the table, route by its frontmatter description. The `principle-*` skills hold individual engineering rules; `$zmode` reads the relevant ones. [Guide page 8](../../docs/guide/08-principles.md) lists them.

Close calls:

- `$how` explains current mechanics. `$why` reconstructs decisions from the record. `$teach` combines them for learning.
- `$arena` compares attempts at one brief and synthesizes an artifact. `$swarm` covers slices or races and returns one report.
- `$interrogate` tries to break the named diff. `$blast-radius` proves the facts that keep downstream behavior safe.
- `$recall` rebuilds context across scoped prior chats. `$ketchup` covers changes in this chat since the user's last message. Picking up one branch uses the Session pickup playbook.

## Playbooks

Playbooks are files inside `$zmode`, not separate skill commands. Describe the task or name the playbook:

- "babysit this PR" drives it to merge-ready. It merges only if the user asks to land or merge.
- "land the stack" uses Shipping.
- "take over this branch" uses Session pickup.
- "pause safely" uses Pause safely.
- "full autopilot on this queue" uses Autopilot-full. "autopilot, don't merge" uses Autopilot-stack.
- "run the eval playbook" uses Eval.
- "plan this migration" uses Multi-phase plan and delivers a plan.

Use `$architect` or the Prototype playbook to settle an uncertain design. Follow the active Codex collaboration mode; a skill cannot switch it by claiming Plan Mode is active.

## Fix a run

| Symptom | Response |
|---|---|
| The workflow drifted out of context | Restate the goal and invoke `$zmode` for the current task. |
| A follow-up was mistaken for the old task | Say "new task" and name its goal. |
| A model preference had no effect | Confirm the file was read and the active tool permits the requested override. The file cannot change the parent chat model. |
| A skill was not selected automatically | Check its name, discovery location, description, and `agents/openai.yaml` policy. Explicit-only invocation may be intentional. |
| Parallel writers overwrote each other | Use separate worktrees or disjoint writable paths. Local delegates share files. |
| An unattended run moved but finished nothing | Give it a check that can pass or fail and a concrete stop condition. Do not assume a future automatic wakeup. |
| A reply claimed success from a build | Ask for the real user flow, command output, stored value, or measured profile. |

Use `$create-verification-skill` when app behavior needs a reproducible driver. Use `$create-formal-verification-skill` for a race or invariant beyond what tests cover. Existing verification skills have matching maintenance skills.

## Customize

`$automate-me` drafts personal working conventions from scoped history and stated preferences. `$reflect` proposes durable improvements from this run. `$correct` fixes recurring mistakes through architecture, types, checks, and only then prose. Skill authoring uses the available `skill-creator` skill; Codex does not provide a universal `/create-skill` command.

## Reply

Lead with the answer. Give at most one adapted example prompt from [`references/recipes.md`](references/recipes.md), then link the source file. Keep it short unless the user asks for the whole map.
