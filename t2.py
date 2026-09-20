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
    elif mtc_utils.HOSTNAME in ("JacPad"):
        use_plugin_packet_loss = True
    elif mtc_utils.HOSTNAME in ("JacMac-iSH"):
        use_plugin_claude = False
    elif mtc_utils.HOSTNAME in ("JacDroid",):
        use_plugin_packet_loss = True
        # Can be used on Termux but NOT on iSH
        force_plugin_continuum = True
        use_plugin_resurrect = True

    def plugin_menus(self) -> list:  # 1.5
        #
        # Replacement plugin definition for performance testing on ultra
        # modest platforms, tweaked at minimal overhead
        #
        # when using it:
        #  1 - rename this to plugin_menus
        #  2 - rename local overrides below to something like _local_overrides
        #      or simply remove the lines covering the tmux-menus plugin
        #
        # Once done, simply do a git restore
        #
        if self.use_plugin_menus:
            min_vers = 1.5
        else:
            # it works on iSH, but soo slow it is of no practical usage
            min_vers = -1.0  # Don't use

        if mtc_utils.HOSTNAME in ("JacMac", "kajsa", "hetz2", "cc-dev-1"):
            aim = "Dbg"
            # aim = "Defaults"  # except for trigger
        elif mtc_utils.HOSTNAME in ("JacPad"):
            aim = "SemiDbg"
        else:
            aim = "Perf"
            # aim = "Defaults"  # except for trigger

        # General config
        conf = """

        #
        #  Common basic config
        #
        set -g            @menus_trigger  Space

        set -g     @menus_show_key_hints  No
        set -g  @menus_use_hint_overlays  No

        set -g  @menus_nav_home  '#[fg=colour84]<=='
        set -g  @menus_nav_next  '#[fg=colour220]-->'
        set -g  @menus_nav_prev  '#[fg=colour71]<--'

        # set -g       @menus_use_cache  No

        #  When testing other menu locations
        # set -g  @menus_main_menu  "$HOME/tmp/foo/items/main.sh"

        #
        # No performance degradation once cached, but here is a quick way
        # to disable for testing
        #
        # set -g   @menus_display_commands  No
        # set -g        @menus_danger_zone  '' # disable feature
        """
        if aim == "Defaults":
            # Just unset all general settings that might have been defined
            conf += """

            #
            #  Reset all tmux-menus related settings to defaults, except for trigger
            #
            set -g    @menus_show_key_hints  FORCE-UNSET
            set -g @menus_use_hint_overlays  FORCE-UNSET

            set -g          @menus_nav_home  FORCE-UNSET
            set -g          @menus_nav_next  FORCE-UNSET
            set -g          @menus_nav_prev  FORCE-UNSET

            set -g         @menus_use_cache  FORCE-UNSET
            set -g         @menus_main_menu  FORCE-UNSET
            set -g  @menus_display_commands  FORCE-UNSET
            set -g       @menus_danger_zone  FORCE-UNSET

            set -g @use_bind_key_notes_in_plugins No
            """
        elif aim in ("Dbg", "SemiDbg"):
            # Turn interesting things on to get logging, casche validation etc
            conf += """

            #
            #  Debugging - Turn interesting things on to get logging,
            #              casche validation etc
            #
            set -g           @menus_log_file  "$HOME/tmp/tmux-menus-t2.log"
            set -g         @menus_use_timers  Yes
            set -g     @menus_validate_cache  Yes
            """
        else:
            # optimize for performance
            conf += """
            set -g     @menus_show_key_hints  No
            set -g  @menus_use_hint_overlays  No

            # not having a log_file shortcircuts processing, so saves
            # performance, and is what most users would have set anyhow
            set -g         @menus_use_timers  No
            set -g     @menus_validate_cache  No
            """

        if aim in ("SemiDbg"):
            # Slightly reduce dbg state for limited hosts
            conf += """

            #
            #  Semi Debugging - Slightly dial it down for limited hosts
            #
            set -g     @menus_validate_cache  No
            """

        if self.vers_ok("3.7"):
            conf += """
            #
            # Obsoleted from 3.7 - so unset
            #
            set -g  @menus_use_hint_overlays  FORCE-UNSET
            set -g     @menus_show_key_hints  FORCE-UNSET
            """

        if self.vers_ok(3.4) and aim != "Defaults":
            conf += """
            #
            # tmux menu styling available from 3.4
            #
            # set -g           menu-style  "fg=green,bg=blue"
            # set -g  menu-selected-style  "fg=red,bg=grey"
            # set -g    menu-border-style  "fg=green,bg=default"
            set -g      menu-border-lines  rounded
            """

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
                  set -g @packet-loss-ping_host  "1.1.1.1"

                  ## set -g  @packet-loss-log_file  ""  # Use this to disable logging
                  set -g  @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-t2.log
                """)


if __name__ == "__main__":
    T2().run()
