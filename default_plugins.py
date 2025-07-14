#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Includes plugins I "always" use, regardless of Local vs Remote node
#
#  Since I use this on older tmux versions, I can't use line continuation
#  on tmux commands, so some of those lines are really long...
#
#  The generated config is not really meant to be used as a primary source
#  of the setup it will include group headers and some comments suck in
#  from here, but this is the canonical place to observe the code.
#
#  I use this when I check various versions for feature and plugin
#  compatibility.
#

# pylint: disable=C0116

"""Defines default plugins"""

import os

#
#  Since I often run this on iSH, this class will bind missing keys in the
#  case this is run directly on the IshConsole, in all other cases it will
#  do nothing
#
import mtc_utils
from base import BaseConfig  # BaseConfig


class DefaultPlugins(BaseConfig):
    """
    Any method starting with plugin_ will be assumed to be a plugin
    definition, and handled as such by the TmuxConfig class.

    Plugins will be ordered alphabetically based on method name.
    Normally order has no significance, but in some cases order is significant
    therefore  the method handling "tmux-continuum" is named plugin_zz_continuum()

    Syntax for plugins methods:

    The method should return a triplet:
        min_version
        plugin name - needed when installing it, and to identify it.
        code snippet defining plugin variables

    Plugin definitions can use self.write() in their code block, but this
    is not recommended, instead generate a string and supply as mentioned above

    Calling self.plugins.installed(short_name=True) will give a name of
    all plugins that will be used, so can be used to define the status bar
    """

    #
    #  Override all other env settings like is_limited_host or is_tmate
    #  and ensure plugin is used or not
    #
    force_plugin_continuum = False

    #
    #  Default plugins that can be disabled
    #
    use_plugin_better_mouse_mode = True
    use_plugin_continuum = True
    use_plugin_extrakto = True
    use_plugin_jump = True
    use_plugin_menus = True
    use_plugin_mouse_swipe = True
    use_plugin_power_zoom = True
    use_plugin_resurrect = True
    use_plugin_session_wizard = True
    use_plugin_suspend = True

    if mtc_utils.IS_ISH:
        use_plugin_session_wizard = False

    #
    # Replaced by corresponding use_plugin variables
    #

    if mtc_utils.IS_INNER_TMUX:
        #  Doesn't make much sense in an inner tmux
        use_plugin_mouse_swipe = False
        # use_plugin_power_zoom = False
        # use_plugin_session_wizard = False

    #
    #  Optional plugins, need to be enabled. Be aware since they are
    #  actively selected, there is no env checks being done if it should
    #  be used or not
    #
    use_plugin_battery = False
    use_plugin_mullvad = False
    use_plugin_spotify_info = False

    use_plugin_1password = False
    use_plugin_gentrify = False
    use_plugin_keyboard_type = False
    use_plugin_packet_loss = False
    use_plugin_which_key = False
    use_plugin_yank = False

    #
    #  The default is to use jaclu/tpm, with built in support for
    #  TMUX_BIN and some improvements in reporting progress during
    #  install/removal of plugins.
    #  If you prefer to use the original uncomment this
    #
    # plugin_handler = "tmux-plugins/tpm"

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """This is called just before the status bar is rendered,
        local_overrides() is called later so can not modify status bar
        left & right without a pointless reassignment.

        I use this to add hooks for plugins that are currently used.

        I have come to realize that leaving them in for non active plugins
        is not desired.

        If the plugin code is present in ~/.tmux/plugins,
        even if not used, status bar actions are happening.
        If it is not intended to be used, errors might be triggered.

        If print_header=True is sent back to the BaseCofig instance,
        it will print a header. If this returns True a footer will be
        printed.
        """

        super().status_bar_customization(print_header=print_header)

        if not self.style:
            self.assign_style("host not recognized - No style is used")

        #
        #  Plugin-hooks for status-bar, enable an item if that plugin
        #  is used, in order to get a consistent status-bar order,
        #  I also include plugins only used on some nodes here.
        #
        used_plugins = self.plugins.installed(short_name=True)

        #  Consider adding placement for

        if "tmux-suspend" in used_plugins:
            # pylint: disable=E0203,W0201
            self.sb_right += "#{@mode_indicator_custom_prompt}"

        if "tmux-mullvad" in used_plugins:
            # pylint: disable=E1101
            self.sb_left += "#{mullvad_city}#{mullvad_country}"
            self.sb_left += "#{mullvad_status}"

        if "tmux-keyboard-type" in used_plugins:
            # pylint: disable=W0201
            self.sb_right = "#{keyboard_type}" + self.sb_right

        if "tmux-battery" in used_plugins:
            # pylint: disable=W0201
            self.sb_right = "#{battery_smart} " + self.sb_right

        if "tmux-spotify-info" in used_plugins:
            # pylint: disable=W0201
            self.sb_right = "#[bg=colour28]#(tmux-spotify-info)#[default] " + self.sb_right

        if "tmux-packet-loss" in used_plugins:
            # pylint: disable=W0201
            self.sb_right = "#{packet_loss}" + self.sb_right

        return True  # request footer to be printed

    #
    #  Plugin functions should return a list containing:
    #    - name of plugin (where to download it on github if TPM is used)
    #    - min version of tmux it supports (-1 means plugin is ignored)
    #    - text blob, containing plugin config, written to tmux conf
    #

    # ----------------------------------------------------------
    #
    #  Group one, plugins I typically always use, unless it is redundant
    #  in an inner session, or is to resource demanding on limited nodes
    #
    # ----------------------------------------------------------

    def plugin_better_mouse_mode(self) -> list:  # [str | float | int]:  # 2.1
        """A tmux plugin to better manage the mouse.
        Emulate mouse scrolling for full-screen programs that doesn't
        provide built in mouse support, such as man, less, vi.
        Can scroll in non-active 'mouse over-ed' panes.
        Can adjust scroll-sensitivity."""

        if not self.use_plugin_better_mouse_mode or self.is_tmate():
            # Is needed also in an inner tmux!
            vers_min = -1.0  # Dont use
        else:
            vers_min = 2.1

        return [
            "jaclu/tmux-better-mouse-mode",
            vers_min,
            """
            #  Scroll events are sent to moused-over pane.
            set -g @scroll-without-changing-pane  on

            #  Scroll speed, lines per tic
            set -g @scroll-speed-num-lines-per-scroll  1

            #
            #  Scroll wheel is able to send up & down keys for alternate
            #  screen apps that lacks inherent mouse support
            #
            set -g @emulate-scroll-for-no-mouse-alternate-buffer  on
            """,
        ]

    def plugin_extrakto(self) -> list:  # 3.2
        """Can be used on older versions with limitations
        Popup allowing for selection of items on screen
        tab for insert tested down to 1.8
        enter to copy instakills asdf local tmux
        Default trigger: <prefix> Tab
        """
        if not self.use_plugin_extrakto or mtc_utils.IS_ISH:
            # the popup gets stuck on iSH
            vers_min = -1.0
        else:
            vers_min = 1.8

        conf = """
        set -g @extrakto_grab_area "window recent"
        """
        if os.getenv("TMUX_NO_CLIPBOARD"):
            conf += """
            # Will only paste into tmux clipboard to prevent tmux insta-crash
            set -g @extrakto_clip_tool ">/dev/null"
            """
        else:
            if self.vers_ok(3.2):
                conf += """
                # allow tmux OSC52 to set the clipboard
                set -g @extrakto_clip_tool_run "tmux_osc52"
                set -g @extrakto_clip_tool ">/dev/null"
                """
            else:
                conf += """
                # manually pipe to OSC52
                set -g @extrakto_clip_tool_run "fg"
                set -g @extrakto_clip_tool "osc_52_send"
                """
        return ["jaclu/extrakto", vers_min, conf]

    def plugin_jump(self) -> list:  # 2.4
        """Jump to word(-s) on the screen that you want to copy,
        without having to use the mouse.
        Default trigger: <prefix> u
        """
        if not self.use_plugin_jump or mtc_utils.IS_ISH or mtc_utils.IS_TERMUX:
            # it seems Termux fails to handle ttys
            # it works on iSH, but soo slow it is of no practical usage
            min_vers = -1.0  # Dont use
        else:
            min_vers = 2.4

        return [
            "jaclu/tmux-jump",  # was Lenbok
            min_vers,
            #
            #  The weird jump key syntax below is how I both sneak in
            #  a note and make the key not to depend on prefix :)
            #
            """#  Additional dependency: ruby >= 2.3
            set -g @jump-key "-N plugin_Lenbok/tmux-jump  u"
            # set -g @jump-keys-position 'off_left'
            """,
        ]

    def plugin_menus(self) -> list:  # 1.5
        #  Tested down to vers 1.5
        #  Default trigger: <prefix> Space
        if self.use_plugin_menus:
            min_vers = 1.5
        else:
            # it works on iSH, but soo slow it is of no practical usage
            min_vers = -1.0  # Dont use

        return [
            "jaclu/tmux-menus",
            min_vers,
            """
            # set -g @menus_use_cache no

            set -g @menus_trigger Space
            # set -g @menus_without_prefix No

            # set -g @menus_location_x C
            # set -g @menus_location_y C

            set -g @menus_display_commands Yes
            # set -g @menus_display_cmds_cols 170

            set -g @menus_use_hint_overlays No
            # set -g @menus_show_key_hints Yes

            set -g @menus_border_type 'rounded'
            #
            #  Slightly catppuccin frappe inspired
            #
            # fg @thm_surface_0 bg @thm_yellow
            # set -g @menus_simple_style_selected "fg=#414559,bg=#e5c890"
            # set -g @menus_simple_style "bg=#414559"        # @thm_surface_0
            # set -g @menus_simple_style_border "bg=#414559" # @thm_surface_0

            set -g @menus_simple_style_selected default
            set -g @menus_simple_style default
            set -g @menus_simple_style_border default

            set -g @menus_nav_next "#[fg=colour220]-->"
            set -g @menus_nav_prev "#[fg=colour71]<--"
            set -g @menus_nav_home "#[fg=colour84]<=="

            set -g @menus_log_file "$HOME/tmp/tmux-menus.log"
            """,
        ]

    def plugin_mouse_swipe(self) -> list:  # 3.0
        """right-click & swipe switches Windows / Sessions"""
        if not self.use_plugin_mouse_swipe or self.is_limited_host:
            min_vers = -1.0  # Dont use
        else:
            min_vers = 3.0

        return [
            "jaclu/tmux-mouse-swipe",
            min_vers,
            """
            #  right-click & swipe switches Windows / Sessions
            """,
        ]

    def plugin_power_zoom(self) -> list:  # 2.0
        """Zooms to separate Window, to allow for adding support panes
        Default trigger: <prefix> Z
        """
        if not self.use_plugin_power_zoom or self.is_tmate():
            vers_min = -1.0  # Dont use
        else:
            vers_min = 2.0

        conf = """
        set -g @power_zoom_trigger  Z
        """
        if self.vers_ok(3.0):
            #  Using mouse in this plugin doesn't work on old versions
            conf += """
            # it seems mouse events can't use any combination of S-
            set -g @power_zoom_mouse_action "C-DoubleClick3Pane"
            """
        return ["jaclu/tmux-power-zoom", vers_min, conf]

    def plugin_resurrect(self) -> list:  # 1.9
        """Saves & Restores server sessions

        save: <prefix> C-s restore: <prefix> C-r

        Does not work on: iSH

        This plugins fails to restore sessions in iSH, at least on my
        devices. so no point enabling tmux-resurrect & tmux-continuum
        on iSH"""
        if not self.use_plugin_resurrect or mtc_utils.IS_ISH or self.is_tmate():
            min_vers = -1.0  # Dont use
        else:
            min_vers = 1.9

        plugins_dir = self.plugins.get_plugin_dir()
        # go up one and put it beside plugins_dir
        resurect_dir = f"{os.path.dirname(plugins_dir)}/resurrect"

        #
        #  Here is a list of all procs that should be restarted during a resume
        #  For scripts and other stuff running using a path, prefixing with ~
        #  will accept that cmd regardless of what path was used to run it.
        #
        procs = "ash bash zsh sudo bat glow htop man ssh sqlite3 tail watch"
        #
        # man needs to be mentioned twice, since on some systems I use a
        # custom man to view asdf versions of tmux, and this is a script thus
        # using path notation when run.
        #
        procs += " '~adssh->adssh *' '~check-connectivity.sh->check-connectivity.sh *'"
        procs += " '~man->man *' '~uptime-tracker->uptime-tracker *'"
        conf = f"""
        #
        #  Default keys:  save: <prefix> C-s restore: <prefix> C-r
        #
        #  All the process names needs to be added on one long line...
        #  Only long running processes needs to be listed, ie those that
        #  might be running in a pane when the session was saved.
        #
        #  If it is a command triggered by a full path you can refer to it
        #  with a ~ prefix, this will match all commands ending with this
        #  name, regardless of where from it was started.
        #
        set -g @resurrect-processes "{procs}"
        #  Env dependent settings for tmux-plugins/tmux-resurrect
        set -g @resurrect-dir "{resurect_dir}"
        """
        return ["jaclu/tmux-resurrect", min_vers, conf]

    def plugin_session_wizard(self) -> list:  # 3.2
        # default trigger: T
        #
        #  Long startup time on limited hosts...

        if self.use_plugin_session_wizard:
            vers_min = 3.2
        else:
            vers_min = -1.0  # Don't use
        return [
            "27medkamal/tmux-session-wizard",
            vers_min,
            """
            set -g @session-wizard "t"  # trigger
            """,
        ]

    def plugin_suspend(self) -> list:  # 2.4
        """Suspend tmux from receiving any keyboard commands
        This plugin inserts its display on status-right, so no need to
        manually add a placeholder
        Default Trigger: -n M-Z
        """
        if self.use_plugin_suspend:
            min_vers = 2.4
        else:
            # it works on iSH, but soo slow it is of no practical usage
            min_vers = -1.0  # Dont use

        #  {@mode_indicator_custom_prompt}
        return [
            "jaclu/tmux-suspend",
            min_vers,
            """
            set -g @suspend_key  "M-Z"
            set -g @suspend_suspended_options \\
                "@mode_indicator_custom_prompt::#[bg=yellow]💤#[default], "
            """,
        ]

    def plugin_zz_continuum(self) -> list:  # 1.9
        """Automatically save and restore tmux server's open sessions.

        Depends on the plugin tmux-resurrect for actual save/restore.

        Due to a "known issue" mentioned on the plugins GitHub page, this
        plugin method name is intended to make sure this is the last
        plugin defined. Here is this issue:

        In order to be executed periodically, the plugin updates the
        status-right tmux variable. In case some plugin (usually themes)
        overwrites the status-right variable, the autosave feature stops
        working. To fix this issue, place the plugin last in the TPM plugins list.
        """

        if not self.use_plugin_continuum or (
            not self.force_plugin_continuum
            and (self.is_limited_host or self.t2_env or self.is_tmate())
        ):
            vers_min = -1.0  # Don't use
        else:
            vers_min = 1.9

        conf = """
        set -g @continuum-save-interval  15
        set -g @continuum-restore        on
        """
        return ["jaclu/tmux-continuum", vers_min, conf]

    # ==========================================================
    #
    #  Optional pluguins, disablesd by default
    #  Since thye need to be enabled to be used, here there are
    #  no env checks deciding if they will be enabled
    #
    # ==========================================================

    # ----------------------------------------------------------
    #
    #  First plugins only meaningful to run on a local server,
    #  interacting with battery, music players etc
    #
    # ----------------------------------------------------------

    def plugin_battery(self):  # 2.2
        """Forked from: https://github.com/tmux-plugins/tmux-battery

        Only meaningful for local tmux!

        My modifications: all important stats can be displayed by using
        #{battery_smart} in status bar. When plugged in and fully
        charged only the "connected" icon is displayed. If on battery or
        charging the percentage is displayed, and remaining time in
        colors indicating approximately how full the battery is.
        """
        if self.use_plugin_battery:
            #  1.8 accd to orig devel, but i get issues below 2.2
            min_vers = 2.2
        else:
            min_vers = -1.0  # don't use this one

        return [
            "jaclu/tmux-battery",
            min_vers,
            """
            set -g @batt_remain_short true
            """,
        ]

    def plugin_mullvad(self):  # 2.2
        """Display mullvad VPN status
        #{mullvad_city}#{mullvad_country}#{mullvad_status}
        """
        if self.use_plugin_mullvad:
            min_vers = 2.2
        else:
            min_vers = -1.0  # Don't use

        return [
            "jaclu/tmux-mullvad",
            min_vers,
            """
            set -g @mullvad_cache_time ''

            #
            #  I only want to be notified about where the VPN is connected if
            #  not connected to my normal location, typically when avoiding Geo
            #  blocks.
            #  Since this will negatively impact bandwidth and lag, its good to
            #  have a visual reminder.
            #
            # set -g @mullvad_excluded_country 'Netherlands'
            # set -g @mullvad_excluded_city    'Amsterdam'

            #  No colors wanted for disconnected status, just distracting.
            set -g @mullvad_disconnected_bg_color ' '

            #  Since nothing is printed when connected, we don't need to
            #  bother with the colors
            set -g @mullvad_connected_text ' '

            #  When city/country is printed, use comma as separator
            set -g @mullvad_city_suffix ','

            #
            #  Keep separation if items are displayed
            #
            set -g @mullvad_country_no_color_suffix 1
            set -g @mullvad_status_no_color_suffix 1
            """,
        ]

    def plugin_spotify_info(self):  # 1.9
        """Only usable on MacOS!

        Forked from https://github.com/jdxcode/tmux-spotify-info
        My modifications:
        Limited max output length - the default sometimes completely
        filled the status line if one of the reported fields were
        really long

        Display in status-bar with: #(tmux-spotify-info)"""
        if self.use_plugin_spotify_info:
            min_vers = 1.9
        else:
            min_vers = -1.0  # Don't use
        if self.vers_ok(2.9):
            conf = """
            #  Version dependent settings for jaclu/tmux-spotify-info
            """
            conf += "bind -N 'Toggle Spotify' -n MouseDown3StatusRight "
            conf += 'run "spotify pause > /dev/null"'
        else:
            conf = ""
        return ["jaclu/tmux-spotify-info", min_vers, conf]

    # ----------------------------------------------------------
    #
    #  General plugins that makes sense in some conditions
    #
    # ----------------------------------------------------------

    def plugin_1password(self):  # ?.?  local
        """Plugin for 1password CLI tool
        Does not seem to use the status bar"""
        if self.use_plugin_1password:
            min_vers = 1.9  # Unknown min version 1.9 seems ok
        else:
            min_vers = -1.0  # Don't use

        return [
            "yardnsm/tmux-1password",
            min_vers,
            """
                # set -g @1password-key 'u' # default 'u'
                # set -g @1password-account 'acme' # default 'my'
                # set -g @1password-vault 'work' # default '' (all)
                # set -g @1password-copy-to-clipboard 'on' # default 'off'
                # set -g @1password-filter-tags 'development,servers'
                # set -g @1password-debug 'on' # default 'off'
                """,
        ]

    def plugin_gentrify(self) -> list:
        #
        # Sounds kind of interesting, but when tried on 25-05-24 seemed
        # to buggy
        #
        if self.use_plugin_gentrify:
            min_vers = 3.0
        else:
            min_vers = -1.0  # Dont use
        return ["kristopolous/tmux-gentrify", min_vers, ""]

    def plugin_keyboard_type(self):  # 1.9
        """Display in status-bar with:  #{keyboard_type}
        When displaying takes 0.8 s to process...

        Only meaningful for local tmux!
        Tested envs: Darwin, Linux"""
        if self.use_plugin_keyboard_type:
            min_vers = 1.9
        else:
            min_vers = -1.0  # Don't use

        return [
            "jaclu/tmux-keyboard-type",
            min_vers,
            """
            set -g @keyboard_type_hidden  "ABC|U.S.|USInternational-PC"
            set -g @keyboard_type_aliases "Swe=Swedish-Pro|Swe=Swedish|US=U.S."
            set -g @keyboard_type_fg ""
            set -g @keyboard_type_bg "green"
            set -g @keyboard_type_prefix ""
            set -g @keyboard_type_suffix " "
            """,
        ]

    def plugin_packet_loss(self):  # 1.9
        if self.use_plugin_packet_loss:
            min_vers = 1.9
        else:
            min_vers = -1.0  # Don't use
            # 1.1.1.1 - stopped responding 250715
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            set -g @packet-loss-ping_host "8.8.8.8"
            set -g @packet-loss-ping_count     6
            set -g @packet-loss-history_size   6
            set -g @packet-loss-level_alert 18 # 4-26 6-18 7-15

            set -g @packet-loss-weighted_average  yes
            set -g @packet-loss-display_trend     no
            set -g @packet-loss-hist_avg_display  yes
            set -g @packet-loss-run_disconnected  yes

            set -g @packet-loss-level_disp  5

            set -g @packet-loss-level_crit 50

            set -g @packet-loss-color_alert  colour21
            set -g @packet-loss-color_bg     colour226

            set -g @packet-loss-log_file  "$HOME/tmp/tmux-packet-loss.log"

            """,
        ]

    def plugin_which_key(self) -> list:
        """Somewhat similar to tmux-menus, but more limited.

        Doesn't support going back through the menus yet, but with this
        addition to submenus, it can go back, note that the next menu to be
        opened must be named!

            - name: Back
                key: BSpace
                command: 'show-wk-menu #{@wk_menu_panes}'

        Not sure this would work in an inner tmux, outer is capturing key
        in both states. If this is really needed in the inner tmux
        a separate capture key for t2 could be defined"""
        if self.use_plugin_which_key:
            min_vers = 3.0
        else:
            min_vers = -1.0  # Don't use

        return ["alexwforsythe/tmux-which-key", min_vers, ""]

    def plugin_yank(self) -> list:  # 1.8
        """copies text from the command line to the clipboard.
        Default rigger: <prefix> y
        """
        if self.use_plugin_yank:
            min_vers = 1.8
        else:
            min_vers = -1.0  # Don't use

        return [
            "jaclu/tmux-yank",
            min_vers,
            """#  Default trigger: <prefix> y
            # seems to only work on local system
            """,
        ]


if __name__ == "__main__":
    DefaultPlugins().run()
