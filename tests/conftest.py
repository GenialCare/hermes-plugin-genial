"""Fixtures compartilhadas da suíte.

A fixture `hermes_home` cria um HERMES_HOME temporário isolado — a mesma
técnica dos testes manuais que precederam este plugin: NUNCA tocamos na
config real do usuário durante os testes.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture
def hermes_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """HERMES_HOME isolado + garante que variáveis do shell não vazem para os testes."""
    home = tmp_path / "hermes-home"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    return home
