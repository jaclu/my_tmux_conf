#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#

"""Setup a tmate env"""

from sb.sb_muted import SB


class Tmate(SB):
    """plugins to investigate for tmate:
        jaclu/tmux-packet-loss - almost works?
        jaclu/tmux-better-mouse-mode  - needs testing
    lmost"""

    prefix_key = "C-w"
    tmux_bin = "tmate"
    is_limited_host = True  # Trigger display of plugin progress

    # def __init__(self) -> None:
    #    super().__init__(conf_file="~/.tmate.conf", tmux_bin="tmate")

    def status_bar_customization(self, print_header: bool = True) -> bool:
        super().status_bar_customization(print_header=print_header)
        print("><> tmate.py:status_bar_customization()")
        print(f"><> self.sb_left [{self.sb_left}]")
        print(f"self.prefix_key [{self.prefix_key}]")
        if self.prefix_key.lower() != "c-b":
            tag = f"Pfx-{self.prefix_key} "
            self.sb_left = f"#[fg=green,bg=black]{tag}#[default]{self.sb_left}"

        return print_header


if __name__ == "__main__":
    Tmate().run()
