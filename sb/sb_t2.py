#!/usr/bin/env python3
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a test system
#

"""Style t2 env"""

from ..default_plugins import DefaultPlugins


# pylint: disable=R0903
class SB(DefaultPlugins):
    """Style t2 env"""

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """override statusbar config"""
        fg_clr = "black"
        if self.vers_ok(1.0):
            bg_clr = "colour185"  # "yellow"
        else:
            bg_clr = "yellow"
        w = self.write
        self.assign_style(__file__)
        super().status_bar_customization(print_header=print_header)

        if self.vers_ok("1.9"):
            w(f"set -g status-style fg={fg_clr},bg={bg_clr}")
            # w("set -g status-justify centre")
        else:
            w(
                f"""
                set -g status-fg {fg_clr}
                set -g status-bg {bg_clr}
                """
            )
        return print_header  # request footer to be printed


if __name__ == "__main__":
    SB().run()
    SB().run()
