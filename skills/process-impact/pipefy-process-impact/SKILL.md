---
name: pipefy-process-impact
description: >
  Use this skill when the user asks whether a process change is worth it,
  wants impact / ROI / a short internal justification, or wants more than
  the Impact line that pipefy-process-design or pipefy-process-intelligence
  already emit. Quantify time returned to the team from Pipefy data already
  in context. Start a pipe diagnosis only if the user asked to measure this
  pipe, or pipefy-process-intelligence is already running (reuse round 1
  only). Do not implement from this skill; if pipefy-process-intelligence is
  already implementing, continue there.
tags: [pipefy, process-impact, impact, automation]
---

# Process impact

Read the [MCP reference](references/mcp.md) or [CLI reference](references/cli.md) for the surface you are using. Load only the relevant reference, and only in Diagnosis mode: the Impact line and the Impact case make no calls.

Quantify the impact of a process change already under discussion. **Use the context you already have. Open a diagnosis only if the user asked to measure this pipe, or `pipefy-process-intelligence` is already running (reuse round 1 only).**

This skill does not create pipes, automations, or AI agents. Point to the skill that builds the change when the user wants it built.

---

## When to use

- "Is this change worth it?" / "Does this pay off?"
- "What is the impact / ROI?" / "Help me justify this internally."
- `pipefy-process-design` or `pipefy-process-intelligence` just proposed a material change (phase, automation, AI agent, iPaaS) and the user wants more than its Impact line.

Do not use this skill for:

- Designing a new process from scratch: use `pipefy-process-design`.
- Investigating or implementing pipe improvements: use `pipefy-process-intelligence`.
- Building the recommended automation or agent: use `pipefy-building`, then the domain skill.

---

## Cost of investigation

Pick the cheapest mode that answers the question:

| Mode | When | Extra calls |
|------|------|-------------|
| **Impact line** | Default. `pipefy-process-design` and `pipefy-process-intelligence` already emit one in their output. | None |
| **Impact case** | The user asked to justify the change or to go deeper on the numbers. | None. Use the conversation context plus stated assumptions. |
| **Diagnosis** | The user asked to measure *this pipe*, or `pipefy-process-intelligence` is already running. | Reuse round 1 of `pipefy-process-intelligence`. Do not repeat that investigation here. |

`get_card`, `get_cards` and `find_cards` do **not** return `created_at` or `updated_at`. Do not derive lead time from those operations.

---

## Prerequisites

- A proposed or existing change in view (phase, automation, AI agent, iPaaS, or a new process design).
- Diagnosis only: the pipe id, and the pipe `uuid` that `get_pipe` returns, for `get_ai_agents`.

---

## Tools needed

Only in **Diagnosis** mode, and only by following round 1 of `pipefy-process-intelligence`. Do not call them for an Impact line or an Impact case.

| Operation | Read-only | Purpose |
|-----------|-----------|---------|
| `search_pipes` | Yes | Find the pipe id when only the name is known |
| `get_pipe` | Yes | Phases, `cards_count` per phase, and the pipe `uuid` |
| `get_cards` | Yes | A card sample that shows which hops look manual |
| `get_automations` | Yes | Hops that already have an automation |
| `get_ai_agents` | Yes | AI agents that already run on the pipe |

`get_ai_agents` takes the pipe **UUID**, not the numeric pipe id. Call `get_pipe` first, then `get_ai_agents repo_uuid=<pipe.uuid>`. A numeric id returns a permission error: the id type is wrong, the access is not.

Usage and credit totals, if the user already wants them in the case, are in `pipefy-observability`. Treat credit spend as the cost of capacity the process already produces, not as a line to cut.

---

## What you can measure

| Axis | Without a diagnosis | With round 1 of `pipefy-process-intelligence` | Ask the user |
|------|---------------------|-----------------------------------------------|--------------|
| Time people spend operating the pipe | Count visible manual hops (phase with no automation, human triage) | Composition: which hops look manual. A card sample is not weekly volume. `phases[].cards_count` is live WIP and bottleneck inventory, not duration | Minutes per hop; cases per week, unless a dated throughput source is already in context |
| Lead time (from card creation to done) | Do not invent a number | Not measured unless dates are already in this round's context | "How long does a case take today, end to end?" |
| Cost / capacity | Hours returned to the team | Same, with measured volume | Hourly cost is **optional**. Money only when they give it |
| Revenue | Omit | Omit unless the user confirms this process sits on the path to revenue (quotes, onboarding, billing) | Ticket, conversion, or that confirmation |

Always show the arithmetic:

```text
hours returned per week ≈ manual hops per case × minutes per hop × cases per week / 60
cost avoided per week ≈ hours returned per week × hourly cost   (only if the user gave an hourly cost)
```

If a number is missing, keep the formula and label the gap as an assumption. Do not fill it in.

---

## Value ladder

Every material recommendation has **two rungs**. The user chooses. Do not stack both as "do these now."

1. **Minimum step**: a traditional automation when the rule is clear ("if field = X, move"). Impact: hops and time returned.
2. **Next step (optional)**: an AI agent or AI automation when the hop is judgment, free text, or conversation; iPaaS when the work lives in another app. Show the extra lift (for example: the triage phase can go away and the card arrives ready in the next phase). If the extra rung does not close with evidence, say so and stop.

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
2. **Name the current hop**: what people do in the pipe today for this change (manual move, triage, copy-paste, waiting).
3. **Write the ladder**: minimum step and optional next step, each with time returned (formula). Lead time only with a cycle the user stated or dates already in context.
4. **Ask only for missing assumptions**: minutes per hop, weekly volume, hourly cost. One question, not a survey.
5. **Point to implementation**: which domain skill builds the chosen rung. Do not implement from this skill.

---

## Output format

**Impact line**, the same one-line shape `pipefy-process-design` and `pipefy-process-intelligence` put in their output:

```text
Impact: [hop that is manual today]. [Minimum step] returns ~[N] hours/week (assumption: [missing number]). [Next step and its extra lift, or "next step does not close"].
```

**Impact case:**

```text
## Process impact: [pipe or proposed change]

Current: [what people do in the pipe today]
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
- No invented lead time.
- No pipe deletion unless the user asked to delete that pipe.
- Report **time returned to the team** on repetitive hops. Do not frame impact as fewer people on the process.
- Rung 2 is omitted or marked "does not close" when the evidence is weak.

## Failure modes

| Symptom | Likely cause | Recovery |
|---------|--------------|----------|
| User wants a money ROI | No hourly cost in context | Ask for it; otherwise stop at hours returned |
| User wants lead time | Card reads have no timestamps | Ask for today's cycle; omit the number if they do not give one |
| Permission error listing AI agents | Numeric pipe id passed to `get_ai_agents` | Read `uuid` from `get_pipe` and pass it as `repo_uuid` |
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
- `pipefy-reports`: exports when the user asked for a deeper volume picture.
