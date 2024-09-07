#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Kind of a .tmux.conf compiler, generating one compatible with the
#  current tmux version.
#
#  Trying my best to keep this in sync with my regular .tmux.conf
#  but no doubt at times they will be slightly out of sync.
#
#  The generated config will only include group headers
#  The more detailed comments in here will not be written, read them here :)
#  The generated config is not really meant to be used as a primary config,
#  I use it when I check various versions for feature and plugin compatibility,
#  and this seemed like a quick way of using my default config,
#  filtering out or replacing incompatible syntax.
#

""" host: JacDroid """

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

# flake8: noqa: E402
# pylint: disable=wrong-import-position
from ish_host import IshHostWithStyle


class JacDroid(IshHostWithStyle):
    status_interval = 5


    # Override unwanted default plugins with disables
    
    def plugin_jump(self) -> list:  # 1.8
        return [ "jump", 99, "" ]
    
    def plugin_mouse_swipe(self) -> list:  # 3.0
        return [ "mouse_swipe", 99, "" ]

    def plugin_prefix_highlight(self) -> list:  # 2.0
        return [ "prefix_highlight", 99, "" ]

    def plugin_resurrect(self) -> list:  # 1.9
        return [ "resurrect", 99, "" ]

    def plugin_session_wizard(self) -> list:  # 3.2
        return [ "session_wizard", 99, "" ]

    def plugin_suspend(self) -> list:  # 2.4
        return [ "suspend", 99, "" ]
    
    def plugin_zz_continuum(self) -> list:  # 1.9
        return [ "continuum", 99, "" ]

	    
if __name__ == "__main__":
    # IshHostWithStyle().run()
    JacDroid().run()
