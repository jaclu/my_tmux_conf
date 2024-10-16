#!/usr/bin/env python3
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  This is for my local MacBook, so plenty of plugins only meaningful for
#  a local system.
#
#  The generated config will only include group headers
#  The more detailed comments in here will not be written, read them here :)
#  The generated config is not really meant to be used as a primary config,
#  I use it when I check various versions for feature and plugin compatibility,
#  and this seemed like a quick way of using my default config,
#  filtering out or replacing incompatible syntax.
#

# pylint: disable=C0116

""" JacMac config """

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)


# flake8: noqa: E402
# pylint: disable=wrong-import-position
from sb.sb_muted import SB


class JacMacConfig(SB):
    """JacMac config"""

    status_interval = 5

    #
    #  Default plugins that can be disabled
    #
    # skip_plugin_mouse_swipe = True
    # skip_plugin_session_wizard = True

    #
    #  Optional plugins, need to be enabled
    #
    # use_plugin_1password = True
    use_plugin_battery = True
    # use_plugin_jump = True
    use_plugin_keyboard_type = True
    # use_plugin_mullvad = True
    use_plugin_packet_loss = True
    # use_plugin_spotify_info = True
    # use_plugin_which_key = True
    # use_plugin_yank = True


if __name__ == "__main__":
    JacMacConfig().run()
