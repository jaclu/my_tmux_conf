#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a cloud host
#

import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
 
# now we can import the module in the parent
# directory.
from default_plugins import DefaultPlugins


class SB(DefaultPlugins):
    def status_bar_customization(self, print_header=True):
        self.assign_style(__file__)
        super().status_bar_customization(print_header=print_header)
        if self.vers_ok("1.9"):
            self.write("set -g status-style fg=black,bg=colour44")
        return print_header  # request footer to be printed


if __name__ == "__main__":
    SB().run()
