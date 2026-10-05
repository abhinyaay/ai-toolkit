# MCP reference

Only Diagnosis mode makes calls, and it follows round 1 of `pipefy-process-intelligence`. Its MCP reference has the full invocation list.

## Invocation examples

```text
get_pipe pipe_id=<id>
```

Keep both `pipe.id` and `pipe.uuid` from the response.

```text
get_ai_agents repo_uuid=<pipe.uuid>
```

```text
get_cards pipe_id=<id> first=50 include_fields=true
```

The page size is a composition sample, not weekly volume.

```text
get_automations pipe_id=<id>
```

The listing is complete only when `pagination.has_more` is false.
