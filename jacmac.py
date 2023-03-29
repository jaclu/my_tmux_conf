#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  This is for my local MacBook, so plenty of plugins only meaningful for
#  a local system.
#
#  The generated config will only include group headers
#  The more detailed comments in here will not be written, read them here :)
#  The generated config is not really meant to be used as a primary config,
#  I use it when I check various versions for feature and plugin compatibility,
#  and this seemed like a quick way of using my default config,
#  filtering out or replacing incompatible syntax.
#

import sys

# from sb.sb_local import SB
from sb.sb_muted import SB

# from sb.sb_muted import SB
# from default_plugins import DefaultPlugins as SB


class JacMacConfig(SB):
    status_interval = 5

    # use_embedded_scripts = False

    def plugin_packet_loss(self):  # 1.9
        min_vers = 1.9
        if self.is_tmate():
            min_vers = 99  # disable for tmate
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            # set -g @packet-loss-history_size     7
            set -g @packet-loss-weighted_average 1

            set -g @packet-loss-display_trend 1

            set -g @packet-loss-level_disp  3
            set -g @packet-loss-level_alert 18
            set -g @packet-loss-level_crit  40

            set -g @packet-loss-hist_avg_display 1

            set -g @packet-loss-color_alert colour21
            set -g @packet-loss-color_crit  colour196
            set -g @packet-loss-color_bg    colour226
            set -g @packet-loss-prefix |
            set -g @packet-loss-suffix |
            """,
        ]

    def plugin_1password(self):    # ?.?  local
        #
        #  Plugin for 1password CLI tool op
        #
        return ["yardnsm/tmux-1password",
                1.0,
                """
                # set -g @1password-key 'u' # default 'u'
                # set -g @1password-account 'acme' # default 'my'
                # set -g @1password-vault 'work' # default '' (all)
                # set -g @1password-copy-to-clipboard 'on' # default 'off'
                # set -g @1password-filter-tags 'development,servers' # default '' (no tag filtering)
                # set -g @1password-debug 'on' # default 'off'
                """]

    def plugin_keyboard_type(self):  # 1.9  local
        #
        #  When displaying takes 0.8 s to process...
        #
        #  Only meaningful for local tmux!
        #   Tested envs: Darwin, Linux
        #
        #  Display in status-bar with:  #{keyboard_type}
        #
        return [
            "jaclu/tmux-keyboard-type",
            1.9,
            """
            set -g @keyboard_type_hidden  "ABC|U.S.|USInternational-PC"
            set -g @keyboard_type_aliases "Swe=Swedish-Pro|Swe=Swedish|US=U.S."
            set -g @keyboard_type_fg ""
            set -g @keyboard_type_bg "green"
            set -g @keyboard_type_prefix ""
            set -g @keyboard_type_suffix " "
            """,
        ]

    def plugin_mullvad(self):  # 2.2  local
        #
        #   #{mullvad_city}#{mullvad_country}#{mullvad_status}
        #
        min_vers = 2.2
        if self.is_tmate():
            min_vers = 99  # disable for tmate
        return [
            "jaclu/tmux-mullvad",
            min_vers,
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

    # def plugin_nordvpn(self):
    #     return [ 'maxrodrigo/tmux-nordvpn', 0.0, """
    #     set -g @nordvpn_connected_text=""
    #     set -g @nordvpn_connecting_text="🔒"
    #     set -g @nordvpn_disconnected_text="🔓"
    #     """]

    def plugin_spotify(self):  # 1.8  local
        #
        #  Ensure this is only used on MacOS
        #
        #
        name = "jaclu/tmux-spotify-info"
        if sys.platform == "darwin":
            min_v = 1.8
        else:
            min_v = 99
            name = name + "-requires-MacOS"
        if self.is_tmate():
            min_v = 99
        #
        #  Only meaningful for local tmux!     Only works on MacOS
        #
        #  Forked from https://github.com/jdxcode/tmux-spotify-info
        #  My modifications:
        #   Limited max output length - the default sometimes completely
        #   filled the status line if one of the reported fields were
        #   really long
        #
        #  Display in status-bar with: #(tmux-spotify-info)
        #
        if self.vers_ok(2.9):
            conf = """
            #  Version dependent settings for jaclu/tmux-spotify-info
            """
            conf += "bind -N 'Toggle Spotify' -n MouseDown3StatusRight "
            conf += 'run "spotify pause > /dev/null"'
        else:
            conf = ""
        return [name, min_v, conf]

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
        min_vers = 2.2
        if self.is_tmate():
            min_vers = 99  # disable for tmate

        return [
            "jaclu/tmux-battery",
            min_vers,  # 1.8 accd to orig devel, but i get issues below 2.2
            """
            set -g @batt_remain_short 'true'
            """,
        ]


if __name__ == "__main__":
    JacMacConfig().run()
