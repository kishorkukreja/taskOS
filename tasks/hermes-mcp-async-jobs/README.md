# Hermes MCP Async Jobs

Status: captured
Created: 2026-05-03
Owner: Kish / Hermes
Priority: high-reliability

## Summary

Enhance the custom Hermes MCP server so Claude can trigger long Hermes workflows without timing out. Replace the current synchronous-only `hermes_ask` / `hermes_run_skill` pattern with async job submission and polling: Claude submits a task, receives a `job_id` immediately, then polls status/result while Hermes runs in the background.

## Current working endpoint

Public MCP URL:

https://openclaw-server-9a85630.tail02cfc3.ts.net/mcp

Local MCP server:

http://127.0.0.1:8643/mcp

Service:

hermes-mcp.service

Source:

/root/hermes-mcp/server.py

## Phase 1 target

Implement generic async wrapper around the existing Hermes API call:

- `hermes_submit` — submit long-running Hermes command and return a job ID quickly.
- `hermes_job_status` — poll queued/running/succeeded/failed/timed_out/interrupted state.
- `hermes_job_result` — fetch final Hermes response when complete.
- Optional later: `hermes_job_cancel`.

## Next conversion step

- [ ] Convert `docs/idea.md` into `docs/spec.md`
- [ ] Convert spec into `docs/prd.md`
- [ ] Convert PRD/spec into `docs/issues.md`
- [ ] Create implementation plan for Codex/Hermes
- [ ] Add direct fast-path Self-OS/taskOS tools after Phase 1 is stable
