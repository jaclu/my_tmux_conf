#!/usr/bin/env python3
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
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
#

"""Setup secondary session"""

# everything, a lot of this is setup
#  in the default file, this is for color theme and selection of often
#  changing list of plugins I am testing
#  out.
import mtc_utils

if mtc_utils.HOSTNAME == "ish-hetz1":
    from sb.sb_acceptance import SB
else:
    from sb.sb_t2 import SB  # type: ignore


# Pylance complains about the base class here, the above condition confuses it
# pylint: disable=too-many-ancestors
class T2(SB):  # type: ignore
    """Normally the Inner tmux session"""

    t2_env = "1"

    if mtc_utils.HOSTNAME == "JacMac":
        use_plugin_battery = True

    # use_plugin_gentrify = True

    # plugin_handler = "manual"
    # plugin_handler: str = "tmux-plugins/tpm"

    # use_embedded_scripts = False
    # is_limited_host = True

    def plugin_menus(self) -> list:  # 1.5
        #  Tested down to vers 1.5
        if not self.use_plugin_menus:
            # it works on iSH, but soo slow it is of no practical usage
            min_vers = -1.0  # Dont use
        else:
            min_vers = 1.5

        conf = """
        set -g @menus_trigger Space

        set -g @menus_format_title "'#[fg=yellow,align=left] #{@menu_name} '"
        set -g @menus_simple_style_border "fg=green,bg=default"
        set -g @menus_nav_next "#[fg=colour220]-->"
        set -g @menus_nav_prev "#[fg=colour71]<--"
        set -g @menus_nav_home "#[fg=colour84]<=="
        set -g @menus_border_type 'rounded'

        set -g @menus_display_commands "Yes"
        # set -g @menus_display_cmds_cols 95

        set -g @menus_use_hint_overlays no
        set -g @menus_show_key_hints no

        # ensuring both home and ~ expansion works for single quotes
        set -g @menus_config_file '$HOME/t2/tmux/tmux.conf'

        set -g @menus_log_file '~/tmp/tmux-menus-t2.log'
        # set -g @menus_use_cache  No

        set-environment -g TMUX_PLUGIN_MANAGER_PATH "$HOME/t2/tmux/plugins"
        """
        return ["jaclu/tmux-menus", min_vers, conf]

    def local_overrides(self) -> None:
        """
        Applies local configuration overrides, executed after all other
        configuration steps. These overrides do not affect the status bar
        configuration (see `status_bar_customization()` for that).

        When overriding this method in a subclass, ensure that
        super().local_overrides() is called first, to retain any overrides
        defined by parent classes before applying additional customizations.
        """
        super().local_overrides()
        w = self.write
        #  Display what class this override comes from
        w("# --- T2.local_overides()")

        if self.vers_ok(1.9):
            #
            #  Works both on bright and dark backgrounds
            #  this makes it easier to see if a pane is part of a t2 env
            #
            w(
                """# t2 border style
                set -g pane-active-border-style "fg=yellow"
                set -g pane-border-style        "fg=colour105"
                """
            )

        if "tmux-packet-loss" in self.plugins.installed(short_name=True):
            w(
                """#
                # tmux-packet-loss - overrides
                #
                # Use a different host vs the outer tmux
                set -g @packet-loss-ping_host "8.8.4.4"
                set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-t2.log
                set -g @packet-loss-run_disconnected No
            """
            )


if __name__ == "__main__":
    T2().run()
