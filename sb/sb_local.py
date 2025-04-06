#!/usr/bin/env python3
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a local system
#

"""Style local"""

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

# flake8: noqa: E402
# pylint: disable=wrong-import-position,import-error
from default_plugins import DefaultPlugins  # noqa: E402


# pylint: disable=R0903
class SB(DefaultPlugins):
    """Style local"""

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """override statusbar config"""
        fg_clr = "colour226"
        bg_clr = "colour19"
        self.assign_style(__file__)
        super().status_bar_customization(print_header=print_header)

        if self.vers_ok("1.9"):
            self.write(f"set-option -g status-style fg={fg_clr},bg={bg_clr}")
        else:
            self.write(
                f"""
                set-option -g status-fg {fg_clr}
                set-option -g status-bg {bg_clr}
                """
            )
        return print_header  # request footer to be printed


if __name__ == "__main__":
    SB().run()
