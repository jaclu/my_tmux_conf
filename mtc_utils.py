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
#  Provided methods:
#   run_shell()     - Runs a shell command, returns result as a str
#   get_currency()  - Get local currency as a str, based on public IP#
#  Provides constants:
#   HOSTNAME        hostname -s
#   IS_INNER_TMUX   (bool) this runs inside another tmux session
#   IS_DARWIN       (bool) this system is Darwin (MacOS)
#   IS_ISH          (bool) this system is the iOS iSH App
#   IS_TERMUX       (bool) this system is Termux
#

"""Common utils"""

import json
import os.path
import platform
import random
import shutil
import subprocess  # nosec


#
#  Public methods
#
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
    result = run_shell(f"curl -s {url}")
    # Parse the JSON output
    if result.strip():  # Ensure the command ran successfully
        data = json.loads(result)
        currency = data.get(tag, "Unknown")
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
    HOSTNAME = _get_short_hostname()

IS_INNER_TMUX = bool(os.getenv("TMUX_OUTER"))

IS_DARWIN = platform.system() == "Darwin"
IS_ISH = os.path.isdir("/proc/ish")
IS_TERMUX = os.environ.get("TERMUX_VERSION") is not None
