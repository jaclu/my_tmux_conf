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

import subprocess  # nosec

# pylint: disable=subprocess-run-check
result = subprocess.run("hostname -s", capture_output=True, text=True,  # nosec: B607
                        shell=True)  # nosec: B602
hostname = result.stdout.strip()
# print(f"hostname: [{hostname}]")

if hostname == "ish-hetz1":
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
        if self.is_tmate():
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
