---
name: pipefy-process-impact
description: >
  Use this skill when the user asks whether a process change is worth it,
  wants its ROI or the time it returns to the team, a short internal
  justification, or more than the Impact line that pipefy-process-design or
  pipefy-process-intelligence already emit. Quantify time returned from
  context in the conversation; when the user names a pipe, first check
  (read-only) what already covers the hop. Start a pipe diagnosis only if
  the user asked to measure this pipe, or pipefy-process-intelligence is
  already running (reuse round 1 only). Do not implement from this skill;
  if pipefy-process-intelligence is already implementing, continue there.
  Not for what a configuration change breaks elsewhere in a pipe.
tags: [pipefy, process-impact, impact, automation]
---

# Process impact

Read the [MCP reference](references/mcp.md) or [CLI reference](references/cli.md) for the surface you are using. Load only the relevant reference, and only when the mode makes calls: the coverage check in an Impact case, a pipe report export, or a Diagnosis. The Impact line makes no calls.

Quantify the impact of a process change already under discussion. **Use the context you already have. When the user names a pipe, check what already covers the hop before you size it. Open a diagnosis only if the user asked to measure this pipe, or `pipefy-process-intelligence` is already running (reuse round 1 only).**

This skill does not create pipes, automations, or AI agents. Point to the skill that builds the change when the user wants it built.

---

## When to use

- "Is this change worth it?" / "Does this pay off?"
- "What is the ROI?" / "How much time does this give back?" / "Help me justify this internally."
- `pipefy-process-design` or `pipefy-process-intelligence` just proposed a material change (phase, automation, AI agent, iPaaS) and the user wants more than its Impact line.

Do not use this skill for:

- Designing a new process from scratch: use `pipefy-process-design`.
- Investigating or implementing pipe improvements: use `pipefy-process-intelligence`.
- Building the recommended automation or agent: use `pipefy-building`, then the domain skill.
- Finding what a field, phase, or automation change would break elsewhere: that is a dependency question, not process impact.

---

## Cost of investigation

Pick the cheapest mode that answers the question:

| Mode | When | Extra calls |
|------|------|-------------|
| **Impact line** | Default. `pipefy-process-design` and `pipefy-process-intelligence` already emit one in their output. | None |
| **Impact case** | The user asked to justify the change or to go deeper on the numbers. | A coverage check when the user names a pipe: `search_pipes` if only the name is known, then `get_pipe`, `get_automations`, `get_ai_agents`, and `get_ai_agent` for each active agent. No card sample. A pipe report export only under the rule below. |
| **Diagnosis** | The user asked to measure *this pipe*, or `pipefy-process-intelligence` is already running. | Reuse round 1 of `pipefy-process-intelligence`, then read the behaviors of each active agent with `get_ai_agent` (round 1 lists agents but does not read them). Do not repeat the rest of that investigation here. |

`get_card`, `get_cards` and `find_cards` return no creation, update, or phase timestamps (custom date fields can still come back in `fields`). Do not derive lead time or weekly volume from them.

A pipe report export carries those dates. Run it when the user asked you to measure lead time or weekly volume; otherwise offer it and run it once they agree. The export works on an existing pipe report (`get_pipe_reports` lists them); if the pipe has none, creating one with `create_pipe_report` is a write to the user's pipe, so ask first. Pass the date columns by `name` in `columns`, taken from `get_pipe_report_columns`: `created_at`, `finished_at`, `updated_at`, and per phase `start_at_phase_<n>`, `end_at_phase_<n>` and `duration_in_phase_<n>`, where `<n>` is a report index, not the phase id. The file headers show labels such as "Total time in <phase> (days)". `pipefy-reports` has the export and polling steps.

---

## Prerequisites

- A proposed or existing change in view (phase, automation, AI agent, iPaaS, or a new process design).
- Coverage check or Diagnosis: the pipe id, and the pipe `uuid` that `get_pipe` returns, for `get_ai_agents` and the report reads.

---

## Tools needed

In an **Impact case**, only the coverage check and, under the rule above, the export. In **Diagnosis** mode, round 1 of `pipefy-process-intelligence` plus `get_ai_agent`. An Impact line makes no calls.

