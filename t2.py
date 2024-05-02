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

from ish_host import IshHost
from sb.sb_tst import SB

# from sb.sb_acceptance import SB
# from sb.sb_production import SB


class T2(IshHost, SB):
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

    #  Handled by outer tmux
    def not_plugin_jump(self):
        return ["jaclu/tmux-jump", 99, ""]

    def plugin_packet_loss(self):  # 1.9
        min_vers = 1.9
        if self.is_tmate():
            min_vers = 99  # disable for tmate
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            set -g @packet-loss-ping_host 8.8.8.8

            set -g @packet-loss-ping_count   7
            set -g @packet-loss-history_size 5
            set -g @packet-loss-level_alert 15

            set -g @packet-loss-display_trend     no
            set -g @packet-loss-hist_avg_display  yes

            set -g @packet-loss-level_disp   1

            set -g @packet-loss-color_alert colour21
            set -g @packet-loss-color_bg    colour226

            set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-t2.log

            """,
        ]


if __name__ == "__main__":
    T2().run()
