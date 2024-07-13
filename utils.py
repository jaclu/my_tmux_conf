#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#

import os.path
import subprocess  # nosec


def run_shell(cmd: str) -> str:
    """Run a command in a shell"""
    # pylint: disable=subprocess-run-check
    result = subprocess.run(
        cmd, capture_output=True, text=True, shell=True  # nosec: B602
    )
    return result.stdout.strip()


#if os.path.exists("/usr/local/bin/hostname"):
#    # For iSH nodes, where the builtin hostname only shows localhost
display_hostname = run_shell("hostname -s")
#else:
#    display_hostname = "#h"