| Operation | Read-only | Purpose |
|-----------|-----------|---------|
| `search_pipes` | Yes | Find the pipe id when only the name is known |
| `get_pipe` | Yes | Phases, `cards_count` per phase, and the pipe `uuid` |
| `get_cards` | Yes | A card sample that shows which hops look manual (Diagnosis only) |
| `get_automations` | Yes | Hops that already have an automation |
| `get_ai_agents` | Yes | AI agents on the pipe, active or disabled |
| `get_ai_agent` | Yes | Behaviors of an active agent: which phases it acts on and what it does there |
| `get_pipe_reports` | Yes | Existing pipe reports to export |
| `get_pipe_report_columns` | Yes | Column `name` values for the export |
| `export_pipe_report` | No | Start an export job; changes no card or report |
| `get_pipe_report_export` | Yes | Poll the export until the file is ready |
| `create_pipe_report` | No | Only when the pipe has no report and the user agreed |

`get_ai_agents` takes the pipe **UUID**, not the numeric pipe id. Call `get_pipe` first, then `get_ai_agents repo_uuid=<pipe.uuid>`. A numeric id returns a permission error: the id type is wrong, the access is not.

An agent is active when `disabledAt` is null; count only behaviors with `active: true`. A behavior acts on the phase in its event params (`to_phase_id`, `inPhaseId`, `fromPhaseId`; a `card_created` behavior acts at intake), and it moves the card itself when it has a `move_card` action (`destinationPhaseId`). An automation covers a hop only when it is `active` and its action is enabled (`actionEnabled`).

Usage and credit totals, if the user already wants them in the case, are in `pipefy-observability`. Treat credit spend as the cost of capacity the process already produces, not as a line to cut.

---

## What you can measure

| Axis | Without a diagnosis | With round 1 of `pipefy-process-intelligence` | Ask the user |
|------|---------------------|-----------------------------------------------|--------------|
| Time people spend operating the pipe | Count visible manual hops (phase with no automation or agent coverage, human triage) | Composition: which hops look manual. A card sample is not weekly volume. `phases[].cards_count` is live WIP and bottleneck inventory, not duration. Its sum also counts cards in done phases, which `get_pipe` does not flag, and leaves out the start form, so it is not the number of open cases | Minutes per hop; cases per week, unless a dated source is in context (a pipe report export: cards per week by `created_at`) |
| Lead time (from card creation to done) | Do not invent a number | Not measured unless a pipe report export ran or dates are already in context | "How long does a case take today, end to end?", or offer a pipe report export (`finished_at` minus `created_at` on cards that finished) |
| Cost / capacity | Hours returned to the team | Same, with measured volume | Hourly cost is **optional**. Money only when they give it |
| Revenue | Omit unless the user confirms this process sits on the path to revenue (quotes, onboarding, billing) | Same | Ticket, conversion, or that confirmation |

Always show the arithmetic, per rung:

```text
hours returned per week ≈ hops this step removes per case × minutes per hop × cases per week / 60
cost avoided per week ≈ hours returned per week × hourly cost   (only if the user gave an hourly cost)
```

If a number is missing, keep the formula with the gap named. Do not fill it in.

---

## Value ladder

Every material recommendation has **two rungs**. The user chooses. Do not stack both as "do these now."

1. **Minimum step**: a traditional automation when the rule is clear ("if field = X, move"). Impact: the hops it removes and the time they return.
2. **Next step (optional)**: an AI agent or AI automation when the hop is judgment, free text, or conversation; iPaaS when the work lives in another app. Show the extra lift from the hops only this rung removes (for example: the triage phase can go away and the card arrives ready in the next phase). If the extra rung does not close with evidence, say so and stop.

Do not recommend a capability the evidence does not support.

---

## Structural change vs leaving the process

| User ask | Read it as | Response |
|----------|------------|----------|
| Fewer **phases** | A cleaner flow | Yes, when the work stays in the pipe. Prefer replacing the hop with an automation or AI agent. |
| Fewer **pipes** / a quiet pipe | Architecture, or a process that never launched | Do not delete. Ask: missing trigger (form, portal, create-card automation)? Duplicate of a live pipe? Should it be a relation or a database table? Reactivate or connect it, and cover remaining manual hops with automations or AI agents when that fits. Delete a pipe **only** when the user asks in so many words, and then absorb the work into the pipe that remains, not a spreadsheet. |
| Less **platform** (cut credits, seats, "go back to Excel") | Out of scope | This skill measures process impact. Do not recommend moving work off Pipefy. |

