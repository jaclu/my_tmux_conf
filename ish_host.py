#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Changes needed when tmux runs inside iSH, regardless if started
#  localy or via remote shell
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

# import os

from default_plugins import DefaultPlugins
from sb.sb_muted_ish import SB


class IshHost(DefaultPlugins):
    """A typical iSH host"""

    # status_interval = 5

    # plugin_handler = ""

    # use_embedded_scripts = False

    #
    #  Plugins not suitable for limited hosts, iSH being classed as such,
    #  are set to require tmux version 99 in default_plugins.py
    #  Thereby not making them available for iSH hosts
    #


class IshHostWithStyle(IshHost, SB):
    """iSH host with default style"""

    def plugin_packet_loss(self):  # 1.9
        return [
            "jaclu/tmux-packet-loss",
            99.9,
            "",
        ]


if __name__ == "__main__":
    IshHostWithStyle().run()
