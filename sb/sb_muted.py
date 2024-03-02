#!/usr/bin/env python3
#
#  Copyright (c) 2022,2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar a somewhat muted look, this template
#  follow the style used in  https://waylonwalker.com/tmux-status-bar/
#

from default_plugins import DefaultPlugins

theme_text = "colour135"  # lilac / magenta, not sure how to label this
muted_text = "colour242"  # grey


class SB(DefaultPlugins):
    username_template = f"#[fg={theme_text}] #(whoami)#[default]@"
    sb_left = f"#[fg={theme_text}]" "#{session_name}" f"#[fg={muted_text}]: "

    def status_bar_customization(self, print_header=True):
        self.assign_style(__file__)
        super().status_bar_customization(print_header=print_header)
        w = self.write
        w("# this is sb_muted")
        self.hostname_template = f"#[fg={theme_text}]#{self.hostname_display}#[default]"

        self.sb_right = self.sb_right.replace(
            "%a %h", f"#[fg={muted_text}] %a %h")
        w(
            f'set -g window-status-format "#[fg={muted_text}]'
            '#I:#W#{?window_flags,#{window_flags}, }#[default]"'
        )
        w(f'set -g window-status-current-format "#[fg={theme_text}]#W"')
        w("set -g status-justify centre")

        if self.vers_ok("1.9"):
            w('set -g message-style "fg=colour251,bg=colour8"')
            w('set -g mode-style "fg=colour251,bg=colour8"')
            w(f"set -g status-style fg={muted_text},bg=default")
            w("set -g window-status-current-style default")

        return True  # request footer to be printed


if __name__ == "__main__":
    SB().run()
