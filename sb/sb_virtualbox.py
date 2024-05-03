#!/usr/bin/env python3
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a (local) virtual box
#

""" Style virtualbox node """

# pylint: disable=E0401
from default_plugins import DefaultPlugins


class SB(DefaultPlugins):
    """Style virtualbox node"""

    fnc_rev_sb_color = "msg_rev_sb_color"

    def status_bar_customization(self, print_header=True):
        """override statusbar config"""
        self.assign_style(__file__)
        super().status_bar_customization(print_header=print_header)
        w = self.write
        self.mkscript_rev_sb_color()
        if self.vers_ok("1.9"):
            w("set -g status-style fg=colour19,bg=colour226")
            w(self.es.run_it(self.fnc_rev_sb_color))
        else:
            w(
                """
                set -g status-fg colour19
                set -g status-bg colour226
                """
            )

        return print_header  # request footer to be printed

    def mkscript_rev_sb_color(self):
        """Reverse statusbar color"""
        cut_this1 = "cut -d',' -f1 | cut -d'='"
        cut_this2 = "cut -d',' -f2 | cut -d'='"
        rev_sb_sh = [
            self.fnc_rev_sb_color + "() {",
            "    #",
            "    #  Reversing the order of fg and bg is so much easier in a",
            "    #  regular script vs trying to do this with tmux notation.",
            "    #",
            '    sb="$TMUX_BIN display -p \\"#{status-style}\\")"',
            "",
            f'    bg_c="$(echo $sb | {cut_this1} -f2)"',
            f'    fg_c="$(echo $sb | {cut_this2} -f2)"',
            '    $TMUX_BIN set -g message-style "fg=$fg_c,bg=$bg_c"',
            "    exit 0 # Ensure exit is true",
            "}",
        ]
        self.es.create(self.fnc_rev_sb_color, rev_sb_sh)


if __name__ == "__main__":
    SB().run()
