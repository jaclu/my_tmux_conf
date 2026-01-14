#!/usr/bin/env python3
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  kajsa - devel server
#

"""host kajsa"""

import os
import sys

# Put the "project path first to support relative imports"
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)


# flake8: noqa: E402
# pylint: disable=E0401, C0413
from sb.sb_cloud import SB  # noqa: E402


# pylint: disable=R0903
class Kajsa(SB):
    """kajsa config"""

    # optionals selected
    use_plugin_packet_loss = True

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
        self.write("# kajsa.local_overides")
        log_file = "~/tmp/packet-loss-kajsa.log"
        self.write(
            f"""
            set -g @packet-loss-run_disconnected  yes
            set -g @packet-loss-log_file  "{log_file}"
            """
        )


if __name__ == "__main__":
    Kajsa().run()
