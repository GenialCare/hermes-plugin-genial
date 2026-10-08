"""Tests for the genial-setup command parser and handler.

Pure dispatch tests: the setup action delegates to genial_setup.config
(monkeypatched here so no real `hermes` CLI is invoked); subcommands that
are not implemented yet must say so explicitly.
"""

from __future__ import annotations

import pytest

from genial_setup import cli, config


def test_parser_accepts_setup_flags():
    args = cli.build_parser().parse_args(
        ["--force-mcps", "--skip-browser", "--skip-gcloud"]
    )
    assert args.force_mcps is True
    assert args.skip_browser is True
    assert args.skip_gcloud is True


def test_parser_flags_default_to_false():
    args = cli.build_parser().parse_args([])
    assert args.force_mcps is False
    assert args.skip_browser is False
    assert args.skip_gcloud is False


def test_parser_default_action_is_full_setup():
    args = cli.build_parser().parse_args([])
    assert args.subcommand is None, "with no subcommand, the default action is the full setup"


def test_parser_accepts_gcloud_and_status_subcommands():
    assert cli.build_parser().parse_args(["gcloud"]).subcommand == "gcloud"
    assert cli.build_parser().parse_args(["status"]).subcommand == "status"


@pytest.fixture
def mocked_config(monkeypatch, hermes_home):
    """Isolate the setup action: env path points to the isolated home and the
    `hermes config set` calls are recorded without touching the real machine."""
    calls: list[list[str]] = []
    monkeypatch.setattr(cli.config, "env_path", lambda: hermes_home / ".env")
    monkeypatch.setattr(
        cli.config, "apply_provider_config", lambda: calls.append(["config-set"])
    )
    return hermes_home, calls


def test_run_setup_saves_key_from_prompt_and_applies_provider(mocked_config, monkeypatch, capsys):
    hermes_home, calls = mocked_config
    monkeypatch.setattr("builtins.input", lambda prompt="": "sk-or-typed")
    rc = cli.run(cli.build_parser().parse_args([]))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Chave OpenRouter salva em" in out
    assert calls == [["config-set"]], "provider settings must be applied once"
    assert (hermes_home / ".env").read_text() == "OPENROUTER_API_KEY=sk-or-typed\n"


def test_run_setup_reuses_existing_key_without_prompt(mocked_config, capsys):
    hermes_home, calls = mocked_config
    (hermes_home / ".env").write_text("OPENROUTER_API_KEY=sk-or-existing\n")
    rc = cli.run(cli.build_parser().parse_args([]))
    out = capsys.readouterr().out
    assert rc == 0
    assert "já configurada" in out
    assert calls == [["config-set"]]


def test_run_setup_missing_key_fails_with_guidance(mocked_config, monkeypatch, capsys):
    def raise_missing(*a, **k):
        raise config.MissingKeyError("Chave OpenRouter não informada.")

    monkeypatch.setattr(cli.config, "ensure_key", raise_missing)
    rc = cli.run(cli.build_parser().parse_args([]))
    out = capsys.readouterr().out
    assert rc == 1, "setup must stop (exit 1) when the key is missing"
    assert "Chave OpenRouter não informada" in out


def test_run_setup_missing_key_never_prints_typed_secret(mocked_config, monkeypatch, capsys):
    """The typed key must not leak to stdout even in the failure path."""
    monkeypatch.setattr("builtins.input", lambda prompt="": "sk-or-secret-typed")
    monkeypatch.setattr(
        cli.config,
        "ensure_key",
        lambda *a, **k: (_ for _ in ()).throw(config.MissingKeyError("missing")),
    )
    cli.run(cli.build_parser().parse_args([]))
    out = capsys.readouterr().out
    assert "sk-or-secret-typed" not in out


def test_run_pending_subcommands_say_so_explicitly(capsys):
    """gcloud (Phase 2) and status (Phase 4) are not implemented yet — they
    must never be silent no-ops."""
    for sub in ("gcloud", "status"):
        args = cli.build_parser().parse_args([sub])
        rc = cli.run(args)
        out = capsys.readouterr().out
        assert rc == 0
        assert "ainda não implementada" in out
