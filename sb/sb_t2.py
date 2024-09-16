#!/usr/bin/env python3
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a test system
#

""" Style test """

from mtc_utils import IS_ISH
from sb.sb_tst import SB as SB_tst


# pylint: disable=R0903
class SB(SB_tst):
    """Style test"""

    def status_bar_customization(self, print_header=True):
        """override statusbar config"""
        self.assign_style(__file__)
        # super().status_bar_customization(print_header=print_header)
        if self.vers_ok("1.9"):
            if IS_ISH:
                # only need to overwrite if this is running on iSH,
                # otherwise leave already defined styling as is
                # this gives iSH a slightly different color theme, makes
                # it easier to spot that
                self.write("# iSH override")
                self.write("set -g status-style fg=black,bg=yellow")

        return print_header  # request footer to be printed

    def local_overides(self):
        """Local overrides applied last in the config, not related to
        status bar, for that see status_bar_customization()
        """
        super().local_overides()
        if self.vers_ok(1.9):
            #
            #  Works both on bright and dark backgrounds
            #
            self.write(
                """
                # t2 border style
                set -g pane-active-border-style fg=colour38  #  38 bluish
                set -g pane-border-style        fg=colour95  # 131 grey with a bit red
                """
            )


if __name__ == "__main__":
    SB().run()
