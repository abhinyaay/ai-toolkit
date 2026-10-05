# MCP reference

Diagnosis mode follows round 1 of `pipefy-process-intelligence`, whose MCP reference has the full invocation list. An Impact case only runs the coverage check: `get_pipe`, `get_automations`, `get_ai_agents`, `get_ai_agent`.

## Invocation examples

```text
get_pipe pipe_id=<id>
```

Keep both `pipe.id` and `pipe.uuid` from the response.

```text
get_ai_agents repo_uuid=<pipe.uuid>
```

For each active agent, read its behaviors:

```text
get_ai_agent uuid=<agent.uuid>
```

```text
get_cards pipe_id=<id> first=50 include_fields=true
```

The page size is a composition sample, not weekly volume.

```text
get_automations pipe_id=<id>
```

The listing is complete only when `pagination.has_more` is false.
