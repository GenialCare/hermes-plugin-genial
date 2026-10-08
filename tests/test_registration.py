"""Tests for the genial-setup plugin registration.

Validates the contract with the Hermes plugin system: register(ctx) must
register the 'genial-setup' CLI command pointing to the right handlers.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


class FakeContext:
    """Test double for the Hermes PluginContext: captures registrations
    without importing the real Hermes."""

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
    """Import the plugin's __init__.py by path (the plugin is not a pip package)."""
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    spec = importlib.util.spec_from_file_location("genial_plugin_init", REPO_ROOT / "__init__.py")
    assert spec is not None and spec.loader is not None, "plugin __init__.py not found"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    yield module
    sys.modules.pop("genial_plugin_init", None)


def test_register_registers_cli_command(plugin_module):
    ctx = FakeContext()
    plugin_module.register(ctx)

    assert "genial-setup" in ctx.cli_commands, (
        "register(ctx) must register the 'genial-setup' CLI command"
    )
    entry = ctx.cli_commands["genial-setup"]
    assert callable(entry["setup_fn"]), "setup_fn must be callable (builds the argparse)"
    assert callable(entry["handler_fn"]), "handler_fn must be callable (runs the action)"
    assert entry["help"], "the command must have a help string for `hermes --help`"
