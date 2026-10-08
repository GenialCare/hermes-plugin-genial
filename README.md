# Hermes Plugin — Genial Care

A Hermes plugin that sets up the Genial Care workspace configuration on your
machine with a single command: `hermes genial-setup`.

> User-facing CLI messages are in Portuguese (the plugin's audience is the
> Genial Care team). Code, docstrings, comments and documentation are in English.

## What the plugin does

| Item | Description |
|---|---|
| LLM provider | `anthropic/claude-sonnet-5` via OpenRouter (main model, auxiliaries and delegation) |
| OpenRouter key | Required — prompted on first run, stored in `~/.hermes/.env` |
| Corporate MCPs | Atlassian, Granola, Slack and Metabase from a centrally managed `mcp.json` on GCS (additive merge) |
| gcloud | Installed and authenticated with your `@genialcare.com.br` account |
| Browser | Chrome with remote debugging (CDP) on port 9222, isolated profile |
| gws | Authentication guidance (client_secret downloaded from GCS) |

## Installation (after installing Hermes)

```shell
hermes plugins install GenialCare/hermes-plugin-genial --enable
hermes genial-setup
```

## Development

```shell
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest -v
```

Official Hermes validation (the same gate as the catalog CI):

```shell
hermes plugins validate . --json
```

## Conventions

- Code, docstrings, comments and documentation in English
- User-facing CLI messages in Portuguese (plugin audience)
- Conventional Commits for every commit (`feat:`, `fix:`, `docs:`, ...)

## Plan

The full implementation plan lives in the author's `.hermes/plans/` — phases:
skeleton → gcloud → GCS (centralized mcp.json + client_secret) → integration →
documentation and legacy script transition.
