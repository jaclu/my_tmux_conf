"""
registry
"""

from .spec import ScriptSpec


class ScriptRegistry:  # pylint: disable=too-few-public-methods
    """
    Docstring for ScriptRegistry
    """

    def __init__(self):
        self._defined = set()  # user-defined scripts
        self._built_in_accepted = set()

    def accept(self, spec: ScriptSpec) -> bool:
        """User-defined scripts always register"""
        if not spec.built_in:
            self._defined.add(spec.name)
            return True

        # Built-in scripts only register if not overridden
        if spec.name in self._defined:
            return False

        if spec.name not in self._built_in_accepted:
            self._built_in_accepted.add(spec.name)
            return True

        return False
