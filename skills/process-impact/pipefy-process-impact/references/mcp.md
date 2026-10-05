# MCP reference

The skill runs the coverage check when the user names a pipe and, when they asked to measure, a pipe report export. Nothing else.

## Coverage check

```text
get_pipe pipe_id=<id>
```

Keep both `pipe.id` and `pipe.uuid` from the response.

```text
get_automations pipe_id=<id>
```

The listing is complete only when `pagination.has_more` is false; pass `after=<pagination.end_cursor>` for the next page.

```text
get_ai_agents repo_uuid=<pipe.uuid>
```

For each active agent, read its behaviors:

```text
get_ai_agent uuid=<agent.uuid>
```

## Pipe report export

```text
get_pipe_reports pipe_uuid=<pipe.uuid>
```

```text
get_pipe_report_columns pipe_uuid=<pipe.uuid>
```

```text
export_pipe_report pipe_id=<id> pipe_report_id=<report.id> columns=["title", "current_phase", "created_at", "finished_at", "duration_in_phase_<n>"]
```

```text
get_pipe_report_export export_id=<export.id>
```

Poll until the state is `done`; the response then has `fileURL` (an XLSX file). The report reads take the pipe `uuid`; the export takes the numeric pipe id.
