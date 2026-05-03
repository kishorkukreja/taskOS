# OAuth for Hermes MCP Server — Idea Capture

Created: 2026-05-03
Status: captured
Repository: /data/taskOS
Task folder: /data/taskOS/tasks/oauth-mcp-server

## What we are trying to do

Implement OAuth for the custom Hermes MCP server used by Claude remote MCP/custom connectors.

The goal is to secure the currently public MCP endpoint so Claude can authenticate properly instead of leaving the MCP server unauthenticated through Tailscale Funnel.

Current public endpoint:

https://openclaw-server-9a85630.tail02cfc3.ts.net/mcp

Current local endpoint:

http://127.0.0.1:8643/mcp

Current service:

hermes-mcp.service

Current source file:

/root/hermes-mcp/server.py

## Why it matters

The current unauthenticated connector works for testing, but it is not safe as the final shape.

Because the Tailscale Funnel URL is publicly reachable, anyone who discovers the URL could potentially call the MCP tools. Those tools can route requests into Hermes, and Hermes has broad operational capability.

We want the final setup to preserve the convenience of Claude remote MCP while adding a real authorization boundary.

## Current state

The MCP server is a custom FastMCP bridge exposing Hermes Agent to Claude.

It exposes tools including:

- `hermes_ask`
- `hermes_run_skill`
- `hermes_health`

Current useful public health probe routes also exist:

- `GET /health`
- `GET /mcp/health`

Both return backend status JSON for connector probes.

`hermes_ask.message` has been raised to a 10,000 character max so Claude can send multiline wiki captures and task requests.

Current Claude connector works when added as an unauthenticated custom connector using only:

https://openclaw-server-9a85630.tail02cfc3.ts.net/mcp

and leaving advanced OAuth/auth/API-key fields blank.

## Observed problem

When Claude is configured with advanced auth/OAuth/API-key fields, it tries to perform an OAuth flow.

Observed failing probes in service logs included:

- `GET /.well-known/oauth-protected-resource` -> 404
- `GET /.well-known/oauth-authorization-server` -> 404
- `GET /authorize?...` -> 404
- `POST /identity/connect/token` -> 404

This proves the server is reachable, but it does not implement the OAuth endpoints Claude expects.

`MCP_API_KEY` exists in service/config, but it is not a Claude-compatible authentication solution by itself. It is not sufficient unless the server/proxy actually enforces it and advertises a compatible auth flow.

## Desired outcome

Claude should be able to add/connect to the same MCP URL:

https://openclaw-server-9a85630.tail02cfc3.ts.net/mcp

and complete an OAuth-based authentication flow.

After successful auth:

- Claude can discover tools.
- Claude can call `hermes_health`.
- Claude can call `hermes_ask`.
- Claude can ask Hermes to save/add things to Self-OS/wiki/taskOS.
- Unauthenticated requests to `/mcp` are rejected.
- Plain public health endpoints remain available for harmless status checks.

## Recommended architecture

Use a small OAuth/auth proxy in front of the existing MCP server rather than rewriting the working FastMCP server.

Proposed flow:

```text
Claude
  -> Tailscale Funnel public URL
  -> OAuth/Auth proxy on 127.0.0.1:8644
      - /.well-known/oauth-protected-resource
      - /.well-known/oauth-authorization-server
      - /oauth/register
      - /authorize
      - /oauth/token
      - protected /mcp proxy
      - public /health and /mcp/health
  -> existing FastMCP server on 127.0.0.1:8643
  -> Hermes backend API on 127.0.0.1:8642
```

Then update Tailscale Funnel to proxy to the OAuth proxy rather than directly to FastMCP.

This keeps the existing working MCP implementation intact.

## OAuth endpoints likely required

### Protected resource metadata

Endpoint:

`GET /.well-known/oauth-protected-resource`

Purpose:

Tell Claude that `/mcp` is a protected resource and where the authorization server lives.

Expected content should include:

- resource identifier for the MCP server
- authorization server URL
- supported bearer token method
- supported scopes

### Authorization server metadata

Endpoint:

`GET /.well-known/oauth-authorization-server`

Purpose:

Tell Claude where OAuth authorization/token/registration endpoints are.

Expected content should include:

- issuer
- authorization_endpoint
- token_endpoint
- registration_endpoint, if using dynamic client registration
- supported response types
- supported grant types
- PKCE method support, especially S256
- token endpoint auth methods
- supported scopes

### Dynamic client registration

Endpoint:

`POST /oauth/register`

Purpose:

Allow Claude to register itself dynamically if supported/expected.

Should return:

- client_id
- optional client_secret
- redirect_uris
- grant_types
- response_types
- token_endpoint_auth_method

### Authorization endpoint

Endpoint:

`GET /authorize`

Purpose:

Handle Claude's OAuth authorization-code + PKCE flow.

Likely behavior:

1. Validate client_id and redirect_uri.
2. Validate response_type=code.
3. Validate code_challenge and code_challenge_method=S256.
4. Show a simple approval page or use a single-user admin approval flow.
5. Generate a short-lived authorization code.
6. Redirect back to Claude's redirect_uri with `code` and `state`.

### Token endpoint

Endpoint:

`POST /oauth/token`

Purpose:

Exchange auth code + PKCE verifier for access token, and optionally support refresh tokens.

Must validate:

- code exists
- code is not expired
- redirect_uri matches
- client_id matches
- PKCE code_verifier matches stored code_challenge
- resource parameter, if Claude sends it

Should return:

- access_token
- token_type = Bearer
- expires_in
- refresh_token, if implemented
- scope

