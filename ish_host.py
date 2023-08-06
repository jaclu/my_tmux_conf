#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
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

#
#  A typical iSH host
#

import os

from sb.sb_muted import SB

# from sb.sb_ish import SB


class ishHost(SB):
    # status_interval = 5

    # plugin_handler = "manual"

    # use_embedded_scripts = False

    #
    #  Plugins not suitable for limited hosts, iSH being classed as such,
    #  are set to require tmux version 99 in default_plugins.py
    #  Thereby not making them available for iSH hosts
    #

    def plugin_packet_loss(self) -> list:  # 1.9
        if os.path.isfile("/etc/debian_version"):
            # Ish Debian tends to fail on this plugin on my (oldish) iPads
            min_vers = 99.0
        else:
            min_vers = 1.9
        return [
            "jaclu/tmux-packet-loss",
            #
            #  I sometimes experiment with this plugin on iSH
            #  When not using it, I set the min version to way above
            #  what will be found.
            #
            min_vers,
            """
            set -g @packet-loss-ping_count    4
            set -g @packet-loss-history_size 10

            set -g @packet-loss-display_trend     1
            set -g @packet-loss-hist_avg_display  1

            set -g @packet-loss-level_alert      26

            set -g @packet-loss-prefix |
            set -g @packet-loss-suffix |
            """,
        ]


if __name__ == "__main__":
    ishHost().run()
