# Idea: Hermes MCP async jobs

## Problem

Claude sometimes calls Hermes through the custom MCP server and times out before Hermes finishes. Hermes is slow by design for high-integrity workflows: it loads skills, extracts web content, reads schemas, writes files, commits/pushes, verifies results, and only then returns. That is fine for Hermes, but brittle for Claude's MCP/tool-call timeout window.

Current flow:

```text
Claude → hermes_ask MCP tool → /v1/chat/completions → Hermes performs all steps → MCP returns final response
```

Current implementation in `/root/hermes-mcp/server.py`:

- `hermes_ask` calls `_call_hermes(params.message)` synchronously.
- `hermes_run_skill` builds a message and also calls `_call_hermes(...)` synchronously.
- `_call_hermes` posts to `http://127.0.0.1:8642/v1/chat/completions` with `REQUEST_TIMEOUT = 120`.
- If Hermes exceeds that time, MCP returns a timeout error; Claude may also time out before the MCP server does.

## Desired outcome

Claude should not need to keep a single MCP tool call open while Hermes completes long workflows. The MCP server should support job semantics:

```text
Claude calls hermes_submit(...)
→ MCP returns job_id immediately
→ background worker calls Hermes API
→ Claude polls hermes_job_status(job_id)
→ Claude fetches hermes_job_result(job_id)
```

## Phase 1 scope

Implement a generic async job wrapper while preserving the existing Hermes behavior.

### New tools

#### `hermes_submit`

Input:

- `message: str`
- optional `system: str`
- optional `timeout_seconds: int`

Behavior:

- Create durable job record.
- Return quickly with `job_id` and `status=queued` or `running`.
- Start background task that calls `_call_hermes` or lower-level Hermes API call.

#### `hermes_job_status`

Input:

- `job_id: str`

Returns:

- `job_id`
- `status`: `queued | running | succeeded | failed | timed_out | interrupted | cancelled`
- timestamps: `created_at`, `started_at`, `finished_at`
- `elapsed_seconds`
- error summary if failed

#### `hermes_job_result`

Input:

- `job_id: str`

Returns:

- final Hermes response if complete
- otherwise a short message asking Claude to poll again

#### Later optional: `hermes_job_cancel`

Cancel in-flight job if possible.

## Persistent storage

Use SQLite so jobs survive MCP process restarts:

```text
/root/hermes-mcp/jobs.sqlite
```

Suggested table:

```sql
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY,
  message TEXT NOT NULL,
  system TEXT,
  status TEXT NOT NULL,
  result TEXT,
  error TEXT,
  created_at TEXT NOT NULL,
  started_at TEXT,
  finished_at TEXT,
  timeout_seconds INTEGER NOT NULL
);
```

On service startup, mark stale `running`/`queued` jobs as `interrupted`, unless a later worker-recovery mechanism is added.

## Tool description / Claude guidance

Update MCP server instructions so Claude chooses async for long tasks:

> Use `hermes_submit` for any command involving web extraction, git operations, wiki writes, research, compile/lint, or multiple-step workflows. Use `hermes_ask` only for short synchronous questions. After `hermes_submit`, poll `hermes_job_status` and then `hermes_job_result`.

## Constraints

- Keep existing `hermes_ask`, `hermes_run_skill`, and `hermes_health` for backward compatibility.
- Avoid exposing secrets in job errors.
- Avoid holding HTTP/MCP request open during long Hermes work.
- Do not require changes to Hermes API server for Phase 1.
- Jobs should be limited enough to avoid unlimited disk growth; later add retention cleanup.

## Acceptance criteria

- Calling `hermes_submit` returns a `job_id` in under a few seconds.
- A background job executes a real Hermes command and records the final response.
- `hermes_job_status` reports status accurately while a job is running and after completion.
- `hermes_job_result` returns the final output once complete, and a helpful still-running message before completion.
- Existing `hermes_ask`, `hermes_run_skill`, and `hermes_health` continue to work.
- `hermes-mcp.service` restarts cleanly after changes.
- Local MCP initialize/list-tools/call smoke tests pass.
- Health endpoint remains OK at `/health` and `/mcp/health`.

## Future Phase 2

Add direct fast-path tools for common workflows to reduce latency and LLM overhead:

- `selfos_raw_capture`
- `taskos_capture`
- `wiki_research_request`

These should write deterministic markdown, run git pull/commit/push, and return commit hashes without invoking the full Hermes agent loop unless interpretation is required.

## Future Phase 3

Add richer job observability:

- progress log lines
- current phase
- Hermes session ID, if available
- commit hash / PR URL extraction
- job cancellation
- retention cleanup
