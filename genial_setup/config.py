"""Provider/key configuration (Task 1.2).

Design rules (from the plan):
- `hermes config path` / `hermes config env-path` are the SOURCE OF TRUTH for
  locations — never guess HERMES_HOME (on Windows the default is
  %LOCALAPPDATA%\\hermes, not ~\\.hermes; finding V5).
- The OpenRouter key lives ONLY in the .env file. It must never appear in
  config.yaml, subprocess arguments or logs.
- If OPENROUTER_API_KEY is already exported in the shell (e.g. Claude Code
  users following plan Part 1), reuse it — Hermes reads .env only, so we
  persist it for the user.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

HERMES = "hermes"

# The 8 provider settings: main model + auxiliaries/delegation — same values
# the legacy install scripts wrote (plan Task 1.2).
PROVIDER_SETTINGS: list[tuple[str, str]] = [
    ("model.default", "anthropic/claude-sonnet-5"),
    ("model.provider", "openrouter"),
    ("model.base_url", "https://openrouter.ai/api/v1"),
    ("model.api_mode", "chat_completions"),
    ("auxiliary.skills_hub.provider", "openrouter"),
    ("auxiliary.skills_hub.model", "anthropic/claude-sonnet-5"),
    ("delegation.model", "anthropic/claude-sonnet-5"),
    ("delegation.provider", "openrouter"),
]


class MissingKeyError(RuntimeError):
    """Raised when no OpenRouter key was informed. Setup cannot continue."""


@dataclass
class KeyResult:
    source: str  # "existing" | "env" | "prompt"
    key: str | None


def _run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(cmd)}\n{result.stderr}")
    return result.stdout.strip()


def config_path() -> Path:
    """Source of truth: ask Hermes where config.yaml lives."""
    return Path(_run([HERMES, "config", "path"]))


def env_path() -> Path:
    """Source of truth: ask Hermes where the .env lives."""
    return Path(_run([HERMES, "config", "env-path"]))


def existing_key(env_file: Path) -> str | None:
    """Return the current OPENROUTER_API_KEY value from the .env, or None."""
    if not env_file.exists():
        return None
    for line in env_file.read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            value = line.split("=", 1)[1].strip()
            return value or None
    return None


def save_key(env_file: Path, key: str) -> None:
    """Append the key line, creating parent directories if needed."""
    env_file.parent.mkdir(parents=True, exist_ok=True)
    with open(env_file, "a") as f:
        f.write(f"OPENROUTER_API_KEY={key}\n")


def ensure_key(env_file: Path, shell_key: str | None = None, prompt_fn=None) -> KeyResult:
    """Guarantee an OpenRouter key exists in the .env.

    Priority: existing .env entry > shell environment > prompt.
    Raises MissingKeyError when nothing is informed (the command stops —
    the key is mandatory; plan decision).
    """
    current = existing_key(env_file)
    if current:
        return KeyResult(source="existing", key=current)
    if shell_key:
        save_key(env_file, shell_key)
        return KeyResult(source="env", key=shell_key)
    if prompt_fn is not None:
        key = (prompt_fn() or "").strip()
        if key:
            save_key(env_file, key)
            return KeyResult(source="prompt", key=key)
    raise MissingKeyError(
        "Chave OpenRouter não informada. Sem ela, o Hermes não funciona. "
        "Peça o convite (invite) do OpenRouter para o Matheus Cáceres no canal "
        "#construindo-com-ia e rode este comando de novo."
    )


def apply_provider_config() -> None:
    """Write the 8 provider settings via `hermes config set`."""
    for key, value in PROVIDER_SETTINGS:
        _run([HERMES, "config", "set", key, value])
