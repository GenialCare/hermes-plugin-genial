# ============================================================================
# Hermes Plugin — Genial Care
# ============================================================================
# Name: genial-setup
# Registers the CLI command `hermes genial-setup` (guided setup: OpenRouter
# provider, corporate MCPs, gcloud, browser CDP).
#
# This is a 100% NATIVE plugin (plugin.yaml + register(ctx)) — no portable
# plugin.json/mcp.json: the Hermes loader is exclusive and ignores mcp.json
# when the native manifest is present (see plan, Task 0.1). Corporate MCPs
# are configured by the command itself via additive merge into config.yaml
# (Phase 3), and the skill is registered via ctx.register_skill (Phase 5).
#
# Usage (after `hermes plugins install GenialCare/hermes-plugin-genial --enable`):
#   hermes genial-setup            # full setup
#   hermes genial-setup gcloud     # gcloud only (install/authenticate)
#   hermes genial-setup status     # environment diagnostics
# ============================================================================

from __future__ import annotations

from pathlib import Path

from genial_setup import cli

PLUGIN_ROOT = Path(__file__).resolve().parent


def register(ctx) -> None:
    """Called by the Hermes plugin system during discovery/load."""
    ctx.register_cli_command(
        name="genial-setup",
        # help/description are user-facing (shown in `hermes --help`) — kept in
        # Portuguese on purpose; see README "Conventions".
        help="Setup guiado do Hermes na Genial Care (provider, MCPs, gcloud, browser)",
        setup_fn=cli.register_cli,
        handler_fn=cli.run,
        description=(
            "Configura o Hermes padrão da máquina com o setup da Genial Care: "
            "provider LLM (Claude Sonnet 5 via OpenRouter), MCPs corporativos "
            "(atlassian, granola, slack, metabase), gcloud com conta Genial e "
            "browser connect via CDP."
        ),
    )
