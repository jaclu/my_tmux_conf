#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#

from sb.sb_muted import SB


class Tmate(SB):
    """plugins to investigate for tmate:
        jaclu/tmux-packet-loss - almost works?
        jaclu/tmux-better-mouse-mode  - needs testing
    lmost"""

    prefix_key = "C-w"
    tmux_bin = "tmate"
    is_limited_host = True  # Trigger display of plugin progress

    # use_plugin_packet_loss = True

    def status_bar_customization(self, print_header: bool = True) -> bool:
        super().status_bar_customization(print_header=print_header)

        if self.prefix_key.lower() != "c-b":
            tag = f"<P> {self.prefix_key} "
            self.sb_left = f"#[fg=green,bg=black]{tag}#[default]{self.sb_left}"

        return print_header


if __name__ == "__main__":
    Tmate().run()