## Authentication model options

### Option A: minimal single-user OAuth shim

A simple internal OAuth server with:

- one admin/user approval flow
- SQLite token/client/code storage
- short-lived access tokens
- refresh tokens if needed
- minimal HTML approval page

Effort: roughly half day to one day.

Best for initial implementation.

### Option B: external OAuth provider/proxy

Use an OAuth-capable reverse proxy or identity provider in front of the MCP server.

Possible benefits:

- less custom security code
- better-tested OAuth implementation
- easier future hardening

Downside:

- may be trickier to make Claude MCP discovery and resource metadata line up exactly.

### Option C: implement OAuth directly inside `/root/hermes-mcp/server.py`

Possible but less preferred because FastMCP currently works and we do not want to destabilize it.

Could use FastMCP custom routes, but auth-middleware integration around `/mcp` may be more fragile than a proxy.

## Storage needs

Use SQLite for persistent OAuth state.

Possible DB path:

`/root/hermes-mcp/oauth.db`

Tables likely needed:

- oauth_clients
- oauth_auth_codes
- oauth_access_tokens
- oauth_refresh_tokens

Avoid storing real secrets in taskOS docs. Any actual credentials should be represented as `[REDACTED]`.

## Security constraints

- Never commit actual API keys, bearer tokens, OAuth secrets, or connection strings.
- Keep public health endpoints harmless: status only, no secrets.
- `/mcp` must require valid bearer token after OAuth is enabled.
- Authorization codes must be short-lived and one-time-use.
- Access tokens should expire.
- Refresh tokens should be revocable/rotated if implemented.
- PKCE S256 should be required.
- Redirect URIs must be validated.
- Use HTTPS public URL through Tailscale Funnel.
- Rate-limit auth endpoints if practical.

## Acceptance criteria

### Connector behavior

- Claude can add/connect using the public MCP URL.
- Claude discovers OAuth metadata successfully.
- Claude can complete authorization flow.
- Claude can discover MCP tools after auth.
- Claude can call `hermes_health` after auth.
- Claude can call `hermes_ask` after auth.

### Security behavior

- Unauthenticated `/mcp` request returns 401.
- 401 includes `WWW-Authenticate` pointing to protected resource metadata.
- Invalid bearer token is rejected.
- Expired bearer token is rejected.
- Auth code cannot be reused.
- Wrong PKCE verifier fails token exchange.
- Wrong redirect URI fails authorization/token exchange.

### Existing behavior preserved

- Existing FastMCP server remains available internally.
- `/health` and `/mcp/health` return 200 when Hermes backend is healthy.
- Hermes backend `/health` remains checked via `127.0.0.1:8642/health`.
- `hermes_ask` still supports up to 10,000 characters.

## Test plan ideas

Before touching Claude, verify with curl/Python:

1. `GET /health` -> 200.
2. `GET /mcp/health` -> 200.
3. `POST /mcp` with no token -> 401.
4. `GET /.well-known/oauth-protected-resource` -> 200.
5. `GET /.well-known/oauth-authorization-server` -> 200.
6. `POST /oauth/register` -> returns client metadata.
7. `GET /authorize` -> redirects or renders approval UI.
8. `POST /oauth/token` with valid code/verifier -> returns bearer token.
9. `POST /mcp` with bearer token -> MCP initialize 200.
10. MCP `tools/list` -> includes Hermes tools.
11. MCP `tools/call` for `hermes_health` -> success.
12. MCP `tools/call` for `hermes_ask` with multiline payload -> success.

Then test in Claude:

1. Remove old unauthenticated connector.
2. Add connector with public MCP URL.
3. Complete OAuth flow.
4. Enable connector in conversation.
5. Ask Claude to call `hermes_health`.
6. Ask Claude to save a small test note to taskOS or wiki.

## Files likely involved later

Existing:

- `/root/hermes-mcp/server.py`
- `/etc/systemd/system/hermes-mcp.service`

Potential new files:

- `/root/hermes-mcp/oauth_proxy.py`
- `/root/hermes-mcp/oauth.db`
- `/etc/systemd/system/hermes-mcp-oauth.service`
- `/root/hermes-mcp/requirements.txt` updates
- tests/scripts for OAuth flow verification

Potential Tailscale change:

- Funnel should proxy public URL to OAuth proxy port, e.g. `127.0.0.1:8644`, instead of directly to `127.0.0.1:8643`.

## Known decisions

- Keep unauthenticated connector working for now while testing.
- Do not rely on `MCP_API_KEY` as if it were Claude-compatible OAuth.
- Prefer proxy architecture over destabilizing the existing FastMCP server.
- Keep OAuth implementation single-user/minimal first; harden later if needed.
- Use taskOS as the backlog and planning repository for this work before converting into spec/PRD/issues.

## Open questions

- Does Claude require dynamic client registration for this custom connector setup, or can we pre-register client ID/secret manually?
- What exact token endpoint path does Claude prefer if metadata advertises `/oauth/token`?
- Should approval be an HTML page with an admin password, or should auth be restricted by a pre-shared setup token?
- Should refresh tokens be implemented in v0, or should users reconnect periodically?
- Should this eventually become part of Hermes Agent proper or remain a VPS-local bridge?
- Should taskOS itself become a Hermes tool/workflow later?

## Future documents to create

- `docs/spec.md` — exact technical design.
- `docs/prd.md` — user-facing requirements and UX.
- `docs/issues.md` — bite-sized issue list for implementation.
- `docs/implementation-plan.md` — Codex/Hermes execution plan.
