# Implementation notes: Phase 1 async jobs

Date: 2026-05-03
Status: implemented-and-live

## Files changed

- `/root/hermes-mcp/server.py`
- `/root/hermes-mcp/test_jobs.py`

A timestamped backup of the original server was created under `/root/hermes-mcp/server.py.bak.*` before editing.

## Implemented

- Added durable SQLite job store at `/root/hermes-mcp/jobs.sqlite`.
- Added `DEFAULT_JOB_TIMEOUT`, defaulting to 900 seconds via `HERMES_MCP_JOB_TIMEOUT` override.
- Added job lifecycle helpers:
  - `_init_jobs_db`
  - `_create_job`
  - `_get_job`
  - `_mark_job_started`
  - `_mark_job_succeeded`
  - `_mark_job_failed`
  - `_mark_stale_jobs_interrupted`
  - `_format_job_status`
  - `_run_hermes_job`
- Added MCP tools:
  - `hermes_submit`
  - `hermes_job_status`
  - `hermes_job_result`
- Kept existing tools:
  - `hermes_ask`
  - `hermes_run_skill`
  - `hermes_health`
- Updated MCP server instructions so Claude should use `hermes_submit` for long workflows and reserve `hermes_ask` for short sync calls.
- Updated `_call_hermes` to support per-call timeout.

## Verification

Commands run from `/root/hermes-mcp`:

```bash
python3 -m unittest test_jobs.py -v
python3 -m py_compile server.py test_jobs.py
python3 - <<'PY'
import importlib.util, json
spec = importlib.util.spec_from_file_location('server', '/root/hermes-mcp/server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)
print(json.dumps({
  'has_submit': hasattr(server, 'hermes_submit'),
  'has_status': hasattr(server, 'hermes_job_status'),
  'has_result': hasattr(server, 'hermes_job_result'),
  'jobs_db_path': server.JOBS_DB_PATH,
  'default_job_timeout': server.DEFAULT_JOB_TIMEOUT,
}, indent=2))
PY
```

Results:

- Unit tests: 6 passed.
- Python compile: passed.
- Import/feature check: `hermes_submit`, `hermes_job_status`, and `hermes_job_result` present.

## Deployment verification

`systemctl restart hermes-mcp` was approved and completed on 2026-05-03.

Live service after restart:

- Service: `hermes-mcp.service`
- Main PID after restart: `685556`
- Active timestamp: `Sun 2026-05-03 17:57:53 UTC`
- Local health: `http://127.0.0.1:8643/health` returned `200 OK`
- Local MCP health: `http://127.0.0.1:8643/mcp/health` returned `200 OK`

Live MCP tool discovery now returns all six tools locally and via the public Funnel URL:

- `hermes_ask`
- `hermes_run_skill`
- `hermes_submit`
- `hermes_job_status`
- `hermes_job_result`
- `hermes_health`

Async smoke test:

- Submitted job: `hjob_20260503_175828_d2325f52`
- Tool: `hermes_submit`
- Followed with `hermes_job_status` polling.
- Final status: `succeeded`
- `hermes_job_result` returned: `MCP_ASYNC_SMOKE_OK`

## Remaining follow-ups

- Consider adding `hermes_job_cancel`.
- Consider retention cleanup for old rows in `/root/hermes-mcp/jobs.sqlite`.
- Consider Phase 2 deterministic fast-path tools: `selfos_raw_capture`, `taskos_capture`, and `wiki_research_request`.
