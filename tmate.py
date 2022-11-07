#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#

from sb.sb_muted import SB


class Tmate(SB):

    prefix_key = "C-w"
    tmux_bin = "tmate"
    is_limited_host = True  # Trigger display of plugin progress

    def status_bar_customization(self, print_header: bool = True) -> bool:
        super().status_bar_customization(print_header=print_header)

        if self.prefix_key.lower() != "c-b":
            tag = f"<P> {self.prefix_key} "
            self.sb_left = f"#[fg=green,bg=black]{tag}#[default]{self.sb_left}"

        used_plugins = self.plugins.found()

        if "jaclu/tmux-packet-loss" in used_plugins:
            self.sb_right = "#{packet_loss}" + self.sb_right
        if "jaclu/tmux-prefix-highlight" in used_plugins:
            self.sb_right += "#{prefix_highlight}"
        return True

    def not_plugin_packet_loss(self):  # 1.9
        # Almost but not completely working in tmate...

        #
        #  #{packet_loss}
        #
        plugin_name = "jaclu/tmux-packet-loss"

        return [
            plugin_name,
            1.9,
            """
            set -g @packet-loss-ping_host "8.8.4.4"

            #  Weighted average last 30 seconds
            #set -g @packet-loss-ping_count "6"
            #set -g @packet-loss-history_size "6"
            #set -g @packet-loss_weighted_average "1"

            #set -g @packet-loss_level_disp "0.1"
            set -g @packet-loss_level_alert "17"
            set -g @packet-loss_level_crit "40"

            #set -g @packet-loss_color_alert "colour181"
            #set -g @packet-loss_color_crit "red"
            #set -g @packet-loss_color_bg "black"

            set -g @packet-loss_prefix "|"
            set -g @packet-loss_suffix "|"
            """,
        ]

    def plugin_prefix_highlight(self):  # 0.0
        #
        #  Highlights when you press tmux prefix key and
        #  when copy/sync mode is active.
        #
        static_conf = """
        set -g @prefix_highlight_show_copy_mode  on
        set -g @prefix_highlight_copy_mode_attr  "fg=black,bg=yellow,bold"
        set -g @prefix_highlight_show_sync_mode  on
        set -g @prefix_highlight_sync_mode_attr "fg=black,bg=orange,blink,bold"
        """
        return ["jaclu/tmux-prefix-highlight", 0.0, static_conf]

    def plugin_better_mouse_mode(self):  # 2.1
        #
        #  A tmux plugin to better manage the mouse.
        #  Emulate mouse scrolling for full-screen programs that doesn't
        #  provide built in mouse support, such as man, less, vi.
        #  Can scroll in non-active 'mouse over-ed' panes.
        #  Can adjust scroll-sensitivity.
        #
        return [
            "jaclu/tmux-better-mouse-mode",
            2.1,
            """
            #  Scroll events are sent to moused-over pane.
            set -g @scroll-without-changing-pane  on

            #  Scroll speed, lines per tic
            set -g @scroll-speed-num-lines-per-scroll  1

            #
            #  Scroll wheel is able to send up & down keys for alternate
            #  screen apps that lacks inherent mouse support
            #
            set -g @emulate-scroll-for-no-mouse-alternate-buffer  on
            """,
        ]


if __name__ == "__main__":
    Tmate().run()
