#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  This sets up the t2 environment, meant to run an "inner" tmux, with
#  its own prefix (will be displayed on the status bar)
#
#  This keeps it's own plugin dirs and environment.
#  It is quite convenient to be able to test tmux settings or plugins
#  inside another tmux session without risking to wreck your entire tmux
#  foring you to fix it and then close everythinh down and restart tmux
#  hoping your primary or outer env comes back.
#
#  Also convenient for simply running this on another host than where
#  your primary tmux is running, without having colliding prefix issues
#


# everything, a lot of this is setup
#  in the default file, this is for color theme and selection of often
#  changing list of plugins I am testing
#  out.
import mtc_utils

if mtc_utils.HOSTNAME == "ish-hetz1":
    from sb.sb_acceptance import SB
else:
    from sb.sb_t2 import SB  # type: ignore


# Pylance complains about the base class here, the above conditon confuses it
class T2(SB):  # type: ignore
    """Inner tmux session"""

    t2_env = "1"

    status_interval = 5
    # plugin_handler = "manual"
    # plugin_handler: str = "tmux-plugins/tpm"
    # use_embedded_scripts = False
    # is_limited_host = True
    # skip_plugin_session_wizard = True
    # force_plugin_continuum = True
    # use_plugin_packet_loss = True

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
        self.write("# T2.local_overides")

        if self.vers_ok(1.8):
            self.write("set -g @menus_log_file ~/tmp/tmux-menus-t2.log")

        if self.vers_ok(1.9):
            #
            #  Works both on bright and dark backgrounds
            #
            self.write(
                """
                # t2 border style
                set -g pane-active-border-style fg=colour3
                set -g pane-border-style        fg=colour241
                """
            )

    #
    #  Override default plugins with empty stubs for plugins
    #  not wanted in T2_ENV
    #  not_ prefix is when I temp allow them, but keeping the opt out
    #  in case I want them gone again
    #


if __name__ == "__main__":
    T2().run()
