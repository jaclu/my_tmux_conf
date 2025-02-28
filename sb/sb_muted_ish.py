#!/usr/bin/env python3
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar a somewhat muted look, this template
#  follow the style used in  https://waylonwalker.com/tmux-status-bar/
#

"""Style muted"""

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

# flake8: noqa: E402
# pylint: disable=wrong-import-position,import-error
import mtc_utils  # noqa: E402
from default_plugins import DefaultPlugins  # noqa: E402

THEME_TEXT = "colour186"  # green with a yellowish tint
MUTED_TEXT = "colour242"  # dark grey


# pylint: disable=R0903
class SB(DefaultPlugins):
    """Style muted"""

    username_template = f"#[fg={THEME_TEXT}] #(whoami)#[default]@"
    sb_left = f"#[fg={THEME_TEXT}]#{{session_name}}#[fg={MUTED_TEXT}]: "

    def status_bar_customization(self, print_header=True):
        """override statusbar config"""
        self.assign_style(__file__)
        super().status_bar_customization(print_header=print_header)
        w = self.write
        w("# this is sb_muted")
        # pylint: disable=W0201
        self.hostname_template = f"#[fg={THEME_TEXT}]{mtc_utils.HOSTNAME}#[default]"

        self.sb_right = self.sb_right.replace("%a %h", f"#[fg={MUTED_TEXT}] %a %h")
        w(
            f'set -g window-status-format "#[fg={MUTED_TEXT}]'
            '#I:#W#{?window_flags,#{window_flags}, }#[default]"'
        )
        w(f'set -g window-status-current-format "#[fg={THEME_TEXT}]#W"')
        w("set -g status-justify centre")

        if self.vers_ok("1.9"):
            w('set -g message-style "fg=colour251,bg=colour8"')  # medium wihte on grey
            w('set -g mode-style "fg=colour251,bg=colour8"')
            w(f"set -g status-style fg={MUTED_TEXT},bg=default")
            w("set -g window-status-current-style default")

        return True  # request footer to be printed


if __name__ == "__main__":
    SB().run()
