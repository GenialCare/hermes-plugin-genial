"""Parser and handler for the `hermes genial-setup` command.

Pure dispatch: concrete work lives in the genial_setup submodules
(config, gcloud_install, gcs, browser). User-facing strings (help texts,
prints) are in Portuguese — the plugin's audience is the Genial Care team.
See README "Conventions".
"""

from __future__ import annotations

import argparse
import os
import sys

from genial_setup import config

PROG = "genial-setup"


def build_parser() -> argparse.ArgumentParser:
    """Standalone parser — used in tests and mirrored by register_cli()."""
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Setup guiado do Hermes na Genial Care",
    )
    parser.add_argument(
        "--force-mcps",
        action="store_true",
        help="Sobrescreve os MCPs corporativos existentes com os valores oficiais do GCS",
    )
    parser.add_argument(
        "--skip-browser",
        action="store_true",
        help="Não abre o Chrome com depuração remota (CDP)",
    )
    parser.add_argument(
        "--skip-gcloud",
        action="store_true",
        help="Pula a instalação e autenticação do gcloud",
    )
    sub = parser.add_subparsers(dest="subcommand")
    sub.add_parser("gcloud", help="Instala e autentica apenas o gcloud")
    sub.add_parser("status", help="Diagnóstico do ambiente (self-test)")
    return parser


def register_cli(subparser: argparse.ArgumentParser) -> None:
    """setup_fn called by Hermes: receives the command subparser and mirrors
    the same flags from the standalone parser."""
    subparser.add_argument(
        "--force-mcps", action="store_true",
        help="Sobrescreve os MCPs corporativos existentes com os valores oficiais do GCS",
    )
    subparser.add_argument(
        "--skip-browser", action="store_true",
        help="Não abre o Chrome com depuração remota (CDP)",
    )
    subparser.add_argument(
        "--skip-gcloud", action="store_true",
        help="Pula a instalação e autenticação do gcloud",
    )
    sub = subparser.add_subparsers(dest="subcommand")
    sub.add_parser("gcloud", help="Instala e autentica apenas o gcloud")
    sub.add_parser("status", help="Diagnóstico do ambiente (self-test)")
    subparser.set_defaults(func=run)


def _run_setup(args: argparse.Namespace) -> int:
    """Full setup: provider + OpenRouter key (Task 1.2). Later phases append:
    gcloud (Phase 2), GCS files (Phase 3), browser (Phase 4)."""
    print("==> Configurando provider LLM (Claude Sonnet 5 via OpenRouter)...")

    def prompt() -> str:
        return input("Cole sua chave OpenRouter (sk-or-...) e pressione Enter: ")

    try:
        result = config.ensure_key(
            config.env_path(),
            shell_key=os.environ.get("OPENROUTER_API_KEY"),
            prompt_fn=prompt,
        )
    except config.MissingKeyError as exc:
        print(f"✗ {exc}")
        return 1

    if result.source == "existing":
        print("==> Chave OpenRouter já configurada.")
    elif result.source == "env":
        print("==> Encontrei OPENROUTER_API_KEY já exportada no seu shell — reaproveitando.")
    else:
        print(f"==> Chave OpenRouter salva em {config.env_path()}")

    config.apply_provider_config()
    print("==> Provider configurado: modelo principal, auxiliares e delegação.")

    print("==> Próximas fases (gcloud, MCPs via GCS, browser) ainda não implementadas.")
    return 0


def run(args: argparse.Namespace) -> int:
    """handler_fn called by Hermes when the user runs `hermes genial-setup`."""
    action = getattr(args, "subcommand", None) or "setup"
    if action == "setup":
        return _run_setup(args)
    print(f"genial-setup: ação '{action}' ainda não implementada (Fases 2-4 do plano).")
    return 0


if __name__ == "__main__":  # local debugging: python -m genial_setup.cli
    sys.exit(run(build_parser().parse_args()))
