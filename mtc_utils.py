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


if os.path.exists("/usr/local/bin/hostname"):
    # For iSH nodes, where the builtin hostname only shows localhost
    cmd = "/usr/local/bin/hostname"
else:
    cmd = "hostname"
HOSTNAME = run_shell(f"{cmd} -s").lower()

IS_ISH_AOK = False
if os.path.isdir("/proc/ish"):
    IS_ISH = True
    with open("/proc/ish/version", "r", encoding="utf-8") as file:
        for line in file:
            if "aok" in line.lower():
                IS_ISH_AOK = True
                break
else:
    IS_ISH = False