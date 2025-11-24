"""
Docstring for tmux_conf.embeded_scripts.script_spec
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ScriptSpec:
    """
    Docstring for ScriptSpec
    """

    name: str
    lines: List[str]
    use_bash: bool
    built_in: bool
