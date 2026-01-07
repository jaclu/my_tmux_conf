#!/usr/bin/env python3
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Template giving the status bar the colors I use for a cloud host
#

"""host hetz2"""

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)


# flake8: noqa: E402
# pylint: disable=E0401, C0413
from default_plugins import DefaultPlugins  # noqa: E402


# pylint: disable=R0903
class Hetz2(DefaultPlugins):
    """hetz2 config"""

    # optionals selected
    use_plugin_packet_loss = True

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """override statusbar config"""
        fg_clr = "black"
        bg_clr = "colour68"
        # 214 - too orange
        self.assign_style(__file__)
        super().status_bar_customization(print_header=print_header)

        if self.vers_ok("1.9"):
            self.write(f"set -g status-style fg={fg_clr},bg={bg_clr}")
        else:
            self.write(
                f"""
                set -g status-fg {fg_clr}
                set -g status-bg {bg_clr}
                """
            )
        return print_header  # request footer to be printed

    def local_overrides(self) -> None:
        """
        Applies local configuration overrides, executed after all other
        configuration steps. These overrides do not affect the status bar
        configuration (see `status_bar_customization()` for that).

        When overriding this method in a subclass, ensure that
        `super().local_overrides()` is called first, to retain any overrides
        defined by parent classes before applying additional customizations.
        """
        super().local_overrides()
        #  Display what class this override comes from
        self.write("# hetz2.local_overides")
        log_file = "~/.dotFiles/latest_statuses/hetz2.log"
        self.write(
            f"""
            set -g @packet-loss-run_disconnected  yes
            set -g @packet-loss-log_file  "{log_file}"
            """
        )


if __name__ == "__main__":
    Hetz2().run()
