#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
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
import sys

from base import BaseConfig  # BaseConfig

#
#  Since I often run this on iSH, this class will bind missing keys in the
#  case this is run directly on the ishConsole, in all other cases it will
#  do nothing
#
from mtc_utils import IS_ISH


class DefaultPlugins(BaseConfig):
    """This defines all the plugins I normally use, local only and very
    resource demanding ones are not added here.
    I use this asmy primary base class
    If you never plan to use iSH you can subclass BaseConfig directly
    We use IshConsole as parent, so that the running node is propperly
    configured
    """

    #
    #  Override all other env settings like is_limited_host or is_tmate
    #  and ensure plugin is used
    #
    force_plugin_continuum = False

    #
    #  Default plugins that can be disabled
    #
    use_plugin_mouse_swipe = True
    use_plugin_session_wizard = True

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
        left & right without a pointless reassignment

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
        used_plugins = self.plugins.found(short_name=True)

        #  Consider adding placement for
        #   tmux-1password

        if "tmux-suspend" in used_plugins:
            # pylint: disable=E0203,W0201
            self.sb_right += "#{@mode_indicator_custom_prompt}"

        if "tmux-mullvad" in used_plugins:
            # pylint: disable=E1101
            self.sb_left += "#{mullvad_city}#{mullvad_country}"
            self.sb_left += "#{mullvad_status}"

        if "tmux-nordvpn" in used_plugins:
            # pylint: disable=E1101
            self.sb_left += "#{nordvpn_country}#{nordvpn_status}"

        if "tmux-keyboard-type" in used_plugins:
            # pylint: disable=W0201
            self.sb_right = "#{keyboard_type}" + self.sb_right

        if "tmux-battery" in used_plugins:
            # pylint: disable=W0201
            self.sb_right = "#{battery_smart} " + self.sb_right

        if "tmux-spotify-info" in used_plugins:
            # pylint: disable=W0201
            self.sb_right = (
                "#[bg=colour28]#(tmux-spotify-info)#[default] " + self.sb_right
            )

        if "tmux-packet-loss" in used_plugins:
            # pylint: disable=W0201
            self.sb_right = "#{packet_loss}" + self.sb_right

        return True  # request footer to be printed

    # ===========================================================
    #
    #  Common Plugins that I would typically use on any system.
    #
    #  Any method starting with plugin_ will be assumed to be a plugin
    #  definition, and handled as such by the TmuxConfig class.
    #  If not in one of the parent classes, just changing the name to something
    #  like not_plugin_menus() is enough to ensure it is not used.
    #
    #  Plugins will be ordered alphabetically based on method name.
    #  In my case I want sensible to come first and continuum to come last.
    #  So I have adjusted the method names accordingly. Normally the order
    #  does not matter at all.
    #  The name has no significance for the resulting tmux.conf, it just has to
    #  start with plugin_ in order to be treated as such.
    #
    #  In the rare case disabling a plugin is needed on some systems,
    #  In my case that is on iSH, so limited that some of these even if
    #  normally considered harmless, would cause excessive load on such systems
    #
    #  One way is to subclass that method and set an absurd version
    #  requirement, like '999.0'
    #
    #  Since such a plugin will never be used, this instance does not need any
    #  meaningful content, here is an example:
    #
    #  def plugin_packet_loss(self):  # 999.9 to disable it from base class
    #      #
    #      #  Dummy to override base class instance
    #      #
    #      return ['999.9', '', '']
    #
    #  Since it is defined in a parent class, prefixing it with not_ or similar
    #  in the subclass will not have any effect.
    #
    #  Syntax for plugins:
    #
    #  The method should return a triplet:
    #     min_version,
    #     plugin name - needed when installing it, and to identify it.
    #     code snippet defining plugin variables
    #
    #  The plugins are handled in a two step process.
    #  First by gather_active_plugins() early on during init, when it is run
    #  writing is disabled so nothing will be outputed to the tmux.conf.
    #  This will create self.used_plugins a sorted list of all plugins
    #  matching the current tmux version. This can be used by the config class
    #  if so needed, since thus it will be aware of what plugins will be used.
    #
    #  On the second run, only plugins matching the current tmux will be
    #  processed. During this run, any code before the return will be
    #  processed and it can write to the tmux.conf.
    #
    #  Normally plugin related code should come as the last triplet of
    #  the return, but since they are just inserted, if version or other checks
    #  needs to be done, write them before the return.
    #  Look at plugin_zz_continuum() below for an example.
    #
    #  Since tpm can only be used starting at 1.9, a min_vers of 0.0
    #  means min version not stated by developer, but it works at 1.9
    #  I havent bothered checking further back :)
    #
    #
    # -----------------------------------------------------------

    def plugin_better_mouse_mode(self) -> list:  # [str | float | int]:  # 2.1
        #
        #  A tmux plugin to better manage the mouse.
        #  Emulate mouse scrolling for full-screen programs that doesn't
        #  provide built in mouse support, such as man, less, vi.
        #  Can scroll in non-active 'mouse over-ed' panes.
        #  Can adjust scroll-sensitivity.
        #
        if self.t2_env or self.is_tmate():
            vers_min = 99.0  # make sure this is never used
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

    #
    #  wont work in an inner tmux, outer is capturing key
    #  in both states. If this is really needed in the inner tmux
    #  a separate capture key for t2 could be defined
    #
    # def plugin_which_key(self) -> list:
    #     return ['alexwforsythe/tmux-which-key', 3.0, ""]

    def plugin_menus(self) -> list:  # 0.0
        conf = """
        set -g @menus_log_file ~/tmp/tmux-menus.log
        # set -g @menus_use_cache no
        """
        #  Tested down to vers 1.7
        return ["jaclu/tmux-menus", 0.0, conf]

    def plugin_mouse_swipe(self) -> list:  # 3.0
        #
        #  right-click & swipe switches Windows / Sessions
        #
        if not self.use_plugin_mouse_swipe or (self.t2_env or self.is_limited_host):
            min_vers = 99.0  # dont use this one
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
        #
        #   Zooms to separate Window, to allow for adding support panes
        #
        if self.is_tmate():
            print("><> plugin_power_zoom thinks this is tmate")
            vers_min = 99.0
        else:
            vers_min = 2.0

        return [
            "jaclu/tmux-power-zoom",
            vers_min,
            """
            set -g @power_zoom_trigger  Z
            set -g @power_zoom_mouse_action "S-DoubleClick3Pane"
            """,
        ]

    def plugin_resurrect(self) -> list:  # 1.9
        #
        #  Saves & Restores server sessions
        #
        #  save: <prefix> C-s restore: <prefix> C-r
        #
        #  Does not work on: iSH
        #
        #  This plugins fails to restore sessions in iSH, at least on my
        #  devices. so no point enabling tmux-resurrect & tmux-continuum
        #  on iSH
        #
        if IS_ISH or self.is_tmate():
            return ["tmux-plugins/tmux-resurrect", 99, ""]

        plugins_dir = self.plugins.get_plugin_dir()
        # go up one and put it beside plugins_dir
        resurect_dir = f"{os.path.dirname(plugins_dir)}/resurrect"

        procs = "zsh bash ash ssh sudo top htop watch psql mysql sqlite sqlite3 "
        procs += "glow bat batcat"

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
        #  Line continuation without passing col 80 here
        # conf += "mysql glow sqlite sqlite3 top htop  ~packet_loss "
        # conf += "~common_pull ~sysload_tracker ~Mbrew ~Mapt'\n"

        return ["jaclu/tmux-resurrect", 1.9, conf]

    def plugin_session_wizard(self) -> list:  # 3.2
        if not self.use_plugin_session_wizard or (
            self.is_limited_host or self.is_termux
        ):
            vers_min = 99.0  # make sure this is never used
        else:
            vers_min = 3.2

        return [
            "27medkamal/tmux-session-wizard",
            vers_min,
            "#  Default trigger: <prefix> T",
        ]

    def plugin_suspend(self) -> list:  # 2.4  - status_bar_customization
        #
        #  {@mode_indicator_custom_prompt}
        #
        #  I use this mostly in order to be able to send root keys
        #  into an inner T2_ENV
        #
        #  Since this key will active in the outer tmux in order to reenable
        #  the only way to use this in an inner tmux is if the inner is using
        #  a different trigger key.
        #
        #  Can't use M-Z since ish_console is not able to generate that
        #  directly
        #
        return [
            "jaclu/tmux-suspend",
            2.4,
            """
            set -g @suspend_key  M-Z
            """
            "set -g @suspend_suspended_options "
            '"@mode_indicator_custom_prompt::#[bg=yellow]💤#[default], "\n',
        ]

    def plugin_zz_continuum(self) -> list:  # 1.9
        #
        #  Auto restoring a session just as tmux starts on a limited
        #  host will just lead to painfull lag.
        #
        #  It is also not desired on inner tmux sessions. They are
        #  typically for testing purposes, being able to manually restore
        #  a session makes sense, but auto-resuming does not.
        #
        if not self.force_plugin_continuum and (
            self.is_limited_host or self.t2_env or self.is_tmate()
        ):
            vers_min = 99.0  # make sure this is never used
        else:
            vers_min = 1.9
        #
        #  Automatically save and restore tmux server's open sessions.
        #
        #   Saves every 15 mins (default) Restores last save when tmux is
        #   starting
        #
        #  Depends on tmux-resurrect for actual save/restore.
        #
        #  In the below switch-statement I set the variables even if the
        #  values are defaults, since when re-running the config after
        #  changing this,
        #  If a variable is unset in the new state, the already set value
        #  will still be in effect. - Boy did that bite me...
        #
        #  2020-12-24
        #  ==========
        #  Due to a bug tmux-continuum should be as close to last plugin
        #  as possible to minimize the risk of a crucial tmux variable
        # `status-right` is not overwritten (usually by theme plugins).
        #
        conf = """
        set -g @continuum-save-interval  15
        set -g @continuum-restore        on
        """
        return ["jaclu/tmux-continuum", vers_min, conf]


