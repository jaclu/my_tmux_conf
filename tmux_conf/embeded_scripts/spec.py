"""
Docstring for tmux_conf.embeded_scripts.script_spec
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScriptSpec:
    """
    Docstring for ScriptSpec
    """

    name: str
    lines: list[str]
    use_bash: bool
    built_in: bool
