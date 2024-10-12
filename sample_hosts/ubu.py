#!/usr/bin/env python3
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

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

# flake8: noqa: E402
# pylint: disable=wrong-import-position
from sb.sb_virtualbox import SB


class UbuConfig(SB):

    # plugin_handler: str = "tmux-plugins/tpm"
    status_interval = 5

    def not_plugin_zz_continuum(self) -> list:  # 1.9
        #
        #  Auto restoring a session just as tmux starts on a limited
        #  host will just lead to painfull lag.
        #
        return ["tmux-plugins/tmux-continuum", 99.0, ""]


if __name__ == "__main__":
    UbuConfig().run()
