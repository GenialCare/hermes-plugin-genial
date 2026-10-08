"""Shared fixtures for the test suite.

The `hermes_home` fixture creates an isolated temporary HERMES_HOME — the
same technique used by the manual tests that preceded this plugin: we NEVER
touch the user's real configuration during tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def hermes_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolated HERMES_HOME; also shields tests from shell environment leakage."""
    home = tmp_path / "hermes-home"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    return home
