"""Testes do parser e do handler do comando genial-setup.

O handler e o parser são funções puras — testáveis sem importar o Hermes
real nem tocar em HERMES_HOME.
"""

from __future__ import annotations

import pytest

from genial_setup import cli


def test_parser_aceita_flags_do_setup():
    args = cli.build_parser().parse_args(
        ["--force-mcps", "--skip-browser", "--skip-gcloud"]
    )
    assert args.force_mcps is True
    assert args.skip_browser is True
    assert args.skip_gcloud is True


def test_parser_flags_sao_false_por_padrao():
    args = cli.build_parser().parse_args([])
    assert args.force_mcps is False
    assert args.skip_browser is False
    assert args.skip_gcloud is False


def test_parser_default_e_acao_setup_completa():
    args = cli.build_parser().parse_args([])
    assert args.subcommand is None, "sem subcomando, a ação default é o setup completo"


def test_parser_aceita_subcomandos_gcloud_e_status():
    assert cli.build_parser().parse_args(["gcloud"]).subcommand == "gcloud"
    assert cli.build_parser().parse_args(["status"]).subcommand == "status"


def test_run_retorna_zero_e_avisa_acoes_pendentes(capsys):
    """v0.1: handler ainda é esqueleto — deve sair com 0 e deixar claro que a
    ação ainda não implementa nada (evita 'comando silencioso que não faz nada')."""
    args = cli.build_parser().parse_args([])
    rc = cli.run(args)
    out = capsys.readouterr().out
    assert rc == 0
    assert "ainda não implementada" in out
