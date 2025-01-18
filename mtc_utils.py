#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Some common stuff
#
#  Provides constants:
#
#    HOSTNAME   short hostname
#    IS_ISH     (boolean) true if platform is the iOS iSH App
#    IS_ISH_AOK (boolean) true if platform is the iOS-AOK fork
#               If env is iSH-AOK, IS_ISH will also be true
#

"""Common utils"""

import json
import os.path
import shutil
import subprocess  # nosec


def run_shell(_cmd: str) -> str:
    """Run a command in a shell"""
    # pylint: disable=subprocess-run-check
    result = subprocess.run(_cmd, capture_output=True, text=True, shell=True)  # nosec: B602
    return result.stdout.strip()


def get_currency() -> str:
    """Returns currency for device location, or "" if not detected"""
    result = run_shell("curl -s https://ipapi.co/json")
    # Parse the JSON output
    if result.strip():  # Ensure the command ran successfully
        data = json.loads(result)
        currency = data.get("currency", "Unknown")
    else:
        currency = ""
    return currency


HOSTNAME = os.getenv("HOSTNAME_SHORT")
if HOSTNAME:
    HOSTNAME.lower()
else:
    cmd = shutil.which("hostname")
    HOSTNAME = run_shell(f"{cmd} -s").lower()

INNER_TMUX = bool(os.getenv("TMUX_OUTER"))

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

IS_TERMUX = bool(os.environ.get("TERMUX_VERSION") is not None)
