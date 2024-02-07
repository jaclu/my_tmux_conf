#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Kind of a .tmux.conf compiler, generating one compatible with the
#  current tmux version.
#
#  Trying my best to keep this in sync with my regular .tmux.conf
#  but no doubt at times they will be slightly out of sync.
#
#  The generated config will only include group headers
#  The more detailed comments in here will not be written, read them here :)
#  The generated config is not really meant to be used as a primary config,
#  I use it when I check various versions for feature and plugin compatibility,
#  and this seemed like a quick way of using my default config,
#  filtering out or replacing incompatible syntax.
#

#
#  A typical iSH host
#

import ish_console

from ish_host import ishHost


class Pad5(ishHost):

    ic_keyboard = ish_console.kbd_type_omnitype

    def plugin_power_zoom(self):
        #  this host to slow for this plugin...
        return ["jaclu/tmux-power-zoom", 99, ""]


if __name__ == "__main__":
    Pad5().run()
