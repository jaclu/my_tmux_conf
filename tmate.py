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

    #
    #  Default plugins that can be disabled
    #
    # skip_plugin_mouse_swipe = True
    # skip_plugin_session_wizard = True

    #
    #  Optional plugins, need to be enabled
    #
    use_plugin_1password = True
    use_plugin_battery = True
    use_plugin_jump = True
    use_plugin_keyboard_type = True
    use_plugin_mullvad = True
    use_plugin_packet_loss = True
    use_plugin_spotify_info = True
    use_plugin_which_key = True
    use_plugin_plugin_yank = True

    #def __init__(self) -> None:
    #    super().__init__(conf_file="~/.tmate.conf", tmux_bin="tmate")

    def status_bar_customization(self, print_header: bool = True) -> bool:
        super().status_bar_customization(print_header=print_header)

        if self.prefix_key.lower() != "c-b":
            tag = f"<P> {self.prefix_key} "
            self.sb_left = f"#[fg=green,bg=black]{tag}#[default]{self.sb_left}"

        return print_header


if __name__ == "__main__":
    Tmate().run()
