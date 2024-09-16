#!/usr/bin/env python3
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Used when iSH is run chrooted on hetz1
#

""" host hetz1 """

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

# Make chrooted ish reeally standout, by using production color scheme

# flake8: noqa: E402
# pylint: disable=wrong-import-position
from sb.sb_production import SB

if __name__ == "__main__":
    # SB().run()
    SB().run()
