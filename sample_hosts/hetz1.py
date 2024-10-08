#!/usr/bin/env python3
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a cloud host
#

""" host hetz1 """

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

# flake8: noqa: E402
# pylint: disable=wrong-import-position
from sb.sb_cloud import SB


class Hetz1(SB):
    """hetz1 config"""

    status_interval = 10

    def plugin_packet_loss(self):  # 1.9
        min_vers = 1.9
        if self.is_tmate():
            min_vers = 99.0  # disable for tmate
        pkt_loss_log = "$HOME/cloud/Dropbox/machines/hetz1/packet-loss/hetz1.log"
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            f"""
            set -g @packet-loss-ping_host 8.8.8.8

            set -g @packet-loss-hist_avg_display  yes
            set -g @packet-loss-run_disconnected  yes

            set -g @packet-loss-level_crit 50

            set -g @packet-loss-color_alert colour21
            set -g @packet-loss-color_bg    colour226

            set -g @packet-loss-log_file {pkt_loss_log}
            
            """,
        ]


if __name__ == "__main__":
    # SB().run()
    Hetz1().run()
