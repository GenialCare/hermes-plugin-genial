"""Parser e handler do comando `hermes genial-setup`.

Funções puras (sem tocar em HERMES_HOME) para serem testáveis sem o
runtime do Hermes. As ações concretas entram nas Tasks 1.2+ (Fases 1-4).
"""

from __future__ import annotations

import argparse
import sys

PROG = "genial-setup"


def build_parser() -> argparse.ArgumentParser:
    """Parser standalone — usado nos testes e espelhado no register_cli()."""
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
    """setup_fn chamado pelo Hermes: recebe o subparser do comando e espelha
    as mesmas flags do parser standalone."""
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
    """handler_fn chamado pelo Hermes quando o usuário roda `hermes genial-setup`."""
    action = getattr(args, "subcommand", None) or "setup"
    print(f"genial-setup: ação '{action}' ainda não implementada (Tasks 1.2+ do plano).")
    print("Estrutura do comando no ar — as ações reais chegam nas próximas fases.")
    return 0


if __name__ == "__main__":  # permite debug local: python -m genial_setup.cli
    sys.exit(run(build_parser().parse_args()))
