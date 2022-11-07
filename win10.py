#!/usr/bin/env python3
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

from sb_virtualbox import SB

# from sb_muted import MutedConfig as SB


class Win10Config(SB):
    def plugin_packet_loss(self):  # 1.9
        #
        #  #{packet_loss}
        #
        return [
            1.9,
            "jaclu/tmux-packet-loss",
            """
            set -g @packet-loss-ping_host "8.8.4.4"
            set -g @packet-loss-ping_count "6"
            set -g @packet-loss-history_size "6"
            set -g @packet-loss_weighted_average "1"

            set -g @packet-loss_level_disp "0.1"
            set -g @packet-loss_level_alert "16"
            set -g @packet-loss_level_crit "40"

            #set -g @packet-loss_color_alert "colour181"
            #set -g @packet-loss_color_crit "red"
            #set -g @packet-loss_color_bg "black"

            set -g @packet-loss_prefix " | pkt loss: "
            set -g @packet-loss_suffix " | "
            """,
        ]


if __name__ == "__main__":
    Win10Config().run()
