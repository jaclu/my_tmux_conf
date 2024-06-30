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

""" host: jacpad-aok """

from ish_host import IshHostWithStyle


class JacPad(IshHostWithStyle):
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
            # set -g @packet-loss-ping_count     7
            # set -g @packet-loss-history_size   5
            # set -g @packet-loss-level_alert 15 # 4-26 6-17 7-15

            set -g @packet-loss-weighted_average  yes

            set -g @packet-loss-level_disp  5

            set -g @packet-loss-hist_avg_display  yes

            set -g @packet-loss-color_alert  colour21
            set -g @packet-loss-color_bg     colour226

            set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-jacpad.log

            """,
        ]


if __name__ == "__main__":
    # IshHostWithStyle().run()
    JacPad().run()
