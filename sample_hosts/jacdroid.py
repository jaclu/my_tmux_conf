#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
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

"""host: JacDroid"""

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

# flake8: noqa: E402
# pylint: disable=wrong-import-position,import-error
from sb.sb_ish import SB  # noqa: E402


# pylint: disable=too-few-public-methods
class JacDroid(SB):
    """Definitions for host jacdroid"""

    # defaults skipped
    skip_plugin_mouse_swipe = True

    # optionals selected
    use_plugin_packet_loss = True


if __name__ == "__main__":
    JacDroid().run()
