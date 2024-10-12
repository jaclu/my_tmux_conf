#!/usr/bin/env python3
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a cloud host
#

""" host hetz1 """

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)


# flake8: noqa: E402
# pylint: disable=wrong-import-position
from default_plugins import OptionalPlugins
from sb.sb_cloud import SB


class Hetz1(SB, OptionalPlugins):
    """hetz1 config"""

    status_interval = 10
    use_plugin_packet_loss = True


if __name__ == "__main__":
    Hetz1().run()
