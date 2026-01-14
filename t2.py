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

# print("><> t2.py ")


# Pylance complains about the base class here, the above condition confuses it
# pylint: disable=too-many-ancestors
class T2(SB):  # type: ignore
    """Normally the Inner tmux session"""

    t2_env = "1"

    # show_prefix_n_vers_in_sb_colors = ""

    # use_plugin_gentrify = True

    # OB plugin_handler = "manual"
    # plugin_handler: str = "tmux-plugins/tpm"

    # use_embedded_scripts = False
    # is_limited_host = True

    # use_plugin_battery = False
    use_plugin_extrakto = False
    use_plugin_jump = False
    # use_plugin_menus = False
    # use_plugin_mouse_swipe = False
    # use_plugin_power_zoom = False
    use_plugin_session_wizard = False
    use_plugin_suspend = False
    use_plugin_resurrect = False

    if mtc_utils.HOSTNAME == "JacMac":
        use_plugin_battery = True
    elif mtc_utils.HOSTNAME == "JacDroid":
        use_plugin_packet_loss = True
        force_plugin_continuum = True
        use_plugin_resurrect = True

    def plugin_menus(self) -> list:  # 1.5
        #  Tested down to vers 1.5
        if not self.use_plugin_menus:
            # it works on iSH, but soo slow it is of no practical usage
            min_vers = -1.0  # Dont use
        else:
            min_vers = 1.5

        conf = (
            """
        set -g @menus_trigger Space

        # set -g @menus_display_commands "No"
        # set -g @menus_display_cmds_cols 95

        set -g @menus_simple_style_border default
        set -g @menus_simple_style_selected default
        set -g @menus_simple_style default
        set -g @menus_nav_next "#[fg=colour220]-->"
        set -g @menus_nav_prev "#[fg=colour71]<--"
        set -g @menus_nav_home "#[fg=colour84]<=="
        set -g @menus_border_type 'rounded'

        set -g @menus_log_file '~/tmp/tmux-menus-t2.log'
        # set -g @menus_use_cache  No
        set -g @menus_config_file "$TMUX_CONF"

        set -g @menus_use_hint_overlays no
        set -g @menus_show_key_hints no

        # set -g @menus_location_x W
        # set -g @menus_location_y C

        # set -g @menus_main_menu '~/tmp/alt_menu/alt_main.sh'
        # set -g @menus_main_menu "~/my_tmux_menus/main.sh"
        # set -g @menus_main_menu '~/git_repos/mine/tmux-menus/custom_items/_index.sh'
        """
            f"""
        # Hint needed for menus to find the right plugin path
        set-environment -g TMUX_PLUGIN_MANAGER_PATH  "{self.plugins.get_env()[0]}"
        """
        )

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
            # border_active = "colour70"    # pale green
            # border_other = "colour241"  # low intensity grey

            if self.vers_ok(3.2):
                w(
                    f"{self.opt_pane} pane-active-border-style "
                    "'#{?pane_in_mode,fg=yellow,"
                    "#{?synchronize-panes,fg=red,fg=colour70}}'"
                )
                w(
                    f"{self.opt_pane} pane-border-style "
                    "'#{?pane_in_mode,fg=yellow,fg=colour241}'"
                )
            else:
                w(
                    f"""{self.opt_pane} pane-active-border-style fg=colour70
                {self.opt_pane} pane-border-style fg=colour241"""
                )

        if "tmux-packet-loss" in self.plugins.installed(short_name=True):
            w(
                """#
                # tmux-packet-loss - overrides
                #
                # Use a different host vs the outer tmux
                set -g @packet-loss-ping_host "1.1.1.1"

                # set -g @packet-loss-log_file "" # Use this to disable logging
                set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-t2.log
                set -g @packet-loss-run_disconnected No
            """
            )


if __name__ == "__main__":
    T2().run()
