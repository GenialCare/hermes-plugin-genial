"""Testes do registro do plugin genial-setup.

Valida o contrato com o plugin system do Hermes: register(ctx) deve
registrar o comando CLI 'genial-setup' apontando para os handlers certos.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


class FakeContext:
    """Dublê do PluginContext do Hermes: captura registros sem importar o Hermes real."""

    def __init__(self):
        self.cli_commands: dict[str, dict] = {}
        self.skills: dict[str, dict] = {}

    def register_cli_command(self, name, help, setup_fn, handler_fn=None, description=""):
        self.cli_commands[name] = {
            "help": help,
            "setup_fn": setup_fn,
            "handler_fn": handler_fn,
            "description": description,
        }
        return name

    def register_skill(self, name, path, description="", frontmatter=None):
        self.skills[name] = {"path": path, "description": description}
        return name


@pytest.fixture
def plugin_module():
    """Importa o __init__.py do plugin pelo caminho (o plugin não é um pacote pip)."""
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    spec = importlib.util.spec_from_file_location("genial_plugin_init", REPO_ROOT / "__init__.py")
    assert spec is not None and spec.loader is not None, "falha ao localizar __init__.py do plugin"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    yield module
    sys.modules.pop("genial_plugin_init", None)


def test_register_registra_comando_cli(plugin_module):
    ctx = FakeContext()
    plugin_module.register(ctx)

    assert "genial-setup" in ctx.cli_commands, (
        "register(ctx) deve registrar o comando CLI 'genial-setup'"
    )
    entry = ctx.cli_commands["genial-setup"]
    assert callable(entry["setup_fn"]), "setup_fn deve ser chamável (configura o argparse)"
    assert callable(entry["handler_fn"]), "handler_fn deve ser chamável (executa a ação)"
    assert entry["help"], "o comando deve ter um help para o 'hermes --help'"
