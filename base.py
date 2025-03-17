#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Since I use this on older tmux versions, I can't use line continuation
#  when writing to the config file.
#  Some of the lines in the resulting tmux.conf will be really long...
#
#  The generated config is not really meant to be used as a primary
#  sourceof the setup it will include group headers and some comments
#  suck in from here, but this is the canonical place to observe the
#  code.
#
#  Admittedly the level of version checking done here is way beyond what
#  would be needed in any normal case. Since I often try to make plugins
#  as backwards compatible as possible, it was convenient to also have
#  a setup that can run on any available tmux version.
#  This is tested to work without issues all the way back to version 0.8
#
#  Alternate session
#  -----------------
#  If the env variable T2_ENV is set this will generate an "alternate"
#  tmux session, clearly indicated with 'ALT CONF' in the status line
#  and using green pane borders, to make it easier to spot if a pane is
#  part of the primary or alternate session.
#
#  The alternate session has its own plugin directory if jaclu/tpm is used
#
#  Custom exit codes are defined in mtc_utils.ERROR_
#  Those print customized error messages, so myt can just exit without
#  printing it's own error message.
#
#  In the case of ERROR_INCOMPATIBLE_TMUX_CONF_LIB
#    myt will attempt to recreate the venv (if used)
#

# pylint: disable=C0116,C0302


"""base class used by tpm"""

import os
import re
import sys

import __main__

# pylint: disable=import-error
# pyright: reportMissingImports=false
from tmux_conf import TmuxConfig

import mtc_utils
from tablet_kbd import special_consoles_config

# ruff checks might be relevant F403,F401

TMUX_CONF_NEEDED = "0.20.0"


