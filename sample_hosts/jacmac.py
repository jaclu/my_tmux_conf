#!/usr/bin/env python3
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
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


"""JacMac config"""

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)


# flake8: noqa: E402
# pylint: disable=wrong-import-position,import-error
from sb.sb_muted import SB  # noqa: E402


# pylint: disable=R0903
class JacMacConfig(SB):
    """JacMac config"""

    #
    #  Optional plugins, need to be enabled
    #
    # use_plugin_1password = True
    use_plugin_battery = True
    use_plugin_keyboard_type = True
    # use_plugin_mullvad = True
    use_plugin_packet_loss = True
    # use_plugin_spotify_info = True
    # use_plugin_which_key = True
    # use_plugin_yank = True

    def local_overrides(self) -> None:
        """
        Applies local configuration overrides, executed after all other
        configuration steps. These overrides do not affect the status bar
        configuration (see `status_bar_customization()` for that).

        When overriding this method in a subclass, ensure that
        `super().local_overrides()` is called first, to retain any overrides
        defined by parent classes before applying additional customizations.
        """
        super().local_overrides()
        #  Display what class this override comes from
        self.write("# JacMac.local_overides")
        self.write(
            """
            # set -g @packet-loss-ping_host 8.8.8.8
            """
        )


if __name__ == "__main__":
    JacMacConfig().run()
