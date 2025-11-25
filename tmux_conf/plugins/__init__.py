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

"""Plugin management package for tmux-conf.

This package provides comprehensive plugin management for tmux configurations,
including:
- Plugin registration and version checking
- Plugin deployment (TPM or manual)
- Plugin display and reporting
"""

from .manager import Plugins

__all__ = ["Plugins"]
