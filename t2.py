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

if mtc_utils.HOSTNAME == "chrooted-iSH":
    from sb.sb_acceptance import SB
else:
    from sb.sb_t2 import SB  # type: ignore

# print("><> t2.py ")


# Pylance complains about the base class here, the above condition confuses it
# pylint: disable=too-many-ancestors
class T2(SB):  # type: ignore
    """Normally the Inner tmux session"""

    pane_border_active_color = "colour70"  # pale green

    use_plugin_continuum = False
    use_plugin_extrakto = False
    use_plugin_jump = False
    use_plugin_resurrect = False
    use_plugin_session_wizard = False
    use_plugin_suspend = False

    if mtc_utils.HOSTNAME in ("JacMac",):
        use_plugin_battery = True
        use_plugin_claude = False
    elif mtc_utils.HOSTNAME in ("JacMac-iSH"):
        use_plugin_claude = False
    elif mtc_utils.HOSTNAME in ("JacDroid",):
        use_plugin_packet_loss = True
        # Can be used on Termux but NOT on iSH
        force_plugin_continuum = True
        use_plugin_resurrect = True

    def plugin_menus(self) -> list:  # 1.5
        #  Tested down to vers 1.5
        if not self.use_plugin_menus:
            # it works on iSH, but soo slow it is of no practical usage
            min_vers = -1.0  # Don't use
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
        super().local_overrides()

        if self.vers_ok(1.8):
            # User variables not present before 1.8
            w = self.write
            #  Display what class this override comes from
            w("# ---  T2.local_overrides()")
            used_plugins = self.plugins.installed(short_name=True)
            if "tmux-claude-usage" in used_plugins:
                w("set -g @claude_usage_color_low colour29")

            if "tmux-packet-loss" in used_plugins:
                w("""#
                # tmux-packet-loss - overrides
                #
                # Use a different host vs the outer tmux
                set -g @packet-loss-ping_host "1.1.1.1"

                # set -g @packet-loss-log_file "" # Use this to disable logging
                set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-t2.log
                """)


if __name__ == "__main__":
    T2().run()
