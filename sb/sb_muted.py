#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar a somewhat more advanced look
#

from default_plugins import DefaultPlugins

theme_text = "colour135"  # lilaish
muted_text = "colour242"  # grey


class SB(DefaultPlugins):
    def status_bar_customization(self, print_header=True):
        super().status_bar_customization(print_header=print_header)
        w = self.write
        w("# this is sb_muted")
        self.username_template = f"#[fg={theme_text}] #(whoami)#[default]@"
        self.hostname_template = f"#[fg={theme_text}]#h#[default]"
        self.sb_left = f"#[fg={theme_text}]" "#{session_name}" f"#[fg={muted_text}]: "
        self.sb_right = self.sb_right.replace(
            "%a %h", f"#[fg={muted_text}] %a %h")
        w(
            f'set -g window-status-format "#[fg={muted_text}]'
            '#I:#W#{?window_flags,#{window_flags}, }#[default]"'
        )
        w(f'set -g window-status-current-format "#[fg={theme_text}]#W"')
        w("set -g status-justify centre")

        w('set -g message-style "fg=colour251,bg=colour8"')
        w('set -g mode-style "fg=colour251,bg=colour8"')

        if self.vers_ok("1.9"):
            w(f"set -g status-style fg={muted_text},bg=default")
            w("set -g window-status-current-style default")

        return True  # request footer to be printed


if __name__ == "__main__":
    SB().run()
