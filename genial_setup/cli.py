"""Parser and handler for the `hermes genial-setup` command.

Pure functions (no HERMES_HOME access) so they can be tested without the
Hermes runtime. Concrete actions land in Tasks 1.2+ (Phases 1-4).

User-facing strings (help texts, prints) are in Portuguese — the plugin's
audience is the Genial Care team. See README "Conventions".
"""

from __future__ import annotations

import argparse
import sys

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


def run(args: argparse.Namespace) -> int:
    """handler_fn called by Hermes when the user runs `hermes genial-setup`."""
    action = getattr(args, "subcommand", None) or "setup"
    print(f"genial-setup: ação '{action}' ainda não implementada (Tasks 1.2+ do plano).")
    print("Estrutura do comando no ar — as ações reais chegam nas próximas fases.")
    return 0


if __name__ == "__main__":  # local debugging: python -m genial_setup.cli
    sys.exit(run(build_parser().parse_args()))
