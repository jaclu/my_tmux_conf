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
from sb.sb_ish import SB

class JacDroid(SB):
    status_interval = 5

    def plugin_packet_loss(self):  # 1.9
        min_vers = 1.9
        if self.is_tmate():
            min_vers = 99.0  # disable for tmate
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            # set -g @packet-loss-ping_host 1.1.1.1
            set -g @packet-loss-ping_count     6
            set -g @packet-loss-history_size   6
            set -g @packet-loss-level_alert 18 # 4-26 6-18 7-15

            set -g @packet-loss-weighted_average  yes
            set -g @packet-loss-display_trend     no
            set -g @packet-loss-hist_avg_display  yes
            set -g @packet-loss-run_disconnected  yes

            set -g @packet-loss-level_disp  5

            set -g @packet-loss-level_crit 50

            set -g @packet-loss-color_alert  colour21
            set -g @packet-loss-color_bg     colour226

            set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss.log

            """,
        ]

    # Override unwanted default plugins with disables
    
    def plugin_jump(self) -> list:  # 1.8
        return [ "jump", 99, "" ]
    
    def plugin_mouse_swipe(self) -> list:  # 3.0
        return [ "mouse_swipe", 99, "" ]


if __name__ == "__main__":
    # IshHostWithStyle().run()
    JacDroid().run()
