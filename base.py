#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Since iSH has a horrifically poor terminal implementation
#  sessions starting from there has LC_KEYBOARD set, pointing to
#  what keyboard is used on that iOS device.
#  if LC_KEYBOARD is set use IshConsole as base class
#  otherwise use the normal BaseConfig
#

"""Mix in IshConsole when apropriate"""

import os

# print("><> is ish_console imported")
if "LC_KEYBOARD" in os.environ:
    from ish_console import IshConsole

    BaseClass = (IshConsole,)
else:
    import base_config

    BaseClass = (base_config.BaseConfig,)


class BaseConfig(*BaseClass):
    pass


if __name__ == "__main__":
    BaseConfig().run()
