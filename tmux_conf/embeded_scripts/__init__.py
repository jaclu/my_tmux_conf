#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/tmux-conf
#
#  See constants.py for version info
#
#  See the README.md in the repository for more info
#

"""Embedded scripts package for tmux-conf.

This package provides functionality for managing and executing embedded
shell scripts within tmux configurations.
"""

from .scripts import EmbeddedScripts

__all__ = ["EmbeddedScripts"]
