#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  This sets up the t2 environment, meant to run an "inner" tmux, with
#  its own prefix (will be displayed on the status bar)
#
#  This keeps it's own plugin dirs and environment.
#  It is quite convenient to be able to test tmux settings or plugins
#  inside another tmux session without risking to wreck your entire tmux
#  foring you to fix it and then close everythinh down and restart tmux
#  hoping your primary or outer env comes back.
#
#  Also convenient for simply running this on another host than where
#  your primary tmux is running, without having colliding prefix issues
#

# everything, a lot of this is setup
#  in the default file, this is for color theme and selection of often
#  changing list of plugins I am testing
#  out.
import mtc_utils

if mtc_utils.HOSTNAME == "ish-hetz1":
    from sb.sb_acceptance import SB
else:
    # normal theme
    from sb.sb_t2 import SB


class T2(SB):
    """Inner tmux session"""

    t2_env = "1"

    # plugin_handler = "manual"
    # plugin_handler: str = "tmux-plugins/tpm"
    # bind_meta = False
    # use_embedded_scripts = False
    # is_limited_host = True
    status_interval = 5

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

    # def plugin_which_key(self) -> list:
    #     return ['alexwforsythe/tmux-which-key', 3.0, ""]

    def plugin_menus(self) -> list:  # 1.8
        conf = """
        set -g @menus_log_file ~/tmp/tmux-menus-t2.log
        # set -g @menus_use_cache no
        """
        #
        #  This plugin works in tmux 1.7, but that version do not support
        #  @variables, so we say 1.8 here...
        #
        return ["jaclu/tmux-menus", 1.8, conf]

    def plugin_packet_loss(self):  # 1.9
        min_vers = 1.9
        # if mtc_utils.IS_ISH or mtc_utils.HOSTNAME == "ish-hetz1" or self.is_tmate():
        if mtc_utils.IS_ISH or self.is_tmate():
            #  this will draw lots of CPU on hetz1, so disable it
            min_vers = 99.1  # disable for tmate
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            set -g @packet-loss-ping_host 1.1.1.1

            set -g @packet-loss-ping_count   6
            set -g @packet-loss-history_size 6
            set -g @packet-loss-level_alert 18 # 4-26 6-18 7-15

            set -g @packet-loss-display_trend    no
            set -g @packet-loss-hist_avg_display yes
            set -g @packet-loss-run_disconnected no

            set -g @packet-loss-level_disp   5

            set -g @packet-loss-color_alert colour21

            set -g @packet-loss-level_crit 50

            set -g @packet-loss-color_bg    colour226

            set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-t2.log

            """,
        ]


if __name__ == "__main__":
    T2().run()
