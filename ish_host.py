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

# pylint: disable=C0116

""" A typical iSH host """

import os

from default_plugins import DefaultPlugins
from sb.sb_muted import SB


class IshHost(DefaultPlugins):
    """A typical iSH host"""

    # status_interval = 5

    hostname_display: str = "(/usr/local/bin/hostname)"

    # plugin_handler = ""

    # use_embedded_scripts = False

    #
    #  Plugins not suitable for limited hosts, iSH being classed as such,
    #  are set to require tmux version 99 in default_plugins.py
    #  Thereby not making them available for iSH hosts
    #

    def not_local_overides(self) -> None:
        super().local_overides()
        self.write(
            """

        set -s escape-time 0

        #  Using Esc prefix for nav keys

        set -s user-keys[200]  "\\302\\247" # Generates §
        bind -N "Switch to -T escPrefix" -n User200 switch-client -T escPrefix

        bind -T escPrefix  User200  send Escape # Double tap for actual Esc
        bind -T escPrefix  Down     send PageDown
        bind -T escPrefix  Up       send PageUp
        bind -T escPrefix  Left     send Home
        bind -T escPrefix  Right    send End
        bind -T escPrefix  User201  send '\\'

        set -s user-keys[201]  "\\302\\261" # Generates '±'  # Usually: ~
        bind -N "Enables ~" -n User201 send '~'

        # ⌥ Option+⇧ Shift+2 in United States layout
        #set -s user-keys[202]  "\\033\\117\\121" # Usually: €
        set -s user-keys[202]  "\\342\\202\\254" # Usually: €

        bind -N "Enables €" -n User202 send '€'
        """
        )

    def not_plugin_packet_loss(self) -> list:  # 1.9
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


class IshHostWithStyle(IshHost, SB):
    """iSH host with default style"""


if __name__ == "__main__":
    IshHostWithStyle().run()
