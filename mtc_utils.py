#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
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
#   IS_REMOTE       (bool) if true this is a remote session via mosh/ssh etc
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
# I keep track on if it is a remote session, to be able to figure out if
# this session is using a limited console like if running on an iSH node.
# It can also be used to disable unintentionally activated multi-media related
# plugins. not much point trying to stream audio on a cloud hosted node.
#
IS_REMOTE = bool(os.getenv("SSH_CLIENT"))

#
# I often test things out on a separate tmux instance, that can either run
# standalone or inside the other.
# TMUX_OUTER indicates that one of my envs runs inside the other. In such cases
# any attempt to restart the outer inside the inner is refused to avoid
# bizarre recursive screen updates, and getting disconnected since if the outer
# disconnects the previously inner normally also disappears.
#
IS_INNER_TMUX = bool(os.getenv("TMUX_OUTER"))

#
#  If the session originated on a "primitive keyboard" console, such as
#  iSH or Termux, it is indicated in LC_CONSOLE
#
LC_CONSOLE = os.getenv("LC_CONSOLE") or ""

#
#  Hosts with limited consoles should also list what keyboard they are using
#  in order for tablet_kbd.py to make correct workarounds
#
LC_KEYBOARD = os.getenv("LC_KEYBOARD") or ""

#
#   List hostname where session started, purely informational
#
LC_ORIGIN = os.getenv("LC_ORIGIN") or ""


HOSTNAME = os.getenv("HOSTNAME_SHORT") or ""

IS_DARWIN = platform.system() == "Darwin"
IS_ISH = os.path.isdir("/proc/ish")
IS_TERMUX = os.environ.get("TERMUX_VERSION") is not None
IS_GHOSTTY: bool = os.environ.get("TERM_PROGRAM") == "ghostty"

# muc keys and default values
K_M_PLUS = "M-+"
K_M_UNDERSCORE = "M-_"
K_M_P = "M-P"
K_M_X = "M-X"
K_M_H = "M-h"
K_M_J = "M-j"
K_M_K = "M-k"
K_M_L = "M-l"

#
#  Define some error types
#
ERROR_INCOMPATIBLE_TMUX_CONF_LIB = 64
ERROR_MISSING_KEY_IN_MUC_KEYS = 65
ERROR_USER_KEY_NOT_OCTAL = 65
ERROR_T2_USING_DEF_TMUX_CONF = 67
ERROR_STYLE_REDEFINED = 68


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
def _currency_request(url: str, tag: str = "currency") -> str:
    """Returns currency for device location, or "" if not detected"""
    result = run_shell(f"curl -s {url}")
    # Parse the JSON output
    if result.strip():  # Ensure the command ran successfully
        data = json.loads(result)
        currency: str = data.get(tag, "Unknown")
    else:
        currency = ""
    return currency


def _get_currency_from_geoplugin() -> str:
    """retrieving currency"""
    return _currency_request("http://www.geoplugin.net/json.gp", "geoplugin_currencyCode")


def _get_currency_from_ipwhois() -> str:
    """retrieving currency"""
    return _currency_request("https://ipwhois.app/json/", "currency_code")


def _get_currency_from_ipapi() -> str:
    """retrieving currency"""
    return _currency_request("https://ipapi.co/json")


def _get_short_hostname() -> str:
    cmd = shutil.which("hostname")
    return run_shell(f"{cmd} -s").lower()


# ===============================================================
#
#   Main
#
# ===============================================================

if HOSTNAME:
    HOSTNAME.lower()
else:
    HOSTNAME = _get_short_hostname()
