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
import socket

from sb.sb_muted import SB


class ishHost(SB):

    is_limited_host = True  # Indicates this host has low performance
    status_interval = 5

    # plugin_handler = "manual"

    use_embedded_scripts = True

    def not_status_bar_customization(self, print_header: bool = True) -> bool:
        """This is called just before the status bar is rendered,
        local_overides() is called later so can not modify status bar
        left & right without a pointless reassignment.

        Since I run both iSH and more often iSH-AOK, I keep them
        separated by referring to an regular iSH nodes by hostname,
        and an iSH-AOK node by hostname-aok
        """
        super().status_bar_customization(print_header=print_header)
        if os.path.isfile("/proc/ish/defaults/enable_multicore"):
            self.hostname_template = self.hostname_template.replace(
                "#h", f"{socket.gethostname()}-aok"
            )

        return print_header

    #
    #  Plugins not suitable for limited hosts, iSH being classed as such,
    #  are set to require tmux version 99 in default_plugins.py
    #  Thereby not making them available for iSH hosts
    #

    def plugin_packet_loss(self):  # 1.9
        return [
            "jaclu/tmux-packet-loss",
            #
            #  I sometimes experiment with this plugin on iSH
            #  When not using it, I set the min version to way above
            #  what will be found.
            #
            # 99,
            1.9,
            """
            # set -g @packet-loss-ping_host 8.8.4.4

            set -g @packet-loss_display_trend 1

            set -g @packet-loss_level_disp 2
            set -g @packet-loss_level_alert 17
            set -g @packet-loss_level_crit 40

            set -g @packet-loss_hist_avg_display 1
            set -g @packet-loss_hist_avg_minutes 30
            
            # set -g @packet-loss_color_alert colour181
            # set -g @packet-loss_color_crit red
            # set -g @packet-loss_color_bg black

            set -g @packet-loss_prefix "|"
            set -g @packet-loss_suffix "|"
            """,
        ]


if __name__ == "__main__":
    ishHost().run()
