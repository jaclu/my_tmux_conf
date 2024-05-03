#!/usr/bin/env python3
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for an acceptance system
#

""" Style aceptance """

# pylint: disable=E0401
from default_plugins import DefaultPlugins


# pylint: disable=R0903
class SB(DefaultPlugins):
    """Style aceptance"""

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """override statusbar config"""
        self.assign_style(__file__)
        super().status_bar_customization(print_header=print_header)
        if self.vers_ok("1.9"):
            self.write("set -g status-style fg=black,bg=colour172")
        else:
            self.write(
                """
                set -g status-fg black
                set -g status-bg colour172
                """
            )
        return print_header  # request footer to be printed


if __name__ == "__main__":
    SB().run()
