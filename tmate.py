#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#

"""Setup a tmate env"""

from sb.sb_test import SB


class Tmate(SB):
    """plugins to investigate for tmate:
        jaclu/tmux-packet-loss - almost works?
        jaclu/tmux-better-mouse-mode  - needs testing
    lmost"""

    prefix_key = "C-b"
    tmux_bin = "tmate"
    is_limited_host = True  # Trigger display of plugin progress

    # use_embedded_scripts = False

    def not_status_bar_customization(self, print_header: bool = True) -> bool:
        """not needed atm, since base already provides vers and prefix display"""
        super().status_bar_customization(print_header=print_header)
        # if self.prefix_key.lower() != "c-b":
        tag = f"#[fg=green,bg=black]{self.prefix_key} #[default]"
        self.sb_left = f"{tag}{self.sb_left}"

        return print_header

    def local_overrides(self) -> None:
        """overrides of general config"""
        super().local_overrides()

        #  First mention what class this override comes from
        self.write(
            """
        # --- Tmate.local_overides()
        # Get rid of tmate occupying status-line forever...
        run-shell -b "sleep 1; $TMUX_BIN display 'Press Enter to clear status-line'"
        """
        )


if __name__ == "__main__":
    Tmate().run()