class OptionalPlugins(BaseConfig):

    #
    #  Optional plugins, need to be enabled
    #
    use_plugin_1password = False
    use_plugin_battery = False
    use_plugin_jump = False
    use_plugin_keyboard_type = False
    use_plugin_mullvad = False
    use_use_plugin_nordvpn = False
    use_plugin_packet_loss = False
    use_plugin_spotify = False
    use_plugin_plugin_yank = False

    def plugin_1password(self):  # ?.?  local
        #
        #  Plugin for 1password CLI tool op
        #
        if not self.use_plugin_1password:
            min_vers = 99.0  # dont use this one
        else:
            min_vers = 0.0  # Unknown min version
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

    def plugin_battery(self):  # 2.2 - localstatus_bar_customization
        #
        #  #{battery_smart} takes < 5s ATM
        #
        #  Only meaningful for local tmux!
        #
        #  Forked from: https://github.com/tmux-plugins/tmux-battery
        #
        #  My modifications: all important stats can be displayed by using
        #  #{battery_smart} in status bar. When plugged in and fully
        #  charged only the "connected" icon is displayed. If on battery or
        #  charging the percentage is displayed, and remaining time in
        #  colors indicating approximately how full the battery is.
        #
        #  #{battery_smart}
        #
        if not self.use_plugin_battery or self.is_tmate():
            min_vers = 99.0  # dont use this one
        else:
            #  1.8 accd to orig devel, but i get issues below 2.2
            min_vers = 2.2
        return [
            "jaclu/tmux-battery",
            min_vers,
            """
            set -g @batt_remain_short 'true'
            """,
        ]

    def plugin_jump(self) -> list:  # 1.8
        #
        #  Jump to word(-s) on the screen that you want to copy,
        #  without having to use the mouse.
        #
        #
        #  Default trigger: <prefix> j
        #
        if not self.use_plugin_jump or (
            self.t2_env or self.is_limited_host or self.is_tmate()
        ):
            min_vers = 99.0  # dont use this one
        else:
            min_vers = 1.8
        return [
            "jaclu/tmux-jump",  # was Lenbok
            min_vers,
            #
            #  The weird jump key syntax below is how I both sneak in
            #  a note and make the key not to depend on prefix :)
            #
            """#  Additional dependency: ruby >= 2.3
            set -g @jump-key "-N plugin_Lenbok/tmux-jump -n  M-j"
            set -g @jump-keys-position 'off_left'
            """,
        ]

    def plugin_keyboard_type(self):  # 1.9 - localstatus_bar_customization
        #
        #  When displaying takes 0.8 s to process...
        #
        #  Only meaningful for local tmux!
        #   Tested envs: Darwin, Linux
        #
        #  Display in status-bar with:  #{keyboard_type}
        #
        if not self.use_plugin_keyboard_type:
            min_vers = 99.0  # dont use this one
        else:
            min_vers = 1.9
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

    def plugin_mullvad(self):  # 2.2  - localstatus_bar_customization
        #
        #   #{mullvad_city}#{mullvad_country}#{mullvad_status}
        #
        if not self.use_plugin_mullvad or self.is_tmate():
            min_vers = 99.0  # dont use this one
        else:
            min_vers = 2.2

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

    def plugin_nordvpn(self):  # - localstatus_bar_customization
        if not self.use_use_plugin_nordvpn:
            min_vers = 99.0  # dont use this one
        else:
            min_vers = 0.0  # Not sure of its min version

        return [
            "maxrodrigo/tmux-nordvpn",
            min_vers,
            """
        set -g @nordvpn_connected_text=""
        set -g @nordvpn_connecting_text="🔒"
        set -g @nordvpn_disconnected_text="🔓"
        """,
        ]

    def plugin_packet_loss(self):  # 1.9 - localstatus_bar_customization
        if not self.use_plugin_packet_loss or self.is_tmate():
            min_vers = 99.0  # dont use this one
        else:
            min_vers = 1.9

        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            set -g @packet-loss-ping_host 1.1.1.1
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

            set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss.log

            """,
        ]

    def plugin_spotify(self):  # 1.8 - localstatus_bar_customization
        #
        #  Ensure this is only used on MacOS
        #
        #
        name = "jaclu/tmux-spotify-info"
        if sys.platform == "darwin" and self.use_plugin_spotify and not self.is_tmate():
            min_vers = 1.8
        else:
            min_vers = 99.0
            name = name + "-requires-MacOS"
        #
        #  Only meaningful for local tmux!     Only works on MacOS
        #
        #  Forked from https://github.com/jdxcode/tmux-spotify-info
        #  My modifications:
        #   Limited max output length - the default sometimes completely
        #   filled the status line if one of the reported fields were
        #   really long
        #
        #  Display in status-bar with: #(tmux-spotify-info)
        #
        if self.vers_ok(2.9):
            conf = """
            #  Version dependent settings for jaclu/tmux-spotify-info
            """
            conf += "bind -N 'Toggle Spotify' -n MouseDown3StatusRight "
            conf += 'run "spotify pause > /dev/null"'
        else:
            conf = ""
        return [name, min_vers, conf]

    def plugin_yank(self) -> list:  # 1.8
        #
        #  copies text from the command line to the clipboard.
        #
        if not self.use_plugin_plugin_yank or (self.is_limited_host or self.is_tmate()):
            min_vers = 99.0  # dont use this one
        else:
            min_vers = 1.8
        return [
            "jaclu/tmux-yank",
            min_vers,
            """#  Default trigger: <prefix> y
            # seems to only work on local system
            """,
        ]


if __name__ == "__main__":
    DefaultPlugins().run()
