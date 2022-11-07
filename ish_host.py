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

    # plugin_handler = "manual"

    # use_embedded_scripts = False

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """This is called just before the status bar is rendered,
        local_overides() is called later so can not modify status bar
        left & right without a pointless reassignment.

        Since I run both iSH and more often iSH-AOK, I keep them
        separated by referring to an AOK node by hostname, and an iSH node
        by hostname-i
        """
        super().status_bar_customization(print_header=print_header)
        if os.path.isfile("/proc/ish/defaults/enable_multicore"):
            self.hostname_template = self.hostname_template.replace(
                "#h", f"{socket.gethostname()}-aok"
            )

        return print_header

    def plugin_packet_loss(self):  # 1.9
        return [
            "jaclu/tmux-packet-loss",
            99,
            """
                set -g @packet-loss_level_alert 17
                set -g @packet-loss_level_crit  "50"
                # debug lvl, to always show packet-loss
                # set -g @packet-loss_level_disp 0.0

                set -g @packet-loss_prefix "|"
                set -g @packet-loss_suffix "|"
                """,
        ]

    def plugin_yank(self):  # 1.9
        #
        #  copies text from the command line to the clipboard.
        #
        #  Default trigger: <prefix> y
        #
        return ["tmux-plugins/tmux-yank", 99, ""]

    def not_plugin_resurrect(self):  # 1.9
        #
        #  Does not work on: iSH
        #
        #  This plugins fails to restore sessions in iSH, at least on my
        #  devices. so no point enabling tmux-resurrect & tmux-continuum
        #  on iSH
        #
        return ["tmux-plugins/tmux-resurrect", 99, ""]

    def not_plugin_zz_continuum(self):  # 1.9
        return ["tmux-plugins/tmux-continuum", 99, ""]


if __name__ == "__main__":
    ishHost().run()
