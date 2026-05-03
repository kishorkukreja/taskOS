# OAuth for Hermes MCP Server

Status: captured
Created: 2026-05-03
Owner: Kish / Hermes
Priority: high-security-before-production

## Summary

Implement Claude-compatible OAuth for the custom Hermes MCP server so Claude can connect securely over the public Tailscale Funnel URL instead of using the current unauthenticated remote MCP connector.

## Current working endpoint

Public MCP URL:

https://openclaw-server-9a85630.tail02cfc3.ts.net/mcp

Local MCP server:

http://127.0.0.1:8643/mcp

Service:

hermes-mcp.service

Source:

/root/hermes-mcp/server.py

## Next conversion step

- [ ] Convert `docs/idea.md` into `docs/spec.md`
- [ ] Convert spec into `docs/prd.md`
- [ ] Convert PRD/spec into `docs/issues.md`
- [ ] Create implementation plan for Codex/Hermes
- [ ] Implement in Codex using a branch/PR workflow

## Notes

The current connector works when Claude is configured with only the MCP URL and no advanced OAuth/auth fields. OAuth fields currently cause Claude to probe OAuth endpoints that do not exist yet.