---

## Steps

1. **Choose the mode**: Impact line, Impact case, or Diagnosis (table above). For a diagnosis, reuse round 1 of `pipefy-process-intelligence` only; do not start round 2+ from this skill. If the user asked to analyze **and** improve, `pipefy-process-intelligence` owns implementation after they approve a round.
2. **Name the current hop**: what people do in the pipe today for this change (manual move, triage, copy-paste, waiting). Before you call a hop manual, check what already covers it: an active automation, or an active AI agent whose behaviors act on that phase. If something covers it, say so; the question becomes whether that coverage pays off, not whether to add a second one.
3. **Write the ladder**: minimum step and optional next step, each with the time returned by the hops it removes (formula). Lead time only with a cycle the user stated or dates from a pipe report export.
4. **Ask only for missing assumptions**: minutes per hop, weekly volume, hourly cost. Ask for all of them in one question, not a survey.
5. **Point to implementation**: which domain skill builds the chosen rung. Do not implement from this skill.

---

## Output format

**Impact line** (default mode):

```text
Impact: [hop that is manual today]. [Minimum step] returns [hours/week, or the formula with the missing numbers named]. [Next step and its extra lift, or "next step does not close"].
```

**Impact case:**

```text
## Process impact: [pipe or proposed change]

Current: [what people do in the pipe today, and what already covers it]
Minimum step: [automation], time returned: [formula]
Next step (optional): [AI agent / iPaaS], extra lift: [why, or "does not close"]
Lead time: [number + source] or [not measured; give today's end-to-end cycle]
Assumptions: [minutes per hop, volume, hourly cost if any]
If you want this built: [domain skill]
```

Add a revenue line only when the user confirmed the process sits on the path to revenue.

---

## Success criteria

- Assumptions are explicit. No currency figure without an hourly cost.
- No invented lead time or weekly volume.
- No step proposed for a hop that an active automation or agent already covers, unless the case says so and sizes the coverage instead.
- No pipe deletion unless the user asked to delete that pipe.
- Report **time returned to the team** on repetitive hops. Do not frame impact as fewer people on the process.
- Rung 2 is omitted or marked "does not close" when the evidence is weak.

## Failure modes

| Symptom | Likely cause | Recovery |
|---------|--------------|----------|
| User wants a money ROI | No hourly cost in context | Ask for it; otherwise stop at hours returned |
| User wants lead time | Card reads have no timestamps | Ask for today's cycle, or offer a pipe report export; omit the number if neither is available |
| Export has no date columns | `columns` not passed, or labels passed instead of names | Pass the `name` values from `get_pipe_report_columns` |
| Pipe has no report to export | The export needs an existing report | Ask before `create_pipe_report`; otherwise ask the user for the cycle |
| Permission error listing AI agents | Numeric pipe id passed to `get_ai_agents` | Read `uuid` from `get_pipe` and pass it as `repo_uuid` |
| Permission error with the pipe `uuid` too | The identity cannot read that pipe's agents | Treat AI agent coverage as unknown, say so, and do not call the hop manual on that basis |
| Proposed step duplicates what runs today | An active agent or automation already acts on the hop | Read the agent's behaviors with `get_ai_agent`; size the existing coverage instead of adding a second one |
| Quiet / unused pipe | Process never launched | Reactivate or connect; cover hops with automations or AI agents if they fit. Do not delete unless asked |
| User asks to cut credits or leave Pipefy | Out of scope | Stay on process impact; do not recommend moving work off the pipe |

## See also

- `pipefy-process-design`: new process architecture (emits an Impact line).
- `pipefy-process-intelligence`: diagnose (round 1); reuse it for Diagnosis mode. Round 2+ implementation stays there when the user asked to improve.
- `pipefy-building`: route implementation to a domain skill.
- `pipefy-automations`: minimum-step automations.
- `pipefy-ai-agents`: next-step AI agents.
- `pipefy-ipaas`: next step when the work lives in another app.
- `pipefy-observability`: usage and credits already in the process.
- `pipefy-reports`: pipe report exports for lead time and weekly volume.
