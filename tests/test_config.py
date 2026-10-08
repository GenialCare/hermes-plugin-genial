"""Tests for the provider/key configuration step (Task 1.2).

All Hermes interaction happens through subprocess calls to the real `hermes`
CLI — tests mock subprocess.run and use the isolated `hermes_home` fixture,
never the real config.
"""

from __future__ import annotations

from genial_setup import config


def test_env_path_uses_hermes_cli(hermes_home, monkeypatch):
    """Source of truth: the env path comes from `hermes config env-path`,
    never from a hardcoded HERMES_HOME guess (plan finding V5)."""
    recorded = []

    def fake_run(cmd, **kwargs):
        recorded.append(cmd)
        return type("R", (), {"returncode": 0, "stdout": str(hermes_home / ".env") + "\n"})()

    monkeypatch.setattr(config.subprocess, "run", fake_run)
    env_file = config.env_path()
    assert env_file == hermes_home / ".env"
    assert recorded and recorded[0][:2] == ["hermes", "config"]


def test_detect_existing_key(hermes_home):
    env_file = hermes_home / ".env"
    env_file.write_text("# comment\nOPENROUTER_API_KEY=sk-or-existing\n")
    assert config.existing_key(env_file) == "sk-or-existing"


def test_no_key_when_env_file_missing(hermes_home):
    assert config.existing_key(hermes_home / ".env") is None


def test_save_key_creates_directory_and_line(hermes_home):
    env_file = hermes_home / "sub" / "dir" / ".env"
    config.save_key(env_file, "sk-or-new")
    content = env_file.read_text()
    assert content == "OPENROUTER_API_KEY=sk-or-new\n"


def test_reuses_key_from_environment(hermes_home, monkeypatch):
    """If OPENROUTER_API_KEY is exported in the shell (e.g. Claude Code users,
    plan Part 1), reuse it — never prompt. Hermes reads .env only."""
    env_file = hermes_home / ".env"
    result = config.ensure_key(env_file, shell_key="sk-or-from-env", prompt_fn=lambda: (_ for _ in ()).throw(AssertionError("must not prompt")))
    assert result.source == "env"
    assert config.existing_key(env_file) == "sk-or-from-env"


def test_prompts_when_no_key_anywhere(hermes_home, monkeypatch):
    env_file = hermes_home / ".env"
    result = config.ensure_key(env_file, shell_key=None, prompt_fn=lambda: "sk-or-typed")
    assert result.source == "prompt"
    assert config.existing_key(env_file) == "sk-or-typed"


def test_missing_key_raises_with_clear_guidance(hermes_home):
    import pytest

    env_file = hermes_home / ".env"
    with pytest.raises(config.MissingKeyError):
        config.ensure_key(env_file, shell_key=None, prompt_fn=lambda: "")


def test_apply_provider_runs_expected_config_commands(hermes_home, monkeypatch):
    """The 8 `hermes config set` calls (main model + auxiliary + delegation)."""
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(config.subprocess, "run", fake_run)
    config.apply_provider_config()
    flat = [" ".join(c) for c in calls]
    assert all(c.startswith("hermes config set ") for c in flat)
    assert len(flat) == 8
    joined = "\n".join(flat)
    for expected in (
        "model.default anthropic/claude-sonnet-5",
        "model.provider openrouter",
        "model.base_url https://openrouter.ai/api/v1",
        "model.api_mode chat_completions",
        "auxiliary.skills_hub.provider openrouter",
        "auxiliary.skills_hub.model anthropic/claude-sonnet-5",
        "delegation.model anthropic/claude-sonnet-5",
        "delegation.provider openrouter",
    ):
        assert expected in joined, f"missing config call: {expected}"


def test_key_never_appears_in_provider_commands(hermes_home, monkeypatch):
    """The key belongs to .env only — never in config.yaml, never in logs."""
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(" ".join(cmd))
        return type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(config.subprocess, "run", fake_run)
    config.apply_provider_config()
    assert not any("sk-or" in c or "OPENROUTER_API_KEY" in c for c in calls)
