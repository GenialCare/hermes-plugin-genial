# ============================================================================
# Plugin Hermes — Genial Care
# ============================================================================
# Nome: genial-setup
# Registra o comando CLI `hermes genial-setup` (setup guiado: provider
# OpenRouter, MCPs corporativos, gcloud, browser CDP).
#
# Plugin 100% NATIVO (plugin.yaml + register(ctx)) — sem plugin.json/mcp.json
# portáteis: o loader do Hermes é exclusivo e ignora o mcp.json quando o
# manifest nativo está presente (ver plano, Task 0.1). Os MCPs corporativos
# são configurados pelo próprio comando via merge aditivo no config.yaml
# (Fase 3), e a skill é registrada via ctx.register_skill (Fase 5).
#
# Uso (após `hermes plugins install GenialCare/hermes-plugin-genial --enable`):
#   hermes genial-setup            # setup completo
#   hermes genial-setup gcloud     # só gcloud (instalar/autenticar)
#   hermes genial-setup status     # diagnóstico do ambiente
# ============================================================================

from __future__ import annotations

from pathlib import Path

from genial_setup import cli

PLUGIN_ROOT = Path(__file__).resolve().parent


def register(ctx) -> None:
    """Chamado pelo plugin system do Hermes no discover/load."""
    ctx.register_cli_command(
        name="genial-setup",
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
