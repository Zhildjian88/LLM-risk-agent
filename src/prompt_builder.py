"""
src/prompt_builder.py
Loads prompt templates and injects content for classification.
Generic — no version-specific logic.
Caller is responsible for providing all required placeholders.

Production hardening:
- Escapes { } in user-provided strings to prevent str.format() crashes/injection
  when users paste JSON/code/configs containing braces.
"""

from pathlib import Path
import config


def _escape_braces(value: str) -> str:
    """
    Escape curly braces so Python str.format() treats them as literals.
    Only apply to user-controlled strings, not the template itself.
    """
    if value is None:
        return ""
    return value.replace("{", "{{").replace("}", "}}")


class PromptBuilder:
    def __init__(self, prompt_version: str = None):
        self.version = prompt_version or config.DEFAULT_PROMPT_VERSION
        self.template = self._load_template()

    def _load_template(self) -> str:
        path = Path(config.PROMPT_DIR) / f"{self.version}.txt"
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        return path.read_text()

    def build(self, **kwargs) -> str:
        # Defensive copy
        safe_kwargs = dict(kwargs)

        # Escape braces in any string values coming from callers (likely user text).
        # This prevents crashes when content includes JSON/code with { }.
        for k, v in safe_kwargs.items():
            if isinstance(v, str):
                safe_kwargs[k] = _escape_braces(v)

        try:
            return self.template.format(**safe_kwargs)
        except KeyError as e:
            raise ValueError(
                f"Missing placeholder in prompt template '{self.version}': {e}"
            ) from e
        except Exception as e:
            # Surface formatting problems clearly (e.g., malformed template)
            raise ValueError(
                f"Failed to render prompt template '{self.version}': {e}"
            ) from e
