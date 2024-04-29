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

from sb.sb_virtualbox import SB


class UbuConfig(SB):

    # plugin_handler: str = "tmux-plugins/tpm"
    status_interval = 5

    def plugin_zz_continuum(self) -> list:  # 1.9
        #
        #  Auto restoring a session just as tmux starts on a limited
        #  host will just lead to painfull lag.
        #
        return ["tmux-plugins/tmux-continuum", 99, ""]

    def not_plugin_mullvad(self):  # 2.2  local
        #
        #   #{mullvad_city}#{mullvad_country}#{mullvad_status}
        #
        return [
            "jaclu/tmux-mullvad",
            2.2,
            """
            set -g @mullvad_cache_time ''

            #
            #  I only want to be notified about where the VPN is connected if
            #  not connected to my normal location, typically when avoiding Geo
            #  blocks.
            #  Since this will negatively impact bandwidth and lag, its good to
            #  have a visual reminder.
            #
            set -g @mullvad_excluded_country 'Netherlands'
            set -g @mullvad_excluded_city    'Amsterdam'

            #  No colors wanted for disconnected status, just distracting.
            set -g @mullvad_disconnected_bg_color ' '

            #  Since nothing is printed when connected, we don't need to
            #  bother with the colors
            set -g @mullvad_connected_text ' '

            #  When city/country is printed, use comma as separator
            set -g @mullvad_city_suffix ','

            #
            #  Keep separation if items are displayed
            #
            set -g @mullvad_country_no_color_suffix 1
            set -g @mullvad_status_no_color_suffix 1
            """,
        ]

    #
    #  This is run as a vhost, the next two detect hardware
    #  conditions on the host platform
    #
    def plugin_packet_loss(self):  # 1.9
        min_vers = 1.9
        if self.is_tmate():
            min_vers = 99  # disable for tmate
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            # set -g @packet-loss-ping_host 1.1.1.1
            # set -g @packet-loss-ping_count     7
            # set -g @packet-loss-history_size   5
            # set -g @packet-loss-level_alert 15 # 4-26 6-17 7-15

            set -g @packet-loss-weighted_average  yes
            set -g @packet-loss-display_trend     yes

            set -g @packet-loss-level_disp  5

            set -g @packet-loss-hist_avg_display  yes

            set -g @packet-loss-color_alert  colour21
            set -g @packet-loss-color_bg     colour226

            set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-ubu.log

            """,
        ]

    def plugin_battery(self):  # 2.2  local
        #
        #  #{battery_smart} takes < 5s ATM
        #
        #  Only meaningful for local tmux!
        #
        #  Forked from: https://github.com/tmux-plugins/tmux-battery
        #
        #  My modifications: all important stats can be displayed by using
        #  #{battery_smart} in status bar. When plugged in and fully
        #  charged only the "connected" icon is displayed. If on battery or
        #  charging the percentage is displayed, and remaining time in
        #  colors indicating approximately how full the battery is.
        #
        #  #{battery_smart}
        #
        return [
            "jaclu/tmux-battery",
            2.2,  # 1.8 accd to orig devel, but i get issues below 2.2
            """
            set -g @batt_remain_short 'true'
            """,
        ]


if __name__ == "__main__":
    UbuConfig().run()
