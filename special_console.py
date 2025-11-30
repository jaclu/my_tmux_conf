"""
Docstring for hepp
"""

import sys
from typing import Optional

from .base_config import BaseConfig
from .mtc_utils import IS_REMOTE, LC_CONSOLE, LC_KEYBOARD
from .tablet_kbd import KBD_TOUCH, IshConsole, LimitedKbdSpecialHandling, TermuxConsole


def special_consoles_config(tmux_conf_instance: BaseConfig) -> bool:
    """If a special console is detected, apply needed adaptions"""
    if not LC_CONSOLE:
        # If this is not a special console, take no action
        return False

    kbd: Optional[LimitedKbdSpecialHandling]

    if LC_CONSOLE == "iSH" and not IS_REMOTE:
        kbd = IshConsole(tmux_conf_instance, LC_KEYBOARD or KBD_TOUCH)
    elif LC_CONSOLE == "Termux":
        kbd = TermuxConsole(tmux_conf_instance, LC_KEYBOARD or KBD_TOUCH)
    else:
        sys.exit(f"ERROR: Unrecognized LC_CONSOLE:  [{LC_CONSOLE}]")

    if kbd.config_console_keyb():
        return True
    return False
