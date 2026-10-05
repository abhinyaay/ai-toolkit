# CLI reference

Only Diagnosis mode makes calls, and it follows round 1 of `pipefy-process-intelligence`.

| Operation | Command |
|-----------|---------|
| `search_pipes` | `pipefy pipe list --name <text>` |
| `get_pipe` | `pipefy pipe get <PIPE_ID>` |
| `get_cards` | `pipefy card list --pipe <PIPE_ID> --include-fields` |
| `get_automations` | `pipefy automation list --pipe <PIPE_ID>` |
| `get_ai_agents` | `pipefy agent list --repo <PIPE_UUID>` |

`--repo` takes the pipe UUID that `pipefy pipe get` returns, not the numeric pipe id.
