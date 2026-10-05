# CLI reference

The skill runs the coverage check (`get_pipe`, `get_automations`, `get_ai_agents`, `get_ai_agent`) when the user names a pipe and, when they asked to measure, a pipe report export. Nothing else.

| Operation | Command |
|-----------|---------|
| `search_pipes` | `pipefy pipe list --name <text>` |
| `get_pipe` | `pipefy pipe get <PIPE_ID> --json` |
| `get_automations` | `pipefy automation list --pipe <PIPE_ID> --json` |
| `get_ai_agents` | `pipefy agent list --repo <PIPE_UUID> --json` |
| `get_ai_agent` | `pipefy agent get <AGENT_UUID> --json` |
| `get_pipe_reports` | `pipefy report-pipe list --pipe <PIPE_UUID> --json` |
| `get_pipe_report_columns` | `pipefy report-pipe columns --pipe <PIPE_UUID> --json` |
| `export_pipe_report` | `pipefy report-pipe export --pipe <PIPE_ID> --report-id <REPORT_ID> --columns '<JSON array of column names>' --format csv > report.xlsx` |

`--repo` takes the pipe UUID that `pipefy pipe get` returns, not the numeric pipe id. The report `list` and `columns` commands also take the pipe UUID; `export` takes the numeric pipe id.

`pipefy automation list` without `--json` prints a table that leaves out `event_params` (the phase a rule acts on). The listing returns one page of up to 50 rules; while `pageInfo.hasNextPage` is true, run it again with `--after <pageInfo.endCursor>`.

`--format csv` waits for the export and writes the file's bytes to stdout. For a pipe report the file is XLSX, whatever the flag name, so redirect it to a `.xlsx` path.
