"""Tests for the genial-setup command parser and handler.

Pure functions (no HERMES_HOME access) — testable without importing the
real Hermes runtime.
"""

from __future__ import annotations

from genial_setup import cli


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


def test_run_returns_zero_and_warns_about_pending_actions(capsys):
    """v0.1: the handler is still a skeleton — it must exit with 0 and be
    explicit that the action does nothing yet (never a silent no-op)."""
    args = cli.build_parser().parse_args([])
    rc = cli.run(args)
    out = capsys.readouterr().out
    assert rc == 0
    assert "ainda não implementada" in out
