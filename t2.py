#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template I use for my t2 environment, a secondary tmux env on the same
#  system, be it local or remote. This keeps it's own plugin dirs and
#  everything, a lot of this is setup in the default file, this is for
#  color theme and selection of often changing list of plugins I am testing
#  out. It is quite convenient to be able to test tmux settings inside another
#  tmux session, really frustrating when you suddenly cant start tmux and have
#  to revert to multiple session windows
#

# from default_plugins import DefaultPlugins as tmux
# from sb.sb_cloud import SB
# from sb.sb_ish import SB
# from sb.sb_local import SB

# from sb.sb_muted import SB
# from sb.sb_virtualbox import SB

from sb.sb_tst import SB

# from sb.sb_acceptance import SB
# from sb.sb_production import SB


class T2(SB):
    t2_env = "1"

    # plugin_handler = "manual"
    # bind_meta = False
    # use_embedded_scripts = False

    #
    #  Override default plugins with empty stubs for plugins
    #  not wanted in T2_ENV
    #  not_ prefix is when I temp allow them, but keeping the opt out
    #  in case I want them gone again
    #

    #
    #  wont work in an inner tmux, outer is capturing key
    #  in both states. If this is really needed in the inner tmux
    #  a separate capture key for t2 could be defined
    #
    def plugin_suspend(self):
        return ["jaclu/tmux-suspend", 99, ""]

    def plugin_mouse_swipe(self):  # 3.0
        return ["jaclu/tmux-mouse-swipe", 99, ""]

    #  Handled by outer tmux
    def plugin_jump(self):
        return ["jaclu/tmux-jump", 99, ""]

    def not_plugin_yank(self):
        return ["jaclu/tmux-yank", 99, ""]

    def plugin_zz_continuum(self):
        # T2_ENV is a test env, so we do not want auto save/restore of env
        return ["jaclu/tmux-continuum", 99, ""]


if __name__ == "__main__":
    T2().run()
