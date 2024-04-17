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

from sb.sb_cloud import SB


class Hetz1(SB):
    """hetz1 config"""

    status_interval = 5

    def plugin_packet_loss(self):  # 1.9
        min_vers = 1.9
        if self.is_tmate():
            min_vers = 99  # disable for tmate
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            set -g @packet-loss-ping_count    6
            set -g @packet-loss-history_size 6

            set -g @packet-loss-display_trend     1
            set -g @packet-loss-hist_avg_display  1

            set -g @packet-loss-level_alert      26

            set -g @packet-loss-color_alert colour21
            set -g @packet-loss-color_bg    colour226

            set -g @packet-loss-prefix '|'
            set -g @packet-loss-suffix '|'
            """,
        ]


if __name__ == "__main__":
    SB().run()
    # Hetz1().run()
