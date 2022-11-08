#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
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

import os

#
#  Since I often run this on iSH, this class will bind missing keys in the case
#  this is run directly on the ishConsole, in all other cases it will do nothing
#
from ish_console import IshConsole


class DefaultPlugins(IshConsole):
    """This defines all the plugins I normally use, local only and very
    resource demanding ones are not added here.
    I use this as my primary base class
    If you never plan to use iSH you can subclass BaseConfig directly
    """

    #
    #  Don't do auto-resume session in t2_env
    #  Manual reload with <prefix> C-R is still available
    #  if tmux-plugins/tmux-resurrect is installed
    #
    do_continuum = not os.environ.get("T2_ENV")

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """This is called just before the status bar is rendered,
        local_overides() is called later so can not modify status bar
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

        #
        #  Plugin-hooks for status-bar, enable an item if that plugin is used
        #
        used_plugins = self.plugins.found(short_name=True)
        if "tmux-prefix-highlight" in used_plugins:
            self.sb_right += "#{prefix_highlight}"

        if "tmux-packet-loss" in used_plugins:
            self.sb_right = "#{packet_loss}" + self.sb_right

        if "tmux-suspend" in used_plugins:
            self.sb_right += "#{@mode_indicator_custom_prompt}"

        if "tmux-mullvad" in used_plugins:
            self.sb_left += "#{mullvad_city}#{mullvad_country}#{mullvad_status}"

        if "tmux-keyboard-type" in used_plugins:
            self.sb_right = "#{keyboard_type}" + self.sb_right

        if "tmux-battery" in used_plugins:
            self.sb_right = "#{battery_smart} " + self.sb_right

        if "tmux-spotify-info" in used_plugins:
            self.sb_right = (
                "#[bg=colour28]#(tmux-spotify-info)#[default] " f"{self.sb_right}"
            )

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

    def plugin_prefix_highlight(self):  # 0.0
        #
        #  Highlights when you press tmux prefix key and
        #  when copy/sync mode is active.
        #
        conf = """
        set -g @prefix_highlight_show_copy_mode  on
        set -g @prefix_highlight_copy_mode_attr  "fg=black,bg=yellow,bold"
        set -g @prefix_highlight_show_sync_mode  on
        set -g @prefix_highlight_sync_mode_attr "fg=black,bg=orange,blink,bold"
        """
        return ["jaclu/tmux-prefix-highlight", 0.0, conf]

    def plugin_menus(self):  # 3.0
        conf = "set -g @menus_config_overrides  1"
        #
        #  Popup menus that can be helpful default trigger:  <prefix> \
        #
        #  menu_locations:
        #
        #  W - By the current window name in the status line (default)
        #  P - Lower left of current pane
        #  C - Centered in window (tmux 3.2 and up)
        #  M - Mouse position
        #  R - Right edge of terminal (Only for x)
        #  S - Next to status line (Only for y)
        #  Number - In window coordinates 0,0 is top left of screen
        #
        if self.vers_ok(3.2):
            conf += """
            #  Version dependent settings for jaclu/tmux-menus
            set -g @menus_location_x  C
            set -g @menus_location_y  C
            """
        return ["jaclu/tmux-menus", 3.0, conf]

    def plugin_mouse_swipe(self):  # 3.0
        #
        #  right-click & swipe switches Windows / Sessions
        #
        if self.is_limited_host:
            vers_min = 99  # make sure this is never used
        else:
            vers_min = 3.0
        return [
            "jaclu/tmux-mouse-swipe",
            vers_min,
            """
            #  right-click & swipe switches Windows / Sessions
            """,
        ]

    def plugin_power_zoom(self):  # 2.6
        #
        #   Zooms to separate Window, to allow for adding support panes
        #
        if self.is_limited_host or self.is_tmate():
            # make sure this is never used on a host flagged as limited
            vers_min = 99
        else:
            vers_min = 2.0

        return [
            "jaclu/tmux-power-zoom",
            vers_min,
            """
            set -g @power_zoom_trigger  Z
            set -g @power_zoom_mouse_action "S-DoubleClick3Pane"
            #  Obsolete param, should no longer be used!
            # set -g @power_zoom_mouse yes
            """,
        ]

    def plugin_suspend(self):  # 2.4
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
            "MunifTanjim/tmux-suspend",
            2.4,
            """
            set -g @suspend_key  M-z
            """
            "set -g @suspend_suspended_options "
            '"@mode_indicator_custom_prompt::#[bg=yellow]💤#[default], "\n',
        ]

    def plugin_better_mouse_mode(self):  # 2.1
        #
        #  A tmux plugin to better manage the mouse.
        #  Emulate mouse scrolling for full-screen programs that doesn't
        #  provide built in mouse support, such as man, less, vi.
        #  Can scroll in non-active 'mouse over-ed' panes.
        #  Can adjust scroll-sensitivity.
        #
        min_vers = 2.1
        if self.is_tmate():
            min_vers = 99
        return [
            "jaclu/tmux-better-mouse-mode",
            min_vers,
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

    def plugin_session_wizard(self):  # 3.2
        return ["27medkamal/tmux-session-wizard", 3.2, "#  Default trigger: <prefix> T"]

    def plugin_jump(self):  # 1.8
        #
        #  Jump to word(-s) on the screen that you want to copy,
        #  without having to use the mouse.
        #
        #
        #  Default trigger: <prefix> j
        #
        k = "-n  M-j"
        if self.is_limited_host or self.is_tmate():
            # make sure this is never used, generates to much lag
            vers_min = 99
            self.write(
                f"bind -N 'tmux-jump'  {k}  display "
                "'tmux-jump disabled on limited hosts'"
            )
        else:
            vers_min = 1.8
        return [
            "jaclu/tmux-jump",  # was Lenbok
            vers_min,
            #
            #  The weird jump key syntax below is how I both sneak in
            #  a note and make the key not to depend on prefix :)
            #
            f"""#  Additional dependency: ruby >= 2.3
            set -g @jump-key "-N plugin_Lenbok/tmux-jump {k}"
            set -g @jump-keys-position 'off_left'
            """,
        ]

    def plugin_yank(self):  # 1.5
        #
        #  copies text from the command line to the clipboard.
        #
        if self.is_tmate():
            min_vers = 99
        else:
            min_vers = 1.5
        return [
            "jaclu/tmux-yank",
            min_vers,
            """#  Default trigger: <prefix> y
            # seems to only work on local system
            """,
        ]

    def plugin_resurrect(self):  # 1.9
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
        if self.is_limited_host or self.is_tmate():
            return ["tmux-plugins/tmux-resurrect", 99, ""]

        conf = """
        #
        #  Default keys:  save: <prefix> C-s restore: <prefix> C-r
        #
        #  All the process names needs to be added on one long line...
        #  If it is a command triggered by a full path you can refer to it
        #  with a ~ prefix, this will match all commands ending with this
        #  name, regardless of where from it was started.
        #
        set -g @resurrect-processes 'zsh ash ssh sudo watch psql """

        #  Line continuation without passing col 80 here
        conf += "mysql glow sqlite sqlite3 top htop  ~packet_loss "
        conf += "~common_pull ~sysload_tracker ~Mbrew ~Mapt'\n"

        plugins_dir = self.plugins.get_deploy_dir()
        # go up one and put it beside plugins_dir
        resurect_dir = f"{os.path.dirname(plugins_dir)}/resurrect"
        conf += f"""
        #  Env dependent settings for tmux-plugins/tmux-resurrect
        set -g @resurrect-dir "{resurect_dir}"
        """
        return ["jaclu/tmux-resurrect", 1.9, conf]

    def plugin_zz_continuum(self):  # 1.9
        #
        #  Auto restoring a session just as tmux starts on a limited
        #  host will just lead to painfull lag.
        #
        #  It is also not desired on inner tmux sessions. They are
        #  typically for testing purposes, being able to manually restore
        #  a session makes sense, but auto-resuming does not.
        #
        if self.is_limited_host or self.t2_env or self.is_tmate():
            vers_min = 99  # make sure this is never used
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
        conf = "#  Parameter dependent settings for tmux-plugins/tmux-continuum"
        if self.do_continuum:
            conf += """
            set -g @continuum-restore        on
            set -g @continuum-save-interval  15"""
        else:
            conf += """
            set -g @continuum-restore        off
            set -g @continuum-save-interval  15"""
        return ["jaclu/tmux-continuum", vers_min, conf]


if __name__ == "__main__":
    DefaultPlugins().run()
