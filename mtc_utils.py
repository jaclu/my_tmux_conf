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
import platform
import shutil
import subprocess  # nosec


def run_shell(_cmd: str) -> str:
    """Run a command in a shell"""
    # pylint: disable=subprocess-run-check
    result = subprocess.run(_cmd, capture_output=True, text=True, shell=True)  # nosec: B602
    return result.stdout.strip()


def get_currency() -> str:
    """Since these resources are rate limited, use multiple, oredering by random"""
    currency_functions = [
        _get_currency_from_geoplugin,
        _get_currency_from_ipapi,
        _get_currency_from_ipwhois,
    ]

    # Shuffle the list to call the functions in random order
    random.shuffle(currency_functions)

    # Call each function in random order until a non-empty string is returned
    for func in currency_functions:
        # print(f"using: {func}")
        result = func()
        if result:
            return result
    return ""  # Return empty string if no function returns a non-empty string


#
#  Internals
#
def _currency_request(url, tag="currency") -> str:
    """Returns currency for device location, or "" if not detected"""
    result = run_shell("curl -s https://ipapi.co/json")
    # Parse the JSON output
    if result.strip():  # Ensure the command ran successfully
        data = json.loads(result)
        currency = data.get("currency", "Unknown")
    else:
        currency = ""
    return currency


def _get_currency_from_geoplugin():
    """retrieving currency"""
    return _currency_request("http://www.geoplugin.net/json.gp", "geoplugin_currencyCode")


def _get_currency_from_ipwhois():
    """retrieving currency"""
    return _currency_request("https://ipwhois.app/json/", "currency_code")


def _get_currency_from_ipapi() -> str:
    """retrieving currency"""
    return _currency_request("https://ipapi.co/json")


def _get_short_hostname():
    cmd = shutil.which("hostname")
    return run_shell(f"{cmd} -s").lower()


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

is_termux = bool(os.environ.get("TERMUX_VERSION") is not None)
is_darwin = platform.system() == "Darwin"
