#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a cloud host
#

from default_plugins import DefaultPlugins


class Hetz1(DefaultPlugins):
    def status_bar_customization(self, print_header=True):
        super().status_bar_customization(print_header=print_header)
        if self.vers_ok("1.9"):
            self.write("set -g status-style fg=black,bg=colour44")
        return print_header  # request footer to be printed


if __name__ == "__main__":
    Hetz1().run()