# https://youtu.be/yFLY0SVutgM?si=VoKETDw39BAUHfST&t=420
# class Environment(StrEnum):
#     normal = "normal"
#     t2 = "t2"


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class BaseConfig(TmuxConfig):
    """Defines the general tmux setup, key binds etc

    Groupings of user-keys

    <200 used here
    180 Used for generating Euro sign

    200-499 tablet_kbd.py
    """

    prefix_key: str = "C-a"

    status_interval: int = 5  # How often the status bar should be updated

    monitor_activity: bool = False  # Notification when other windows change state

    show_pane_title: bool = True  # If enabled, Set title with <P> P
    show_pane_size: bool = True  # If enabled pane frame lines will display pane size

    #
    #  This causes most colors on MacOS Term.app to fail
    #
    use_24bit_color: bool = os.environ.get("TERM_PROGRAM") != "Apple_Terminal"
    #
    #  Tc is more commonly supported by terminals
    #  RGB may provide more accurate color representation
    #  If running tmux < 2.7, this will be overridden into Tc, since
    #  RGB was not supported in older tmux'es
    #
    color_tag_24bit: str = "RGB"

    #
    #  Default templates for the status bar, so that they can easily be
    #  modified using status_bar_customization()
    #
    sb_left: str = "|#{session_name}| "
    sb_right: str = "%a %h-%d %H:%MUSERNAME_TEMPLATEHOSTNAME_TEMPLATE"
    username_template: str = " #[fg=colour1,bg=colour195]#(whoami)#[default]"
    hostname_template: str = f"#[fg=colour195,bg=colour1]{mtc_utils.HOSTNAME}#[default]"
    tpm_initializing: str = "#[reverse,blink] tpm initializing...#[default]"

    handle_iterm2: bool = True  # Select screen-256color for iTerm2

    #
    #  Indicates this is a separate tmux env, I use it for testing
    #  plugin compatibility, and changed settings in a way that does not
    #  interfere with my main environment
    #
    t2_env: str = os.environ.get("T2_ENV", "")
    prefix_key_T2: str = "C-w"  # prefix for inner dev environment

    # Disables tmux default popup menus, instead relying on the plugin
    # jaclu/tmux-menus
    skip_default_popups: bool = True

    plugin_handler = "jaclu/tpm"  # overrides of tmux-conf package default

    #
    #  Some devices are unable to generate the nav keys - PageUp, PageDown, Home, and End
    #
    #  Tablet keyboards typically lack dedicated navigation keys such as PageUp,
    #  PageDown, Home, and End. Additionally, iSH only supports unmodified
    #  arrow keys (without Ctrl, Shift, or Alt).
    #  To compensate for this limitation, enabling this setting allows the
    #  <prefix> + arrow keys to function as navigation keys within tmux
    #  when running from the console on such devices, either locally or remotely.
    #  If logged in remotely into such a device, it will not be needed
    #
    #  This feature only activates when the terminal is detected as a limited
    #  device console.
    #
    #  In all other terminals,  the arrow keys and pane navigation remain
    #  unchanged.
    #
    #  Note: Enabling this will reassign tmux pane navigation to use
    #  Vim-style keybindings (<prefix> + h/j/k/l) by default,
    #  which may require adjustment if you're used to using the arrow keys
    #  for pane navigation.
    #
    use_prefix_arrow_nav_keys = False

    # use_debug_log = True  # if True, debug log will be printed

    # pylint: disable=too-many-positional-arguments,too-many-arguments
    def __init__(
        self,
        parse_cmd_line: bool = True,
        #
        #  if parse_cmd_line is True all other params are ignored
        #
        conf_file: str = "~/.tmux.conf",  # where to store conf file
        tmux_bin: str = "",
        tmux_version: str = "",
        replace_config: bool = False,  # replace config with no prompt
        clear_plugins: bool = False,  # remove all current plugins
        plugins_display: int = 0,  # Display info about plugins
        # environment: Environment = Environment.normal,
    ) -> None:
        # Indicates if this tmux is run on the iSH console

        self.style = None
        self.check_libs_compatible()
        super().__init__(
            parse_cmd_line=parse_cmd_line,
            conf_file=conf_file,
            tmux_bin=tmux_bin,
            tmux_version=tmux_version,
            replace_config=replace_config,
            clear_plugins=clear_plugins,
            plugins_display=plugins_display,
        )

        self.tablet_keyb = None
        self.default_m_underscore = "M-_"
        self.muc_keys = {
            # Kbd binds that might need to be replaced by user-keys on nonstandard
            # consoles
            "M_plus": "M-+",
            "M_par_open": "M-(",
            "M_par_close": "M-)",
            "M_underscore": self.default_m_underscore,
            "M_P": "M-P",
            "M_X": "M-X",
            "C_M_h": "C-M-h",
            "C_M_j": "C-M-j",
            "C_M_k": "C-M-k",
            "C_M_l": "C-M-l",
        }
        self.define_opt_params()

        if self.vers_ok(1.8):
            self.shell_bg = "run-shell -b"
        else:
            # option -b was introduced in 1.8, this filters out usages on unsitable
            # versions, since if used, will trigger sometimes hard to trace hangs
            self.shell_bg = (
                "\n#================================\n"
                "#   ERROR - broken code disabled!\n"
                "#================================\n"
                "# This usage of run-shell -b would likely "
                "cause a hang on tmux < 1.8\n# "
            )
        if self.vers_ok(1.9):
            # the syntax can be used in 1.8, but if used path is always set to /
            self.current_path_directive = "-c '#{pane_current_path}'"
        else:
            self.current_path_directive = ""

        #
        #  If tpm is used, this is set once tpm has completed
        #  initialization, this is used to avoid displaying
        #  tpm initializing in the statusbar if config is sourced etc
        #
        self.tpm_working_incicator = "@tpm-is-active"

        if self.is_tmate() and (self.show_pane_title or self.show_pane_size):
            print("show_pane_title & show_pane_size disabled for tmate")
            self.show_pane_size = self.show_pane_title = False

        if self.t2_env:
            if self.conf_file == os.path.expanduser("~/.tmux.conf"):
                print()
                print("ERROR: T2_ENV & ~/.tmux.conf can't be combined!")
                sys.exit(mtc_utils.ERROR_T2_USING_DEF_TMUX_CONF)
            conf_dir = os.path.dirname(self.conf_file)
            self.tpm_location = os.path.join(conf_dir, "plugins", "tpm")
            self.prefix_key = self.prefix_key_T2
            print(f"T2_ENV uses prefix_key: {self.prefix_key}")

        if mtc_utils.IS_ISH or mtc_utils.HOSTNAME == "ish-hetz1":
            print("Detected iSH kernel, assuming this to be a limited host")
            self.is_limited_host = True

        #  to avoid typos I use constants for script names
        self._fnc_shlvl_offset = "shlvl_offset"
        self._fnc_list_plugins = "list_plugins"
        self._fnc_toggle_mouse = "toggle_mouse"
        self._fnc_activate_tpm = "activate_tpm"
        self._fnc_tpm_indicator = "tpm_init_indicator"

    def edit_config(self, edit_key: str = "e") -> None:
        pass  # Im not really using it, so skip it

    def assign_style(self, style_name) -> None:
        """Use this to name the style being used, and to ensure that
        multiple styles are not unintentionally assigned.
        """
        this_style = os.path.splitext(os.path.basename(style_name))[0]
        if self.style:
            # return  # error_disabled
            # used to prevent if multiple styles are inherited and colliding
            print()
            print(
                f"ERROR: Style already assigned as: {self.style}, "
                f"Can not use style: {this_style}"
            )
            sys.exit(mtc_utils.ERROR_STYLE_REDEFINED)
        self.style = this_style
        print(f"Style used is: >> {self.style} <<")

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """This is called just before the status bar is rendered,
        local_overides() is called later so that can not modify status bar
        left & right without a pointless reassignment.

        I use this to modify status bar colors in subclasses
        add hooks for plugins that are currently used.

        I have come to realize that leaving them in for non active
        plugins is not desired. If the plugin code is present in
        ~/.tmux/plugins, even if not used, status bar actions are
        happening.
        If it is not intended to be used, errors might be triggered.

        If print_header=True is propagated to the BaseCofig instance,
        it will print a header in the resulting config file.
        If this method returns True a footer will be printed.
        """
        w = self.write
        if print_header:
            w(
                """
            #
            #   ======   status_bar_customization()   ======
            #"""
            )

        return print_header

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
        w = self.write
        #  Display what class this override comes from
        w("# ---  BaseConfig.local_overides()")

        if not self.tablet_keyb:
            # Tablet keyb configs handle their own euro rempaping
            eur_sequence = "\\033\\100"  # Dawin keyboards, is pc different?
            self.euro_fix(eur_sequence)
        w()  # Spacer after this local override section

    def content(self) -> None:
        """This generates the majority of the tmux.conf.

        Plugins can be handled by plugin_foo() methods, but its
        perfectly fine to just include such code here if that is your
        preference.

        In my setup I try to always be backwards compatible in the sense
        that if I bind something to a meta key, I try to also make it
        available via prefix, in order to still be accessible on dumb
        terminals.
        """
        self.tablet_keyb = special_consoles_config(self)
        self.remove_unwanted_default_bindings()
        self.connecting_terminal()
        self.general_environment()
        self.session_handling()
        self.windows_handling()
        self.pane_handling()
        if self.vers_ok(1.0):
            self.mouse_handling()
        self.status_bar()

        self.__base_overrides()

    def __base_overrides(self) -> None:
        """This should be at the very end of content subclasses
        should not change this one!"""

        if self.plugin_handler and self.plugin_handler != "manual":
            #
            #  Override default script ftom tmux-conf.plugins in order
            #  to indicate tpm is done
            #
            self.mkscript_tpm_deploy()

            if self.vers_ok(2.1):
                #
                #  Script that when called removes tpm init from SB
                #
                self.mkscript_tpm_indicator()

        #     self.write(
        #         f"""
        # #======================================================
        # #
        # #   Base class overrides
        # #
        # #======================================================

        #     """
        #     )

    #
    #  content methods broken up in parts, by content
    #
    def remove_unwanted_default_bindings(self):
        w = self.write
        w(
            """
        #======================================================
        #
        #   Remove unwanted default bindings
        #
        #======================================================
        """
        )
        if self.vers_ok(1.1):
            w(
                """#
                #  Chooses next layout, potentially ruining a carefully crafted one.
                #  I can't really see any purpose with this one. You can access
                #  the layouts directly using <prefix> M-[1-5],
                #  so the safe bet is to disable
                #
                unbind  Space    #  Select next layout"""
            )
        if self.skip_default_popups and self.vers_ok(3.0):
            w(
                """
                #
                #  Remove the default popup menus"""
            )
            if "tmux-menus" in self.plugins.installed(short_name=True):
                w("#  Instead using the plugin jaclu/tmux-menus - <prefix> \\")
            w("#")
            if self.vers_ok(3.0):
                w(
                    """unbind  -n  MouseDown3Pane
                    unbind  -n  MouseDown3Status
                    unbind  -n  MouseDown3StatusLeft
                    unbind  -n  M-MouseDown3Pane"""
                )
                if not self.vers_ok(3.1):
                    w("unbind  -n  MouseDown3StatusRight")
            if self.vers_ok("3.0a"):
                w(
                    """unbind  <
                    unbind  >"""
                )
            if self.vers_ok(3.4):
                w(
                    """unbind  -n  M-MouseDown3Status
                    unbind  -n  M-MouseDown3StatusLeft"""
                )
        w()  # spacer

    def connecting_terminal(self):  # cmd: 2 + optional
        w = self.write
        w(
            """
        #======================================================
        #
        #   Connecting terminal
        #
        #======================================================
        """
        )

        #
        #  If LC_TERMINAL is not passed through, add this to the servers
        #  /etc/ssh/sshd_config:
        #
        # # Allow client to pass locale environment variables
        # AcceptEnv LANG LC_*
        #
        if self.vers_ok(1.0):
            if self.handle_iterm2 and os.getenv("LC_TERMINAL") == "iTerm2":
                w(f"{self.opt_server} default-terminal screen-256color")
            else:
                w(f"{self.opt_server} default-terminal tmux-256color")

        #
        #  Making OSC 52 work on mosh connections.
        #  For this to work the term name used must match, hence * :)
        #  from: https://gist.github.com/yudai/95b20e3da66df1b066531997f982b57b
        #
        if self.vers_ok(1.0) and not os.getenv("TMUX_NO_CLIPBOARD"):
            w(
                f"""
            # Ms modifies OSC52 clipboard handling to work with mosh
            {self.opt_server} -a terminal-overrides ",*:Ms=\\\\E]52;c%p1%.0s;%p2%s\\\\7"
            """
            )

        if self.vers_ok(1.9):
            #  Enable focus events for terminals that support them to be passed
            #  through to applications running inside tmux.
            w(f"{self.opt_server} focus-events on")

        if self.vers_ok(3.2):
            w(f"{self.opt_server} extended-keys on")

        #
        #  For old tmux versions, this is needed to support modifiers for
        #  function keys
        #
        #    https://github.com/tmux/tmux/wiki/Modifier-Keys#modifiers-and-function-keys
        #
        if not self.vers_ok(2.4):
            w(f"{self.opt_win} xterm-keys on")

        #
        #  Support for CSI u  extended keys
        #
        #    https://github.com/tmux/tmux/wiki/Modifier-Keys#extended-keys
        #
        #  Some apps like iTerm2 don't need it, but it never hurts
        #
        if self.use_24bit_color:
            if self.vers_ok(3.2):
                #
                #  not needed for all terminal apps, but since it doesn't hurt,
                #  it makes sense to always include it
                #
                w(f"{self.opt_server} -a terminal-features 'xterm*:extkeys'")
                w(f'{self.opt_server} -a terminal-features ",*:{self.color_tag_24bit}"')
            elif self.vers_ok(2.2):
                if not self.vers_ok(2.7):
                    #  24-bit color on older versions
                    #  This causes colors to completely fail on mosh < 1.4 connections,
                    #  so in the unlikely event that is used, disable use_24bit_color
                    #  RGB not supported until 2.7
                    self.color_tag_24bit = "Tc"
                w(f"{self.opt_server} -a terminal-overrides ',*:{self.color_tag_24bit}'")
        w()  # spacer between sections

    # pylint: disable=too-many-branches,too-many-statements
    def general_environment(self):
        w = self.write
        w(
            """
        #======================================================
        #
        #   General environment - server options
        #
        #======================================================
        """
        )
        # escape-time < 3.5 = 500 3.5 = 10

        if self.vers_ok(1.1):
            self.mkscript_shlvl_offset()
            w(
                f"""
                # Save correction factor for displaying SHLVL inside tmux
                {self.es.run_it(self._fnc_shlvl_offset, in_bg=True)}"""
            )

        if os.getenv("TMUX_NO_CLIPBOARD"):
            # On ssh/mosh connections, when running an asdf tmux with local
            # version changed.
            # tmux instacraches when anything is selected in a tmux buffer
            # if set-clipboard is not off
            if self.vers_ok(1.5):
                w(f"{self.opt_server} set-clipboard off  # TMUX_NO_CLIPBOARD")
        else:
            # using external on the outer, prevents inner tmux from setting
            # terminal clipboard
            if self.vers_ok(1.5):
                w(f"{self.opt_server} set-clipboard on")

        #
        #  Common variable telling plugins if -N notation is wanted
        #  (assuming tmux version supports it)
        #  Since the plugin init code can't use the vers_ok() found here
        #  this is a more practical way to instruct them to use it or not.
        #
        if self.vers_ok(3.1):
            w(
                f"""
                # Hint that plugins can check, will only be true if hints
                # are supported by running tmux, so plugins will not need
                # to check tmux version for this
                {self.opt_server} @use_bind_key_notes_in_plugins Yes
                """
            )

        nav_key = "N"
        if self.vers_ok(2.7):
            w(f'bind -N "Navigate ses/win/pane"     {nav_key}    choose-tree -O time -sZ')
        elif self.vers_ok(1.0):
            w(
                f'bind -N "Navigate ses/win/pane not available warning"  {nav_key}  '
                'display "Navigate needs 2.7"'
            )

        if self.vers_ok(2.8):
            w('bind Any display "This key is not bound to any action"\n')

        scrpad_min_vers = 3.2
        scrpad_key = "O"  # P being taken this is pOpup :)
        if self.vers_ok(scrpad_min_vers):
            display_popup = "display-popup -h 70% -w 70% -E "
            if self.vers_ok(3.3):
                display_popup += '-T "#[align=centre] pOpup Scratchpad Session " '
            w(
                f'bind -N "pOpup scratchpad session"  {scrpad_key}  '
                f'{display_popup} "$TMUX_BIN -u new-session -ADs scratch"'
            )
        elif self.vers_ok(1.0):
            w(
                f'bind -N "pOpup not available warning"  {scrpad_key}  '
                f'display "pOpup scratchpad session needs {scrpad_min_vers}"'
            )

        if self.vers_ok(1.0):
            show_action = f'\\; display "{self.conf_file} sourced"'
        else:
            show_action = ""
        w(f'bind -N  "Source {self.conf_file}"  R  source {self.conf_file} {show_action}')

        self.auc_display_plugins_used()
        self.auc_kill_tmux_server()
        if self.use_prefix_arrow_nav_keys:
            w(
                """
            #
            #  Due to the limited keyboard handling in iSH, only supporting
            #  unmodified arrorws, here they are used for document navigation.
            #
            #  <prefix> <arrow> generates: PageUp, PageDown, Home, End
            #
            #  For pane navigation in this case, use <prefix> hjkl
            #
            bind -N "Page up"    Up     send-key PageUp
            bind -N "Page Down"  Down   send-key PageDown
            bind -N "Home"       Left   send-key Home
            bind -N "End"        Right  send-key End"""
            )
        w()  # spacer between sections

    def remove_prefix(self, s):
        if s.lower().startswith("c-"):
            return s[2:]  # Remove the first 2 characters
        return s

    def session_handling(self):
        w = self.write
        w(
            """
        #======================================================
        #
        #   Session / Client handling  tmux is a bit inconsistent on the terms
        #
        #======================================================
        """
        )
        if self.prefix_key.lower() != "c-b":
            w(
                f"""# Remove the default prefix, do it before assigning
                # the selected one, in case it was some variant of C-b
                # keep it for now, doesn't hurt and might help pairprogrammers
                # unbind  C-b
                {self.opt_ses} prefix {self.prefix_key}"""
            )
            w(  # double prefix always works
                f'bind -N "Repeats sends {self.prefix_key} through"  '
                f"{self.prefix_key}  send-prefix"
            )
            if self.prefix_key.lower() not in ("c-w",):
                # this is recommended in tmux-sensible
                # I added filtering chars colliding with other binds
                w(
                    f'bind -N "prefix then same char sends {self.prefix_key} through"  '
                    f"{self.remove_prefix(self.prefix_key)}  send-keys {self.prefix_key}"
                )

            # in tmux-sensible it was recommended to bind prefix + same char without ctrl
            # to last-window, not sure, but perhaps a good idea?
            w()  # spacer

        w(f"{self.opt_ses} set-titles on")

        #
        # This prevents path_helper and similar tools from messing up PATH
        # inside tmux. On MacOS it is used by default,
        # maybe also on other platforms?
        #
        # Example of what it does: assume ~/bin is first in PATH
        # Inside tmux shells it will now be almost last...
        #
        # However using this on iSH confuses remote tmux sessions utterly
        #
        if not mtc_utils.IS_ISH:
            if self.vers_ok(1.0):
                # prevents /usr/libexec/path_helper from messing up PATH
                w(f'{self.opt_ses} default-command "${{SHELL}}"')
            else:
                w(
                    f'{self.opt_ses} default-command "export '
                    'TERM=screen-256color \\; ${SHELL}"'
                )
            w()  # spacer

        if self.vers_ok(1.0):
            # setting terminal app title - not sure if this is desired
            w(f"{self.opt_ses} base-index 1")
            w(
                f"{self.opt_ses} set-titles-string "
                '"#{host_short} - '
                f"tmux {self.vers.get()}"
                ' - #{session_name}:#{window_name}:#T"'
            )
        if self.vers_ok(1.7):
            w(f"{self.opt_ses} renumber-windows on")
        elif self.vers_ok(1.2):
            w(f"{self.opt_ses} detach-on-destroy off")
        if self.vers_ok(3.2):
            #  will switch to any detached session, when no more active ones
            w(f"{self.opt_ses} detach-on-destroy no-detached")

        w(
            f"""
        {self.opt_ses} repeat-time 750
        {self.opt_ses} history-limit 5000
        {self.opt_ses} status-keys emacs
        """
        )

        if self.vers_ok(0.9):
            s = 'bind -N "Kill session in focus"      M-x  confirm-before'
            if self.vers_ok(1.5):
                s += ' -p "Kill session: #{session_name}? (y/n)"'
            w(f"{s} kill-session")

        s = 'bind -N "Create new session  - M-+"  +    command-prompt'
        if self.vers_ok(1.5):
            s += ' -I "?"'
        if self.vers_ok(1.0):
            s += ' -p "Name of new session: "'
        w(f'{s} "new-session -s \\"%%\\""')

        self.auc_meta_ses_handling()  # used by iSH Console
        if self.vers_ok(1.2):
            # before 1.2 there was no relative switch-client

            # fix a couple of too long lines
            sc_p = "switch-client -p"
            sc_n = "switch-client -n"
            w(
                f"""# session navigation
                bind -N "Select previous session  - M-("  -r  (  {sc_p}
                bind -N "Select next session  - M-)"    -r  )  {sc_n}
                bind -N "Switch to last session"      _  switch-client -l
                bind -N "Select previous session  - P+( M-(" -n  C-M-Up    {sc_p}
                bind -N "Select next session  - P+) M-)"    -n  C-M-Down  {sc_n}"""
            )

        s = 'bind -N "Rename Session"  S  command-prompt'
        if self.vers_ok(1.5):
            s += ' -I "#S"'
        w(f'{s} "rename-session -- \\"%%\\""')

        w()  # spacer between sections

    def windows_handling_part_1(self):
        w = self.write
        w(
            f"""
        #======================================================
        #
        #   Windows handling
        #
        #======================================================

        {self.opt_win} automatic-rename off
        {self.opt_win} aggressive-resize on"""
        )
        if self.monitor_activity:
            w(
                f"""#  bell + # on window that had activity,
                # will only trigger once per window
                {self.opt_win} monitor-activity on"""
            )
            if self.vers_ok(1.9):
                w(f"{self.opt_win} window-status-activity-style default")
            if self.vers_ok(2.6):
                w(f"{self.opt_win} monitor-bell on")
        else:
            w(f"{self.opt_win} monitor-activity off")
            if self.vers_ok(2.6):
                w(f"{self.opt_win} monitor-bell off")

        if self.vers_ok(2.7):
            w(
                """
            # the default key is still available: <prefix> E
            # this is quicker to type on a touch screen
            bind -N "Spread panes out evenly."  e  select-layout -E
            """
            )
        if self.vers_ok(3.3):
            w(f"{self.opt_win} popup-border-lines rounded")

        w()  # spacer

        if self.vers_ok(1.5):
            s = "-I ?"
        else:
            s = ""
        cmd_new_win_named = (
            f'command-prompt {s} -p "Name of new window: "'
            ' "'  # wrap cmd in "
            f"new-window -n '%%' {self.current_path_directive}"
            '"'  # wrap cmd in "
        )

        for key in ("c", "="):  # c is just for compatibility with default key
            if self.vers_ok(1.0):
                w(f'bind -N "New window"  {key}  {cmd_new_win_named}')
            else:
                w(f'bind -N "New window"  {key} new-window')
        if self.vers_ok(1.0):
            w(f'bind -N "New window  - P+=" -n  M-=  {cmd_new_win_named}')

        pref = 'bind -N "Select the '
        w(
            f"""
        # window navigation
        {pref}previously current window  - M--"         -  last-window
        {pref}previous window  - P+9 M-9 C-M-Left"  -r  p  previous-window
        {pref}next window      - P+0 M-0 C-M-Right" -r  n  next-window
        {pref}previous window  - P+p M-9 C-M-Left"  -r  9  previous-window
        {pref}next window  - P+n M-0 C-M-Right"     -r  0  next-window
        """
        )
        if self.vers_ok(91.2):
            w(
                f"""{pref}previous window  - P+p P+9 M-9"  -n  C-M-Left   previous-window
            {pref}next window      - P+n P+0 M-0"  -n  C-M-Right  next-window"""
            )
        else:
            w(
                """
            # temp disabled until I stop using this for split pane
            bind -n C-M-Left display "Soon win navigation - use: <P> M-Left"
            bind -n C-M-Right display "Soon win navigation - use: <P> M-Right"
            """
            )

        #
        #  Splitting the entire window
        #
        self.auc_split_entire_window()  # used by iSH Console
        #
        #  Same using arrow keys with <prefix> M-S modifier
        #
        if self.vers_ok(2.3) and not self.is_tmate():
            #
            #  tmate does not support split-window -f  despite they claim
            #  to be 2.4 compatible and this is a 2.3 feature...
            #
            sw1 = 'bind -N "Split window'  # hackish strings
            sw2 = "split-window -f"  # to make sure
            suffix = self.current_path_directive
            w(
                f"""{sw1} left - P+C-M-h"   C-M-Left   {sw2}hb {suffix}
            {sw1} down - P+C-M-j"   C-M-Down   {sw2}v  {suffix}
            {sw1} up - P+C-M-k"     C-M-Up     {sw2}vb {suffix}
            {sw1} right - P+C-M-l"  C-M-Right  {sw2}h  {suffix}
            """
            )

    def windows_handling(self):
        self.windows_handling_part_1()
        w = self.write

        #
        #  I tend to bind ^[9 & ^[0 to Alt-Left/Right in my terminal apps
        #
        w("# adv key win nav")
        if self.vers_ok(1.0) and not self.tablet_keyb:
            w(
                'bind -N "Select the previous window '
                '- P+p P+9 C-M-Left" -n  M-9  previous-window'
            )
        if self.vers_ok(1.0):
            s = 'bind -N "Select the'
            w(
                f"""{s} next window - P+n P+0 C-M-Right"    -n  M-0  next-window
                {s} previously current window - P+-"    -n  M--  last-window"""
            )
        if self.vers_ok(2.1):
            w2 = "window"  # hackish strings to make sure
            cm = "-T copy-mode -n M-"  # line is not to long
            w(
                f"""# Override odd behaviour in copy-mode
                bind -N "Previous {w2}  - P+9" {cm}9  previous-{w2}
                bind -N "Next {w2} - P+0"      {cm}0  next-{w2}
                """
            )
        #
        #  Swap window left/right <prefix>  < / >
        #  This collides with some default popups,
        #  so only use if they are disabled.
        #  This is also available as no-prefix:  M-<  and  M->
        #  regardless of default popup status.
        #
        w(
            """# window shuffle
            bind -N "Swap window left"         -r  <    swap-window -dt:-1
            bind -N "Swap window right"        -r  >    swap-window -dt:+1"""
        )

        s = 'bind -N "Rename current window"   W  command-prompt'
        if self.vers_ok(1.5):
            s += ' -I "#W"'
        w(f'{s} "rename-window -- \\"%%\\""')

        #
        #  If last window of current session is killed, the session
        #  is destroyed and focus is moved to another session
        #
        for c in ("&", "X"):
            if self.vers_ok(1.5):
                w(
                    f'bind -N "Kill window in focus"    {c}  confirm-before -p '
                    '"kill current window \\"#W\\"? (y/n)" "kill-window"'
                )
            elif self.vers_ok(0.9):
                w(f'bind -N "Kill window in focus"  {c}  confirm-before kill-window')
        w()  # spacer between sections

    def pane_handling(self):
        w = self.write
        w(
            """
        #======================================================
        #
        #   Pane handling
        #
        #======================================================
        """
        )
        # the sleeps below are needed to wait until a pane exists
        if self.vers_ok(1.6):
            #  Set base index for panes to 1 instead of 0
            w(f"{self.opt_pane} pane-base-index 1")
        if self.vers_ok(1.8):
            w(f"{self.opt_pane} allow-rename off")

        if self.vers_ok(2.6) and not os.getenv("TMUX_NO_CLIPBOARD"):
            msg = "terminal clipboard is set"
            if self.vers_ok(3.2):
                delay = "-d 400"
            else:
                delay = ""
            w(
                f"""
            # Displays that tmux picked up clipboard and (hopefully) sent it
            # to the terminal
            set-hook -g pane-set-clipboard "display-message {delay} '{msg}'"
            """
            )

        if self.vers_ok(3.5):
            w(f"{self.opt_pane} allow-set-title off")

        w(f"bind -N 'Toggle synchronize'  *  {self.opt_win_loc} synchronize-panes")

        if self.vers_ok(0.9):
            s = 'bind -N "Kill pane in focus"  x  confirm-before'
            if self.vers_ok(1.5):
                s += ' -p "kill-pane #T (#P)? (y/n)"'
            w(f"{s} kill-pane")

        #
        #  Without a sleep in between the actions, history is not cleared.
        #  Just a guess, but most likely clear-history is run before C-l
        #  is handled by the terminal. Thus pushing the current screen
        #  back into history
        #
        if self.vers_ok(1.1):
            w(
                'bind -N "Clear history & screen" -n  M-l  send-keys C-l \\; '
                'run-shell "sleep 0.1" \\; clear-history'
            )

        #
        #  Save history for current pane, prompts for filename
        #
        #  Save as text              <prefix> M-h
        #  Save with escape codes    <prefix> M-e
        #
        #  When saved with escape code, less/most fails to display
        #  cat history-file will display the included colors correctly.
        #
        s = 'bind -N "Save history to prompted file name (no escapes)"  M-h  command-prompt'
        if self.vers_ok(1.0):
            s += ' -p "save history (no escapes) to:"'
            if self.vers_ok(1.5):
                s += ' -I "$TMPDIR"/tmux.history'
            s2 = "%1"
        else:
            s2 = "$TMPDIR/tmux.history"
        w(f'{s} "capture-pane -S - -E - \\; save-buffer {s2} \\; delete-buffer"')
        if self.vers_ok(1.8):
            w(
                'bind -N "Save history to prompted file name (includes escapes)"  '
                'M-e  command-prompt -p "save history (includes escapes) to:" '
                '-I "$TMPDIR/tmux-e.history" "capture-pane -S - -E - -e \\; '
                'save-buffer %1 \\; delete-buffer"'
            )

        if self.vers_ok(1.2):
            w(
                """
                #  Select, search, delete and even edit(!) paste buffers
                bind -N "Chose paste buffer(-s)"  B  choose-buffer
                """
            )
        w()  # spacer between sections

        #
        #  I have so many pane related settings, so it makes sense to
        #  split them up in multiple parts.
        #
        self.pane_frame_lines()
        self.pane_navigation()
        self.pane_splitting()
        self.pane_resizing()

    def pane_frame_lines(self):
        if not self.vers_ok(1.9):
            return

        w = self.write
        w(
            """
        #
        #   ======  Pane frame lines  ======
        #"""
        )
        #
        #  If you get frame lines drawn as x and q, you need to set an UTF-8 LANG
        #  sample: export LANG=en_US.UTF-8
        #  You should also be able to solve it by starting tmux with param -u
        #  Finally here is an in tmux hack to solve the pane border issue
        #  set -ga terminal-overrides ',*:enacs@:smacs@:rmacs@:acsc@'
        #

        if self.vers_ok(1.9):
            #
            #  Works both on bright and dark backgrounds
            #

            # experimenting with stronger contrast...
            border_active = "colour40"  # green
            border_other = "colour241"  # low intensity grey

            w(
                f"""
                {self.opt_pane} pane-active-border-style fg={border_active}
                {self.opt_pane} pane-border-style fg={border_other}
            """
            )

        #
        #  Display custom pane borders and title if >= 2.6
        #
        if self.vers_ok(2.3) and not self.is_tmate():
            pane_label = ""
            if self.vers_ok(2.6) and self.show_pane_title:
                pane_label += "#T "
            if self.show_pane_size:
                pane_label += "(#{pane_width}x#{pane_height}) "
            if pane_label:
                # set initial spacer
                pane_label = " " + pane_label
                w(f'{self.opt_pane} pane-border-format "{pane_label}"')

            # new windows with just one pane should not display pane border lines
            w('set-hook -g after-new-window "set -w pane-border-status off"')

            #  Display pane border lines when more than one pane is present
            if self.vers_ok(2.6):  # and not self.vers_ok(2.5)):
                extra_opt = "-F"
            else:
                extra_opt = ""
            w(
                f"set-hook -g window-layout-changed '{self.opt_win_loc} {extra_opt} "
                'pane-border-status "#{?#{==:#{window_panes},1},off,top}"'
                "'"  # end quote for 'set
            )

            # Hide frame lines when zoomed
            w(
                "set-hook -g after-resize-pane '"
                'if-shell "[ #{window_zoomed_flag} -eq 1 ]" '
                f'"{self.opt_win_loc} pane-border-status off" '
                f'"{self.opt_win_loc} pane-border-status top"'
                "'"  # end quote for 'if-shell
            )

        if self.vers_ok(3.2):
            w(f"{self.opt_pane} pane-border-lines single")

        if self.vers_ok(3.3):
            w(f"{self.opt_pane} pane-border-indicators arrows")

        if self.show_pane_title:
            if self.vers_ok(2.6):
                w(
                    'bind -N "Set pane title"  P  command-prompt -p '
                    '"Pane title: " "select-pane -T \\"%%\\""'
                )
            elif self.vers_ok(2.3) and not self.is_tmate():
                w(
                    f"""
                    {self.opt_pane} pane-border-status top
                    bind  P  display 'Pane title setting needs 2.6'
                    """
                )

        w()  # spacer between sections

    def pane_navigation(self):
        w = self.write
        w(
            """
        #
        #   ======  Pane Navigation  ======
        #
        """
        )
        if self.vers_ok(1.2):
            pane_left = "select-pane -L"
            pane_up = "select-pane -U"
            pane_right = "select-pane -R"
            pane_down = "select-pane -D"
        else:
            # Really old tmuxes can only navigate up/down by pane index
            pane_left = "up-pane"
            pane_up = "up-pane"
            pane_right = "down-pane"
            pane_down = "down-pane"

        # indicate the right alternate keys
        if self.vers_ok(1.0):
            w(
                f"""bind -N "Select pane left - P+Left M-Left"    -r  h  {pane_left}
                bind -N "Select pane down - P+Down M-Down"    -r  j  {pane_down}
                bind -N "Select pane up - P+Up M-Up"          -r  k  {pane_up}
                bind -N "Select pane right - P+Right M-Right" -r  l  {pane_right}

                bind -N "Select pane left - P+h M-Left"   -r  Left   {pane_left}
                bind -N "Select pane down - P+j M-Down"   -r  Down   {pane_down}
                bind -N "Select pane up - P+k M-Up"       -r  Up     {pane_up}
                bind -N "Select pane right - P+l M-Right" -r  Right  {pane_right}

                bind -N "Select pane left - P+h P+Left"   -n  M-Left   {pane_left}
                bind -N "Select pane down - P+j P+Down"   -n  M-Down   {pane_down}
                bind -N "Select pane up - P+k P+Up"       -n  M-Up     {pane_up}
                bind -N "Select pane right - P+l P+Right" -n  M-Right  {pane_right}
                """
            )

        if self.vers_ok(2.4):
            #
            #  In copy-mode M-Up/Down Scrolls half page, doesn't seem
            #  to be an important feature.
            #  Better to keep them to their normal setting as per above
            #
            w(f'bind -N "Select pane up"   -T "copy-mode"  M-Up   {pane_up}')
            w(f'bind -N "Select pane down" -T "copy-mode"  M-Down {pane_down}')

    def pane_splitting(self):
        #
        #  The defaults just covers splitting the pane right and down.
        #  I am using P+A-Arrows & P+C-hjkl to get a more logical input, and
        #  also to allow left/up splits.
        #
        w = self.write
        cur_path = self.current_path_directive

        w(
            """
        #
        #   ======  Pane Splitting  ======
        #
        """
        )
        if not self.vers_ok(1.0):
            w("bind  C-j     split-window -p 50")
            w("bind  M-Down  split-window -p 50")
            return

        if self.vers_ok(1.0):
            w(
                "bind -N 'Split pane down - P+M-Down'    -r  C-j  "
                f"split-window -v  {cur_path}"
            )
            w(
                "bind -N 'Split pane right - P+M-Right' -r  C-l  "
                f"split-window -h  {cur_path}"
            )
        if self.vers_ok(2.0):
            w(
                "bind -N 'Split pane left - P+M-Left'   -r  C-h  "
                f"split-window -hb {cur_path}"
            )
            w(
                "bind -N 'Split pane up - P+M-Up'       -r  C-k  "
                f"split-window -vb {cur_path}"
            )
        w()  # spacer
        if self.vers_ok(1.0):
            w(
                "bind -N 'Split pane down - P+C-j'  -r  M-Down   "
                f"split-window -v  {cur_path}"
            )
            w(
                "bind -N 'Split pane right - P+C-l' -r  M-Right  "
                f"split-window -h  {cur_path}"
            )
        if self.vers_ok(2.0):
            w(
                "bind -N 'Split pane left - P+C-h'  -r  M-Left   "
                f"split-window -hb {cur_path}"
            )
            w(
                "bind -N 'Split pane up - P+C-k'    -r  M-Up     "
                f"split-window -vb {cur_path}"
            )
        w()  # spacer between sections

    def pane_resizing(self):
        w = self.write
        w(
            """
        #
        #   ======  Pane Resizing  ======
        #
        """
        )

        # Defaults 1.0 2.8
        # bind-key -r -T prefix       M-Up              resize-pane -U 5
        # bind-key -r -T prefix       M-Down            resize-pane -D 5
        # bind-key -r -T prefix       M-Left            resize-pane -L 5
        # bind-key -r -T prefix       M-Right           resize-pane -R 5

        if self.vers_ok(1.0):
            w("bind -N 'Resize pane 1 left - C-S-Left'   -r  H  resize-pane -L")
        if self.vers_ok(0.9):
            w("bind -N 'Resize pane 1 down - C-S-Down'   -r  J  resize-pane -D")
        else:
            w("bind -r  J  resize-pane-down")

        if self.vers_ok(0.9):
            w("bind -N 'Resize pane 1 up - C-S-Up'       -r  K  resize-pane -U")
        else:
            w("bind -r  K  resize-pane-up")
        if self.vers_ok(1.0):
            w("bind -N 'Resize pane 1 right - C-S-Right' -r  L  resize-pane -R")
        w()
        if self.vers_ok(1.2):
            # keys without prefix never needs repeat set
            w("bind -N 'Resize pane 1 left  - P+H' -n  C-S-Left   resize-pane -L")
            w("bind -N 'Resize pane 1 down  - P+J' -n  C-S-Down   resize-pane -D")
            w("bind -N 'Resize pane 1 up    - P+K' -n  C-S-Up     resize-pane -U")
            w("bind -N 'Resize pane 1 right - P+L' -n  C-S-Right  resize-pane -R")
            w()
            w(
                """# For larger changes M-S Arrows scale by 5
            bind -N 'Resize pane 5 left'        -n  M-S-Left   resize-pane -L 5
            bind -N 'Resize pane 5 down'        -n  M-S-Down   resize-pane -D 5
            bind -N 'Resize pane 5 up'          -n  M-S-Up     resize-pane -U 5
            bind -N 'Resize pane 5 right'       -n  M-S-Right  resize-pane -R 5
            """
            )
        # if self.vers_ok(1.8):
        #     height_notice = "Pane height"
        #     if not self.vers_ok(3.3):
        #         height_notice += " (add 1 for panes next to status bar)"
        #     w(
        #         'bind -N "set pane size (w x h)"  s  command-prompt -p '
        #         f'"Pane width","{height_notice}" '
        #         '"resize-pane -x %1 -y %2"'
        #     )
        # elif self.vers_ok(1.0):
        #     w(
        #         'bind -N "Navigate not available warning"  s  '
        #         'display "set pane size needs 1.8"'
        #     )
        w()  # spacer

    def mouse_handling(self):
        w = self.write
        w(
            """
        #======================================================
        #
        #   Mouse handling
        #
        #======================================================
        """
        )
        if self.vers_ok(2.1):
            w(f"{self.opt_ses} mouse on\n")
            self.mkscript_toggle_mouse()
            w(f'bind -N "Toggle mouse on/off"  M  {self.es.run_it(self._fnc_toggle_mouse)}')
        else:
            w(f"{self.opt_win} mode-mouse on")
            if self.vers_ok(1.1):
                w(f"{self.opt_ses} mouse-select-pane on")
            if self.vers_ok(1.5):
                w(f"{self.opt_ses} mouse-select-window on")
                w(f"{self.opt_ses} mouse-resize-pane on")
            w('bind  M  display "mouse toggle needs 2.1"')

        #
        #  If enabled, request mouse input as UTF-8 on UTF-8 terminals
        #  This often seems to trigger random character output when
        #  mouse is moved after tmux session terminates, so better to
        #  disable.
        #
        # if self.vers_ok(2.2):
        #     w(f"{self.opt_ses} mouse-utf8 off")

        #
        #  Zooms pane by right double click
        #
        if self.vers_ok(2.4) and not self.is_tmate():
            w(
                'bind -N "Toggle zoom for mouseovered pane" -n  DoubleClick3Pane'
                ' resize-pane -Z -t= "{mouse}"'
            )
        w()  # spacer

    # pylint: disable=too-many-branches
    def status_bar_prepare(self):
        w = self.write
        w(
            """
        #======================================================
        #
        #   Status bar
        #
        #======================================================
        """
        )
        w(f"{self.opt_ses} status-interval {self.status_interval}")

        if self.is_tmate():
            w(f"{self.opt_ses} display-time 2000")
        else:
            w(f"{self.opt_ses} display-time 4000")
        if self.vers_ok(1.0):
            w(f"{self.opt_ses} status-justify left")
        if self.vers_ok(1.0) and self.monitor_activity:
            w(f"{self.opt_ses} visual-activity off")

        w("# Allow status to grow as needed")
        if self.vers_ok(3.0):
            unlimited = 0
        else:
            unlimited = 999
        if self.vers_ok(1.0):
            w(  # both are ses opts
                f"""{self.opt_ses} status-left-length  {unlimited}
                {self.opt_ses} status-right-length  {unlimited}
                """
            )
        else:
            # For pre 1.0 it needs to be set to something >10
            w(f"{self.opt_ses} status-left-length 30")

        if self.vers_ok(1.7):
            w(f"{self.opt_ses} status-position bottom")

        if self.vers_ok(1.9):
            w(f"{self.opt_win} window-status-current-style reverse")

        #
        #  Status bar assignments must come in intent order, not sorted by version!
        #
        if self.vers_ok(2.2):
            self.sb_right += "#{?window_zoomed_flag, 🔍 ,}"
        elif self.vers_ok(2.0):
            #
            #  Before 2.2 graphical chars (utf 8??) crashes the SB
            #
            self.sb_right += "#{?window_zoomed_flag, Z ,}"

        # if self.vers_ok(1.9) and not self.vers_ok(2.0):
        #     #
        #     #  Before 1.9 the pane_synchronized doesn't exist
        #     #  and from 2.0 #{prefix_highlight} from the
        #     #  tmux-plugins/tmux-prefix-highlight plugin
        #     #  better indicates sync mode
        #     #
        #     self.sb_right += "#[reverse]#{?pane_synchronized,sync,}#[default]"

        if self.vers_ok(1.8):
            #
            #  bypass tmux-prefix-highlight, hardcoding it to avoid countless
            #  variable parsings
            #
            if self.vers_ok(1.9):
                sync_indicator = (
                    "#{?synchronize-panes,#[default]#"
                    "[fg=black]#[bg=yellow]#[blink]#[bold] Sync ,#[default]}"
                )
                if self.vers_ok(2.5):
                    mode_str = "#{pane_mode}"
                else:
                    mode_str = "Copy"
                mode_indicator = (  # will display sync_indicator if not active
                    "#{"
                    f"?pane_in_mode,#[fg=black]#[bg=yellow]#[bold] {mode_str} ,"
                    f"{sync_indicator}"
                    "}"
                )  #
            else:
                mode_indicator = ""

            prefix_indicator = (  # will display copy_indicator if not active
                "#{?client_prefix,#[fg=colour231]#[bg=colour04]"
                f" {self.display_prefix()} ,{mode_indicator}"
                "}#[default]"
            )
            w(f"# prefix_indicator:[{prefix_indicator}]")
            self.sb_right += prefix_indicator

    def status_bar(self):
        w = self.write
        self.status_bar_prepare()
        if self.status_bar_customization():
            w("\n#---   End of status_bar_customization()   ---")

        #
        #  Add this after status_bar_customization() to make it
        #  non-obvious to override it, hint local_overides()
        #
        if self.t2_env:
            #
            #  max length of vers is 6 chars, in order to
            #  not flood status line if running a devel tmux
            #
            if self.is_tmate():
                prefix = "tmate"
            else:
                prefix = f"{self.vers.get()[:6]}"
            t2_tag = f"{prefix} {self.display_prefix()} "
            self.sb_left = f"#[fg=green,bg=black]{t2_tag}#[default]{self.sb_left}"

        self.filter_me_from_sb_right()

        if not self.username_template and self.hostname_template:
            #
            #  insert spacer after time if no username is displayed
            #  unless hostname is also empty
            #
            self.hostname_template = " " + self.hostname_template

        #
        #  Before 1.8 only basic text and strftime(3) can be used
        #
        if not self.vers_ok(1.8):
            self.sb_left = self.sb_left.replace("#{session_name}", "#S")

        self.sb_right = self.sb_right.replace(
            "USERNAME_TEMPLATE", self.username_template
        ).replace("HOSTNAME_TEMPLATE", self.hostname_template)

        if not self.vers_ok(1.0):
            # setting colors in status line not supported
            self.sb_left = re.sub(r"#\[.*?\]", "", self.sb_left)
            self.sb_right = re.sub(r"#\[.*?\]", "", self.sb_right)
        w(
            f"""
        {self.opt_ses} status-left "{self.sb_left}"
        {self.opt_ses} status-right "{self.sb_right}"

        bind -N "Toggle status bar"  T  {self.opt_ses} status

        """
        )

    def filter_me_from_sb_right(self):
        """Don't display my primary username."""

        #  If its my default accounts don't show username
        if os.getenv("USER") in ("jaclu", "u0_a194"):
            self.username_template = ""

            #
            #  Actions bound to Alt uppercase keys. The iSH console doesn't
            #  generate the correct sequences, so must be remapped via user-keys
            #  Further you need to bind those user keys to the intended action.
            #  To avoid having to repeat code I use special methods handling such
            #  keys, for terminals relaying on user-keys, they can be bound to
            #  the intended action fairly simply.
            #

    def muc_non_default_prefix(self, default, current):
        # If a non-default is used, display it as a prefix
        if default != current:
            return f"{default} - "
        return ""

    def auc_meta_ses_handling(self):
        # Defaults might be overridden by TabletBtKbd()
        self.write("# auc_meta_ses_handling()")

        if self.muc_keys["M_plus"] in (None, ""):
            sys.exit("ERROR: auc_meta_ses_handling() M_plus undefined!")

        w = self.write
        if self.vers_ok(1.0):
            s = (
                'bind -N "Create new session  - P++"      '
                f"-n  {self.muc_keys['M_plus']}  command-prompt "
            )
            if self.vers_ok(1.5):
                s += ' -I "?"'
            w(f'{s} -p "Name of new session: " "new-session -s \\"%%\\""')

        if self.vers_ok(1.2):
            w(
                f"bind -N '{self.muc_non_default_prefix(
                    self.default_m_underscore,
                    self.muc_keys['M_underscore'])
                }Switch to last session  - P+_'  "
                f"-n  {self.muc_keys['M_underscore']}  switch-client -l"
            )
            w(
                "bind -N 'Select previous session  - P+( C-M-Up'"
                f" -n  {self.muc_keys['M_par_open']}  switch-client -p"
            )

            # P+)  {self.muc_keys['M_par_close']} C-M-Down
            w(
                "bind -N 'Select next session  - P+) C-M-Down'   "
                f"-n  {self.muc_keys['M_par_close']}  switch-client -n"
            )

    def auc_display_plugins_used(self):  # used by iSH Console
        """iSH console doesn't generate correct ALT - Upper Case sequences,
        so when that is the env, intended keys must be bound as user keys.
        To make that without having two separate snippets of code doing
        the same and keeping them in sync, the default parameters are
        the "normal" case, when used for iSH console, the
        user keys will be given
        """
        self.write("# auc_display_plugins_used()")
        if not self.vers_ok(1.8):
            # There is no plugin support...
            return

        if self.muc_keys["M_P"] != "M-P":
            # If a custom defined key is used the hint won't be helpful about
            # that the key combo for this is...
            note_prefix = "Press: P+M-P - "
        else:
            note_prefix = ""
        #
        # The conf_file needs to be mentioned below to make sure
        # the -p2 run-shell doesn't complain if a non-standard config is used
        # it won't be over-written!
        #
        repo_dir = os.path.dirname(__file__)
        self.write(
            f'bind -N "{note_prefix}List all plugins defined"  {self.muc_keys["M_P"]}  '
            'run-shell "'
            '$TMUX_BIN display-message \\"Generating plugin list\\" \\; '
            # 1st load venv if used
            f"[ -d {repo_dir}/.venv ] && . {repo_dir}/.venv/bin/activate \\; "
            f"{__main__.__file__} -t {self.tmux_bin} -p2 {self.conf_file}"
            '"'
        )

    def auc_kill_tmux_server(self):  # used by iSH Console
        """iSH console doesn't generate correct ALT - Upper Case sequences,
        so when that is the env, intended keys must be bound as user keys.
        To make that without having two separate snippets of code doing
        the same and keeping them in sync, the default parameters are
        the "normal" case, when used for iSH console, the
        user keys will be given

        Can not be used before tmux 0.9!
        """
        if not self.vers_ok(0.9):
            return

        self.write("# auc_kill_tmux_server()")
        if self.muc_keys["M_X"] != "M-X":
            note_prefix = "Press: M-X - "
        else:
            note_prefix = ""

        s = (
            f'bind -N "{note_prefix}Kill tmux server"  '
            f"{self.muc_keys['M_X']}  confirm-before"
        )
        if self.vers_ok(1.5):
            s += f' -p "kill tmux server {self.conf_file}? (y/n)"'
        self.write(f"{s} kill-server")

    def auc_split_entire_window(self):
        """iSH console doesn't generate correct ALT - Upper Case sequences,
        so when that is the env, intended keys must be bound as user keys.
        To make that without having two separate snippets of code doing
        the same and keeping them in sync, the default parameters are
        the "normal" case, when used for iSH console, the
        user keys will be given
        """
        w = self.write
        pref = 'bind -N "Split window '
        sw = "split-window -f"
        cp = self.current_path_directive

        if self.is_tmate() or not self.vers_ok(2.3):
            #
            #  tmate does not support split-window -f  despite they claim
            #  to be 2.4 compatible and this is a 2.3 feature...
            #
            return

        w(
            f"""# auc_split_entire_window()
            {pref}left - P+C-M-Left"    {self.muc_keys["C_M_h"]}  {sw}hb {cp}
            {pref}down - P+C-M-Down"    {self.muc_keys["C_M_j"]}  {sw}v  {cp}
            {pref}up - P+C-M-Up"        {self.muc_keys["C_M_k"]}  {sw}vb {cp}
            {pref}right - P+C-M-Right"  {self.muc_keys["C_M_l"]}  {sw}h  {cp}
            """
        )

    #
    #  Utility methods
    #
    def define_opt_params(self):
        #
        # Define params to use to set various types of options
        # in general they are global, except for opt_win_loc that needs to modify
        # settings on a specific window
        #
        self.opt_server = "set -g"
        self.opt_ses = "set -g"
        if self.vers_ok(1.8):
            self.opt_win_loc = "set -w"
        else:
            self.opt_win_loc = "set-window-option"
        self.opt_win = f"{self.opt_win_loc} -g"
        if self.vers_ok(3.1):
            self.opt_pane = "set -g"
        else:
            # prior to 3.1 pane options were listed as win options
            self.opt_pane = self.opt_win

    def display_prefix(self):
        # Using consistent prefix key notation
        return self.prefix_key  # .lower().replace("c-", "^")

    def mkscript_toggle_mouse(self):
        """Toggles mouse handling on/off"""
        #  The {} encapsulating the script needs to be doubled to escape them
        toggle_mouse_sh = [
            f"""
{self._fnc_toggle_mouse}() {{
    #  This is so much easier to do in a proper script...
    old_state=$($TMUX_BIN show -gv mouse)
    if [ "$old_state" = "on" ]; then
        new_state="off"
    else
        new_state="on"
    fi
    $TMUX_BIN {self.opt_ses} mouse $new_state
    $TMUX_BIN display "mouse: $new_state"
}}"""
        ]
        self.es.create(self._fnc_toggle_mouse, toggle_mouse_sh)

    def mkscript_shlvl_offset(self):
        """Generate a SHLVL offset"""
        shlvl_offset_sh = [
            # region shlvl_offset_sh
            f"""
{self._fnc_shlvl_offset}() {{
    shlvl="$(echo "$SHLVL")"
    f_tmux_socket="$(echo "$TMUX" | cut -d, -f 1)"
    f_tmux_offset="$f_tmux_socket"-shlvl_offset

    # clear out the previous one, to ensure the current is created
    rm -f "$f_tmux_offset"

    os_offset=0
    if [ "$(uname -s)" = "Darwin" ]; then
        os_offset=2
    elif [ -d /proc/ish ] && [ -f /etc/alpine-release ]; then
        os_offset=2
    elif [ "$(uname -s)" = "Linux" ] && [ -f /etc/alpine-release ]; then
        #
        # Can only check chroot on Linux
        # Only chrooted Alpine needs this offset
        #
        if ! grep -q " / / " /proc/self/mountinfo; then
            os_offset=1
        fi
    fi
    if [ "$os_offset" -ne 0 ]; then
        corrected_offset="$(echo "$shlvl - $os_offset" | bc)"
    else
        corrected_offset="$shlvl"
    fi
    echo "$corrected_offset" >"$f_tmux_offset"
    msg="SHLVL[$SHLVL] shlvl[$shlvl] os_offset[$os_offset]"
    echo "$msg corrected[$corrected_offset]" >>~/tmp/shlvl.log
    # ensure that it was created,
    if [ ! -s "$f_tmux_offset" ]; then
        echo "ERROR: Failed to create: $f_tmux_offset"
        exit 1
    fi
}}
                """
            # endregion
        ]
        self.es.create(self._fnc_shlvl_offset, shlvl_offset_sh)

    def mkscript_tpm_deploy(self):
        """Overrides tmux_conf.plugins instance, to add
        toggling of tpm_initializing.

        On iSH sometimes tpm never completes, and thus, indicating
        that condition helps me having to always check it manually.
        """

        output = []
        output.append(
            """
        #======================================================
        #
        #   Tmux Plugin Manager
        #
        #======================================================
        """
        )
        #  os.makedirs(plugins_dir, exist_ok=True)
        plugins_dir, tpm_env = self.plugins.get_env()
        tpm_location = os.path.join(plugins_dir, "tpm")
        tpm_app = os.path.join(tpm_location, "tpm")

        activate_tpm_sh = [
            # region _fnc_activate_tpm
            f"""
{self._fnc_activate_tpm}() {{
    timer_start
    {self.es.call_script(self._fnc_tpm_indicator)} set

    #
    #  Initialize already installed tpm if found
    #  override in base.py
    #
    if [ -x "{tpm_app}" ]; then

        {tpm_env}{tpm_app}

        timer_end "Completed tpm"
        {self.es.call_script(self._fnc_tpm_indicator)} clear
        exit 0
    fi

    #  Create plugin dir if needed
    mkdir -p "{plugins_dir}"

    #  Remove potentially broken tpm install
    rm -rf "{tpm_location}"

    $TMUX_BIN display "Cloning {self.plugin_handler} into {tpm_location} ..."
    git clone https://github.com/{self.plugin_handler} "{tpm_location}"
    if [ "$?" -ne 0 ]; then
        echo "Failed to clone tmux plugin handler:"
        echo "  https://github.com/{self.plugin_handler}"
        exit 11
    fi

    $TMUX_BIN display "Running cloned tpm..."
    {tpm_env}"{tpm_app}"
    if [ "$?" -ne 0 ]; then
        echo "Failed to run: {tpm_app}"
        exit 12
    fi

    #
    #  this only triggers plugins install if tpm needed to be installed.
    #  Otherwise installing missing plugins is delegated to tpm.
    #  Default trigger is: <prefix> I
    #
    $TMUX_BIN display "Installing all plugins..."
    {tpm_env}"{tpm_location}/bindings/install_plugins"
    if [ "$?" -ne 0 ]; then
        echo "Failed to run: {tpm_location}/bindings/install_plugins"
        exit 13
    fi

    timer_end "installing plugins"
    # {self.es.call_script(self._fnc_tpm_indicator)} clear
    $TMUX_BIN display "Plugin setup completed"
}}

#
#  Two support functions, not directly handled by my_tmux_conf
#
timer_start() {{
    t_start="$(date +%s)"

}}

timer_end() {{
    lbl="$1"
    t_duration="$(($(date +%s) - t_start))"
    if [ $t_duration -gt 1 ]; then
        #
        #  Logging startup times for slow hosts
        #
        dte_mins="$((t_duration / 60))"
        dte_seconds="$((t_duration - dte_mins * 60))"
        #  Add zero prefix when < 10
        [ "$dte_mins" -gt 0 ] && [ "$dte_mins" -lt 10 ] && dte_mins="0$dte_mins"
        [ "$dte_seconds" -lt 10 ] && dte_seconds="0$dte_seconds"
        msg="[$(date)] $dte_mins:$dte_seconds $TMUX_CONF"
        [ -n "$lbl" ] && msg="$msg - $lbl"
        TMPDIR="${{TMPDIR:-/tmp}}" # honour it if set
        echo "$msg"  >> "$TMPDIR"/tmux-tpm-startup-times
    fi
}}
"""
            # endregion
        ]
        self.es.create(self._fnc_activate_tpm, activate_tpm_sh)

    def mkscript_tpm_indicator(self):
        """Changes state for tpm_initializing with params: set clear"""
        purge_seq = self.tpm_initializing.replace("[", "\\[").replace("]", "\\]")
        # self.sb_purge_tpm_running = f"$TMUX_BIN {self.opt_ses} -q status-right "
        # \\"$($TMUX_BIN display -p '#{{status-right}}' | sed 's/{purge_seq}//')\\"

        clear_tpm_init_sh = [
            f"""
{self._fnc_tpm_indicator}() {{
    case "$1" in
      "set") task="set" ;;
      "clear") task="clear" ;;
      *)
        $TMUX_BIN display -p "{self._fnc_tpm_indicator}($1) bad param"
        exit 1
    esac

    sb_r_now="$($TMUX_BIN display -p '#{{status-right}}')"
    if [ -n "$($TMUX_BIN display -p '#{{{self.tpm_working_incicator}}}')" ]; then
        tpm_running=1
    else
        tpm_running=0
    fi

    if [ "$task" = "set" ] && [ "$tpm_running" -eq 0 ]; then
        $TMUX_BIN setenv -g {self.tpm_working_incicator} 1

        #
        #  Add tpm init to SB-right
        #
        $TMUX_BIN {self.opt_ses} status-right "$sb_r_now{self.tpm_initializing}"
    elif [ "$task" = "clear" ] && [ "$tpm_running" -eq 1 ]; then
        #
        #  Remove tpm init from SB-right
        #
        sb_r_filtered="$(echo $sb_r_now | sed 's/{purge_seq}//')"
        $TMUX_BIN {self.opt_ses} status-right "$sb_r_filtered"

        $TMUX_BIN setenv -gu {self.tpm_working_incicator}
    fi
}}
"""
        ]
        self.es.create(self._fnc_tpm_indicator, clear_tpm_init_sh)

    def check_libs_compatible(self):
        """Inspection of tmux-conf version to see if it is compatible"""
        try:
            lib_vers_found = self.lib_version.split()[0]
            # [:len(TMUX_CONF_NEEDED)]
        except AttributeError:
            print()
            print(f"ERROR: Needs tmux_conf lib version: {TMUX_CONF_NEEDED}")
            print("       Failed to read version, probably too old()")
            sys.exit(mtc_utils.ERROR_INCOMPATIBLE_TMUX_CONF_LIB)

        maj_vers_found = ".".join(lib_vers_found.split(".")[:2])
        maj_vers_needed = ".".join(TMUX_CONF_NEEDED.split(".")[:2])

        if maj_vers_found != maj_vers_needed:
            self.incompatible_tmux_conf(
                lib_vers_found,
                "Major version incompatible!",
                f"needs: {maj_vers_needed}",
            )

        min_vers_found = int(lib_vers_found.split(".")[2])
        min_vers_needed = int(TMUX_CONF_NEEDED.split(".")[2])
        if min_vers_found < min_vers_needed:
            self.incompatible_tmux_conf(lib_vers_found, "Version to old!")

    def incompatible_tmux_conf(self, lib_vers_found: str, reason: str, details: str = ""):
        print()
        print("ERROR: Incompatible tmux-conf package")
        print()
        print(reason)
        if details:
            print()
            print(details)
        print()
        print(f"vers found: {lib_vers_found}   needs: {TMUX_CONF_NEEDED}")
        sys.exit(mtc_utils.ERROR_INCOMPATIBLE_TMUX_CONF_LIB)

    def euro_fix(self, sequence: str):
        """Some keybs fail to render the Euro sign for M-S-2
        Only do this if local currency is EUR"""
        # print(f"><> euro_fix({sequence})")
        if not self.vers_ok(2.6):
            return  # user keys not yet available

        w = self.write
        if sequence[:1] != "\\":
            print()
            print(f"ERROR: euro_fix({sequence}) must be given in octal notation")
            sys.exit(mtc_utils.ERROR_USER_KEY_NOT_OCTAL)
        currency = mtc_utils.get_currency()
        if currency == "EUR":
            # print("><> Wiill write euro workaround")
            w(
                f"""# M-S-2 should be €
                set -s user-keys[180] "{sequence}"
                bind -N "Send €" -n User180 send "€" """
            )
        elif currency:
            w(
                f"""
                # When checking EUR was not reported as local currency where this node is
                # located, so no EUR fix applied. This node reports: {currency}."""
            )
        else:
            w("# No default currency could be retrieved for this node")


if __name__ == "__main__":
    BaseConfig().run()
