---
name: automate-me
description: "Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill via skill-creator + unslop, optionally pulling fresh evidence from recent transcripts."
---

# Automate me

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-mode` skill tailored to them (for example, `team-mode` or `delivery-mode`).

This skill orchestrates three others: an inline mining pass (see step 1), the available Codex `skill-creator` skill (authoring), and the **unslop** skill (prose discipline). It sequences them. It doesn't replace them.

## Flow

### 0. Check for an existing skill

Look recursively for `.agents/skills/**/*-mode/SKILL.md` and `~/.agents/skills/*-mode/SKILL.md` matching the user's requested workflow identifier. Mode skills can live in a personal category directory (`.agents/skills/<workflow>/`), not only at the top level. If one exists, use the stated intent; ask one short question only if it does not settle update versus replacement:

- Update the existing skill (default for repeat runs)
- Start fresh (rare, ask why before doing it)

Update mode changes the rest of the flow:
- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`).
- Step 2 asks what's changed or missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user hasn't contradicted. Revise ones with new evidence. Add new sections only for genuinely new rules.

### 1. Mine their history

Discover relevant chats with the available Codex chat tools, restricted to the active project and the user's requested window. Use current context or explicitly supplied transcript files when chat tools are unavailable; state the evidence gap. Do not guess internal storage paths or mine unrelated projects.

Survey recent agent conversations within that scope for recurring patterns. Run multiple parallel subagents across slices of history (e.g. last 2-4 weeks, split into 3 slices so each has enough material). Use the available delegation tools and inherit the parent model and reasoning effort unless the user explicitly configures an available override. Respect the active concurrency limit. Each slice mining subagent reads only the scoped chat material or source paths the parent provides, looks for the signals below, and returns a short structured list of patterns it saw with evidence pointers. Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, specialized workflows, parallelism)
- Verification posture (what "done" means, unit tests vs live repro, reviewers)
- Code and prose discipline (style, principles cited, lint/format tools)
- Process conventions (worktrees, commits, PRs, review/merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. Patterns seen in 2+ slices are high-confidence. Lone signals are weak and usually get dropped.

### 2. Ask the user directly

Mining misses intent that hasn't come up yet. Use a question tool when available and appropriate, otherwise ask concise questions in chat. Reuse preferences already stated rather than asking again.

Shape: one or two short questions with a few concrete options. Use only parameters the active question tool supports. Start broad ("Which areas matter most?"), then follow up on selected areas with specific options. After the structured rounds, one free-form chat question catches anything the options missed.

Don't dump 20 questions.

### 3. Cluster findings

Group the combined signals into sections. Common ones (use only what applies):

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking, MCP tool use.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Subagents**: default, parallelism, model-to-task, specialized workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review/merge tooling.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

The **zmode** skill shows an engineering workflow structure. Read it for granularity, without copying its contents into the new skill. Capture only conventions supported by the user's requests and evidence.

### 4. Draft the skill

Use the available Codex `skill-creator` skill to author the skill. Placement:

- Path: preserve an existing mode skill's category. For a new mode, use `.agents/skills/<workflow>/<workflow>-mode/SKILL.md` when the repo has an established personal category for that handle. Otherwise default to `.agents/skills/<workflow>-mode/SKILL.md` in the project (or `~/.agents/skills/<workflow>-mode/` if the user prefers a personal skill).
- Identifier: a user-chosen workflow or team name. Do not require a personal name.
- Frontmatter `description`: name the workflow and its intended requests, such as `$<workflow>-mode`, without implying an author persona or triggering on generic keywords like "write code" or "review PR".
- Frontmatter formatting: follow `skill-creator`'s YAML rules. Keep `description` as one YAML scalar. Quote it or use `description: >-` with indented continuation lines when punctuation or wrapping requires it.
- Preserve an existing invocation policy. For a new mode, automatic discovery is the default unless the user requests explicit-only use; put `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for that choice. Do not invent a persistent Custom Mode or guarantee that a skill stays loaded on every turn.

### 5. Iterate on prose

Apply the **unslop** skill and `skill-creator`'s writing guidelines to every line.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly. A mode skill is not a manual.

### 6. Land it

Save the skill in the requested location and validate it with the available skill-creator checks. Commit or open a PR only when the user requested that publication step; creating a personal skill does not imply publishing it.

## Guardrails

- **Don't overfit to one conversation.** A preference stated once and contradicted another time is noise. Require multiple instances before codifying it.
- **Don't be clever.** Restating other skills' contents, inventing metaphors, or writing "poetic" prose for an agent reader is cost without benefit. Keep it operational.
- **Reference, don't inline.** Other skills the user relies on should appear as path references, not pasted excerpts. Same for any principle docs they maintain elsewhere.
- **Keep sections minimal.** Only add a section if the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- **Use neutral instructions.** Address the agent directly and refer to the user by role. Do not make workflow rules depend on an author persona.
- **Don't force symmetry.** If a user has no process rules worth writing down, skip the Process section entirely.

## Evaluation

A `-mode` skill is subjective output. A `skill-creator`-style test/iterate benchmark loop isn't useful here. Review the draft with the user: does it capture their stated conventions, and is anything missing? Then save the validated result.

Run a description-optimization loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- User wants a task-specific skill (not working conventions): `skill-creator` alone, no mining required.
- User wants to capture one narrow workflow (e.g. "how I write commit messages"). That's a regular skill, not a mode skill.
