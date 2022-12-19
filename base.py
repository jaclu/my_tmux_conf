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
#  This is tested to work without issues all the way back to version 1.7
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


import os
import subprocess  # nosec
import sys
from pydoc import locate

import __main__

TMUX_CONF_NEEDED = "0.15.9"

#
#  Special import handling for debugging, is ignored in normal usage
#
cfb = os.environ.get("__CFBundleIdentifier")
if cfb and (cfb.find("sublime") > -1 or cfb.find("VSCode") > -1):
    #  Makes debugging easier, being able to use the lib without deployment
    #  assumes tmux-conf is checked out inside this repository
    TmuxConfig = locate("local_tmux_conf.src.tmux_conf.tmux_conf.TmuxConfig")
else:
    # import as package
    try:
        # pyright: reportMissingImports=false,reportGeneralTypeIssues=false
        from tmux_conf import TmuxConfig
    except ModuleNotFoundError:
        print("Dependency tmux_conf not installed!")
        sys.exit(1)


class BaseConfig(TmuxConfig):
    """Defines the general tmux setup, key binds etc"""

    prefix_key = "C-a"
    prefix_key_T2 = "C-w"  # prefix for inner dev environment

    status_interval = 10  # How often the status bar should be updated

    monitor_activity = False  # Notification when other windows change state

    show_pane_title = True  # If enabled, Set title with <P> P
    show_pane_size = True  # If enabled pane frane lines will display pane size

    #
    #  So that I can disable them and practice the vi keys every now and
    #  then. If Falde, Meta keys are unbound
    #
    bind_meta = True

    #
    #  Default templates for the status bar, so that they can easily be
    #  modified using status_bar_customization()
    #
    sb_left = "#[default]|#{session_name}| "
    sb_right = "%a %h-%d %H:%M USERNAME_TEMPLATEHOSTNAME_TEMPLATE"
    username_template = "#[fg=colour1,bg=colour195] #(whoami) #[default]@"
    hostname_template = "#[fg=colour195,bg=colour1] #h #[default]"

    handle_iterm2 = True  # Select screen-256color for iTerm2

    #
    #  Indicates this is a separate tmux env, I use it for testing
    #  plugin compatibility, and changed settings in a way that does not
    #  interfere with my main environment
    #
    t2_env = os.environ.get("T2_ENV")

    #  to avoid typos I use constants for script names
    fnc_toggle_mouse = "toggle_mouse"

    # ======================================================
    #
    #  overrides of tmux-conf package defaults
    #
    # ======================================================

    plugin_handler = "jaclu/tpm"

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
    ):
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

        if self.is_tmate() and (self.show_pane_title or self.show_pane_size):
            print("show_pane_title & show_pane_size disabled for tmate")
            self.show_pane_size = self.show_pane_title = False

        if self.t2_env:
            if self.conf_file == os.path.expanduser("~/.tmux.conf"):
                print()
                print("ERROR: T2_ENV & ~/.tmux.conf can't be combined!")
                sys.exit(1)
            conf_dir = os.path.dirname(self.conf_file)
            self.tpm_location = os.path.join(conf_dir, "plugins", "tpm")
            self.prefix_key = self.prefix_key_T2
            print(f"T2_ENV uses prefix_key: {self.prefix_key}")

        if os.path.isdir("/proc/ish"):
            print("Detected iSH kernel, assuming this to be a limited host")
            self.is_limited_host = True

    def status_bar_customization(self, print_header: bool = True) -> bool:
        """This is called just before the status bar is rendered,
        local_overides() is called later so can not modify status bar
        left & right without a pointless reassignment.

        I use this to add hooks for plugins that are currently used.

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

    def content(self):
        """This generates the majority of the tmux.conf.

        Plugins can be handled by plugin_foo() methods, but its
        perfectly fine to just include such code here if that is your
        preference.

        In my setup I try to always be backwards compatible in the sense
        that if I bind something to a meta key, I try to also make it
        available via prefix, in order to still be accessible on dumb
        terminals.
        """
        w = self.write

        self.connecting_terminal()
        self.general_environment()
        self.mouse_handling()
        self.status_bar()
        self.session_handling()
        self.windows_handling()
        self.pane_handling()

        w(
            """

        #======================================================
        #
        #   Local overrides
        #
        #======================================================
        """
        )
        self.local_overides()

    def local_overides(self):
        """Local overrides applied last in the config, not related to
        status bar, for that see status_bar_customization()
        """
        return

    #
    #  content methods broken up in parts, by content
    #
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
        #    Select TERM based on tmux version and terminal application.
        #
        #
        #  If LC_TERMINAL is not passed through, add this to the servers
        #  /etc/ssh/sshd_config:
        #
        # # Allow client to pass locale environment variables
        # AcceptEnv LANG LC_*
        #
        if self.vers_ok(2.6):
            if self.handle_iterm2 and os.getenv("LC_TERMINAL") == "iTerm2":
                w("set -s  default-terminal screen-256color")
                #
                #  Makes 24-bit colors fail utterly on mosh connections.
                #  So I keep it off.
                #
                #  Without it 24-bit is used on ssh connections
                #  and displayed as 256 colours when using mosh
                #  If you connect first using mosh, then later re-connect using
                #  ssh, previou output will still be 256 colors, but any new
                #  output will use 24-bit
                #
                # w('set -ga terminal-overrides ,*256col*:Tc')
            else:
                # Default TERM
                w("set -s  default-terminal tmux-256color")
        else:
            if self.vers_ok(2.1):
                #
                #  this became a server option starting with 2.0
                #  according to tmux-sensible plugin
                #
                def_term_context = "s"
            else:
                def_term_context = "g"
            w(f"set -{def_term_context} default-terminal screen-256color")

        #
        #  For old tmux versions, this is needed to support modifiers for
        #  function keys
        #
        #    https://github.com/tmux/tmux/wiki/Modifier-Keys#modifiers-and-function-keys
        #
        if not self.vers_ok(2.4):
            w("set -g  xterm-keys on")

        #
        #  Support for CSI u  extended keys
        #
        #    https://github.com/tmux/tmux/wiki/Modifier-Keys#extended-keys
        #
        #  Some apps like iTerm2 don't need it, but it never hurts
        #
        if self.vers_ok(3.2):
            w("set -s  extended-keys on")
            #
            #  not needed for all terminal apps, but since it doesn't hurt,
            #  it makes sense to always include it
            #
            w("set -as terminal-features 'xterm*:extkeys'")

        #
        #  Enable focus events for terminals that support them to be passed
        #  through to applications running inside tmux
        #
        if self.vers_ok(1.9):
            w("set -g  focus-events on")

        w()  # spacer between sections

    def general_environment(self):
        w = self.write
        w(
            """
        #======================================================
        #
        #   General environment
        #
        #======================================================"""
        )
        w(
            """
        set -g  display-time 4000
        set -g  repeat-time 750   # I want it a bit longer than 500')
        set-option -s escape-time 0
        set-option -g history-limit 50000
        set-option -g status-keys emacs
        """
        )

        if self.vers_ok(2.6):
            #  Safe, does not allow apps inside tmux to set clipboard
            #  for terminal
            w("set -g  set-clipboard external")
        else:
            w("set -g  set-clipboard on")

        if self.vers_ok(3.3):
            #  needs a short wait, so that display has time to be created
            w("run -b 'sleep 0.2 ; $TMUX_BIN set -w popup-border-lines rounded'")

        self.remove_unwanted_default_bindings()

        # pyright: reportImplicitStringConcatenation=false
        if self.prefix_key.lower() != "c-b":
            w(
                f"""
            set -g  prefix  {self.prefix_key}
            unbind  C-b     # remove default prefix key"""
            )
            w(
                f'bind -N "Repeats sends {self.prefix_key} through"  '
                f"{self.prefix_key}  send-prefix"
            )
            w()

        #  Seems to mess with ish-console, so trying without it
        # if self.vers_ok(2.8):
        #     w('bind Any display "This key is not bound to any action"\n')

        #
        #  Common variable telling plugins if -N notation is wanted
        #  (assuming tmux version supports it)
        #  Since the plugin init code cant use the vers_ok() found here
        #  this is a more practical way to instruct them to use it or not.
        #
        if self.vers_ok(3.1):
            w('set -g @use_bind_key_notes_in_plugins "Yes"\n')

        w(
            f'bind -N  "Source {self.conf_file}"  R  '
            f'source {self.conf_file} \\; display "{self.conf_file} sourced"'
        )

        nav_key = "N"
        w("\n# Navigate to find ses/pane")
        if self.vers_ok(2.7):
            w(
                f'bind -N "Navigate ses/win/pane"     {nav_key}    '
                "choose-tree -O time -sZ"
            )
        else:
            w(
                f'bind -N "Navigate not available warning"  {nav_key}  '
                'display "Navigate needs 2.7"'
            )
        w()  # Spacer

        self.display_plugins_used_UK()

        scrpad_key = "O"  # P being taken this is pOpup :)
        scrpad_min_vers = 3.2
        if self.vers_ok(scrpad_min_vers):
            display_popup = "display-popup -h 70% -w 70% -E "
            if self.vers_ok(3.3):
                display_popup += "-T " '"#[align=centre] pOpup Scratchpad Session " '
            w(
                f'bind -N "pOpup scratchpad session"  {scrpad_key}  '
                f'{display_popup} "$TMUX_BIN -u new-session -ADs scratch"'
            )
        else:
            w(
                f'bind -N "pOpup not available warning"  {scrpad_key}  '
                f'display "pOpup scratchpad session needs {scrpad_min_vers}"'
            )

        self.kill_tmux_server_UK()
        w()  # spacer between sections

    def remove_unwanted_default_bindings(self):
        w = self.write
        w(
            """
        #
        #  Remove unwanted default bindings
        #

        #
        #  Chooses next layout, potentially ruining a carefully crafted one.
        #  I can't really see any purpose with this one. You can access
        #  the layouts directly using <prefix> M-[1-5],
        #  so the safe bet is to disable
        #
        unbind  Space    #  Select next layout

        #
        #  C-Up/Down are handled by MacOS, and since that is what I
        #  usually use, I disable these keys, to ensure they will
        #  never-ever enter my muscle-memory by accident
        #
        unbind  C-Up     #  Resize the pane up
        unbind  C-Down   #  Resize the pane down
        unbind  C-Left   #  Resize the pane left
        unbind  C-Right  #  Resize the pane right
        """
        )

        if self.vers_ok(2.1):
            w(
                """
            #
            #  Remove the default popup menus
            #
            unbind  <   #  Manipulating window
            unbind  >   #  Manipulating pane

            unbind  -n  MouseDown3Pane
            unbind  -n  M-MouseDown3Pane
            unbind  -n  MouseDown3Status"""
            )

        if self.vers_ok(2.9):
            w("unbind  -n  MouseDown3StatusLeft")
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
            w("set  -g mouse on\n")
            self.mkscript_toggle_mouse()
            w(
                'bind -N "Toggle mouse on/off"  M  '
                f"{self.es.run_it(self.fnc_toggle_mouse)}"
            )
        else:
            w(
                """set -g mouse-resize-pane on
            set -g mouse-select-pane on
            set -g mouse-select-window on

            bind  M  display "mouse toggle needs 2.1" """
            )

        #
        #  If enabled, request mouse input as UTF-8 on UTF-8 terminals
        #  This often seems to trigger random character output when
        #  mouse is moved after tmux session terminates, so better to
        #  disable.
        #
        # if self.vers_ok(2.2):
        #    w('set -gq mouse-utf8 off')

        #
        #  Zooms pane by right double click
        #
        if self.vers_ok(2.4) and not self.is_tmate():
            w(
                'bind -N "Toggle zoom for mouseovered pane" -n  DoubleClick3Pane'
                ' resize-pane -Z -t= "{mouse}"'
            )
        w()  # spacer between sections

    def status_bar(self):
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
        #
        #  Before 1.8 only basic text and strftime(3) can be used
        #  So I just don't bother and leave the defaults
        #
        if self.vers_ok(1.8):
            w("# Allow status to grow as needed")
            if self.vers_ok(3.0):
                unlimited = 0
            else:
                unlimited = 999

            w(
                f"""set -g  status-left-length  {unlimited}
                  set -g  status-right-length {unlimited}
                  """
            )
            w(f"set -g  status-interval {self.status_interval}")

        if self.vers_ok(1.9):
            w("set -g  window-status-current-style reverse")

        w("set -g  status-justify left")

        if self.monitor_activity:
            w(
                """#  bell + # on window that had activity,
            # will only trigger once per window
            set -g  monitor-activity on
            set -g  visual-activity off"""
            )
            if self.vers_ok(2.6):
                w("set -g  monitor-bell on")
            if self.vers_ok(1.9):
                w("set -g  window-status-activity-style default")
        else:
            w("setw -g monitor-activity off")
            w("set -g  visual-activity off")
            if self.vers_ok(2.6):
                w("set -g  monitor-bell off")

        if self.vers_ok(2.2):
            self.sb_right += "#{?window_zoomed_flag, 🔍 ,}"
        elif self.vers_ok(2.0):
            #
            #  Before 2.2 graphical chars (utf 8??) crashes the SB
            #
            self.sb_right += "#{?window_zoomed_flag, Z ,}"

        if self.vers_ok(1.9) and not self.vers_ok(2.0):
            #
            #  Before 1.9 the pane_synchronized doesn't exist
            #  and from 2.0 #{prefix_highlight} from the
            #  tmux-plugins/tmux-prefix-highlight plugin
            #  better indicates sync mode
            #
            self.sb_right += "#[reverse]#{?pane_synchronized,sync,}#[default]"

        if self.status_bar_customization():
            w("\n#---   End of status_bar_customization()   ---")

        #
        #  Add this after status_bar_customization() to make it
        #  non-obvious to override it, hint local_overides()
        #
        if self.t2_env:
            t2_tag = f"T2_ENV {self.prefix_key} "
            self.sb_left = f"#[fg=green,bg=black]{t2_tag}#[default]{self.sb_left}"

        self.filter_me_from_sb_right()

        self.sb_right = self.sb_right.replace(
            "USERNAME_TEMPLATE", self.username_template
        ).replace("HOSTNAME_TEMPLATE", self.hostname_template)

        w(
            f"""
        set -g  status-left "{self.sb_left}"
        set -g  status-right "{self.sb_right}"

        bind -N "Toggle status bar"  t  set status
        """
        )

    def filter_me_from_sb_right(self):
        """Dont display my primary hostname & username."""
        # pylint: disable=subprocess-run-check
        hostname_cmd = subprocess.run(  # nosec
            "hostname | cut -d. -f 1",
            capture_output=True,
            text=True,
            shell=True,  # nosec: B602
        )
        #  No need for labeling my primary workstation
        if hostname_cmd.stdout.strip() == "JacMac":
            self.hostname_template = ""

        #  If its my default account dont show username
        if os.getenv("USER") == "jaclu":
            self.username_template = ""

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
        w(
            'bind -N "Create new session"             +    command-prompt -I "?" '
            '-p "Name of new session: " "new-session -s \\"%%\\""'
        )
        if self.bind_meta:
            w(
                'bind -N "Create new session  - P +"  -n  M-+  command-prompt '
                '-I "?" -p "Name of new session: " "new-session -s \\"%%\\""'
            )
        else:
            w("#  skipping adv keys, if resourced")
            w("unbind -n M-+")
        w()

        w(
            """# session navigation
        bind -N "Select previous session" -r  (  switch-client -p
        bind -N "Select next session"     -r  )  switch-client -n
        bind -N "Switch to last session"      _  switch-client -l"""
        )
        if self.bind_meta:
            w(
                """
            bind -N "Select previous session  - P (" -n  M-(  switch-client -p
            bind -N "Select next session  - P )"     -n  M-)  switch-client -n
            bind -N "Switch to last session  - P _"  -n  M-_  switch-client -l
            """
            )
        else:
            w(
                """#  skipping adv keys, if resourced
            unbind -n  M-(
            unbind -n  M-)
            unbind -n  M-_
            """
            )

        w(
            'bind -N "Rename Session"  S    command-prompt -I "#S" '
            '"rename-session -- \\"%%\\""'
        )

        w(
            'bind -N "Kill session in focus"    M-x  confirm-before -p '
            '"Kill session: #{session_name}? (y/n)"  '
            '"set -s detach-on-destroy off \\; kill-session"'
        )

        w()  # spacer between sections

    def windows_handling(self):
        w = self.write
        w(
            """
        #======================================================
        #
        #   Windows handling
        #
        #======================================================

        set -g  base-index 1
        set-window-option -g aggressive-resize on"""
        )

        if self.vers_ok(1.7):
            #  Renumber windows when a window is closed
            w("set -g  renumber-windows on")

        #
        #  Apps should not be allowed to rename windows
        #
        if self.vers_ok(1.6):
            w("set -g  allow-rename off")

        w(
            """set -wg automatic-rename off

        set -g set-titles on
        set -g set-titles-string "#{host_short} #{session_name}:#{window_name}"
        """
        )

        cmd_new_win_named = (
            'command-prompt -I "?" -p "Name of new window: "'
            ' "new-window -n \\"%%\\" -c \\"#{pane_current_path}\\""'
        )

        for key in ("c", "="):  # c is just for compatibility with default key
            w(f'bind -N "New window"           {key}    {cmd_new_win_named}')
        if self.bind_meta:
            w(f'bind -N "New window  - P =" -n  M-=  {cmd_new_win_named}')
        else:
            w("unbind                      -n  M-=  # skipping adv-key")

        w(
            """
        # window navigation
        bind -N "Previous Window"        -r  9    previous-window
        bind -N "Next Window"            -r  0    next-window
        bind -N "Last Window"                -    last-window"""
        )

        #
        #  Splitting the entire window
        #
        self.split_entire_window_UK()
        #
        #  Same using arrow keys with C-M-S modifier
        #
        if self.vers_ok(2.3) and not self.is_tmate():
            #
            #  tmate does not support split-window -f  despite they claim
            #  to be 2.4 compatible and this is a 2.3 feature...
            #
            if self.bind_meta:
                sw1 = 'bind -N "Split window'  # hackish strings
                sw2 = " split-window -f"  # to make sure
                pcb = '-c "#{pane_current_path}"'  # line is not to long
                w(
                    f"""# window splitting - bind_meta
                {sw1} horizontally left"  -n  C-M-S-Left   {sw2}hb {pcb}
                {sw1} vertically down"    -n  C-M-S-Down   {sw2}v  {pcb}
                {sw1} vertically up"      -n  C-M-S-Up     {sw2}vb {pcb}
                {sw1} horizontally right" -n  C-M-S-Right  {sw2}h  {pcb}
                """
                )
            else:
                w(
                    """#  skipping bind_meta, if resourced
                  unbind -n  C-M-S-Left
                  unbind -n  C-M-S-Down
                  unbind -n  C-M-S-Up
                  unbind -n  C-M-S-Right
                  """
                )

        #
        #  TODO: 220516 Not sure if these work, since I map the keys to
        #               ctrl - P/n in my terminal app, need to
        #               investigate at some point
        #
        if self.bind_meta:
            w(
                """# adv key win nav
            bind -N "Previous window  - P 9" -n  M-9  previous-window
            bind -N "Next window - P 0"      -n  M-0  next-window
            bind -N "Last Window - P -"      -n  M--  last-window"""
            )
            if self.vers_ok(2.1):
                w2 = "window"  # hackish strings to make sure
                cm = "-T copy-mode -n M-"  # line is not to long
                w(
                    f"""# Overide odd behaviour in copy-mode
                  bind -N "Previous {w2}  - P 9" {cm}9  previous-{w2}
                  bind -N "Next {w2} - P 0"      {cm}0  next-{w2}
                  """
                )
        else:
            w(
                """#  skipping adv keys, if resourced
            unbind -n  M-9
            unbind -n  M-0
            unbind -n  M--"""
            )
            if self.vers_ok(2.4):
                # TODO: Why can this be bound but not unbound at 2.1?
                w(
                    """
                  unbind -T copy-mode -n M-9
                  unbind -T copy-mode -n M-0
                  """
                )

        if self.vers_ok(1.8):
            #
            #  Swap window left/right <prefix>  < / >
            #
            w(
                """# window shuffle
            bind -N "Swap window left"         -r  <    swap-window -dt:-1
            bind -N "Swap window right"        -r  >    swap-window -dt:+1"""
            )
            if self.bind_meta:
                w(
                    """
                bind -N "Swap window left  - P <"  -n  M-<  swap-window -dt:-1
                bind -N "Swap window right  - P >" -n  M->  swap-window -dt:+1
                """
                )
            else:
                w(
                    """#  skipping adv keys, if resourced
                unbind -n  M-<
                unbind -n  M->
                """
                )

        else:
            # TODO: bind to < does not take effect, so no swap left warning
            w(
                'bind -N "Swap window right"  >  display "Swap window right '
                'needs 1.8"'
            )

        # if self.vers_ok(2.3) and not self.is_tmate():
        #     #
        #     #  tmate does not support split-window -f  despite they
        #     #  claim to be 2.4 compatible and this is a 2.3 feature...
        #     #
        #     sw = 'bind -N "Split window'       # hackish strings to make sure
        #     pcb = '-c "#{pane_current_path}"'  # line is not to long
        #     w(f"""# window splitting
        #     {sw} horizontally right"  M-L  split-window -fh  {pcb}
        #     {sw} horizontally left"   M-H  split-window -fhb {pcb}
        #     {sw} vertically down"     M-J  split-window -fv  {pcb}
        #     {sw} vertically up"       M-K  split-window -fvb {pcb}
        #     """)

        w("bind -N 'Toggle synchronize'      *   set synchronize-panes")

        w(
            'bind -N "Rename current window"   W  command-prompt -I "#W" '
            '"rename-window -- \\"%%\\""'
        )

        #
        #  If last window of current session is killed, the session
        #  is destroyed and focus is moved to another session
        #
        for c in ("&", "X"):
            w(
                f'bind -N "Kill window in focus"    {c}  confirm-before -p '
                '"kill current window \\"#W\\"? (y/n)" '
                '"set -s detach-on-destroy off \\; kill-window"'
            )
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

        if self.vers_ok(1.6):
            #  Set base index for panes to 1 instead of 0
            w("setw -g pane-base-index 1\n")

        #
        #  Without a sleep in between the actions, history is not cleared.
        #  Just a guess, but most likely clear-history is run before C-l
        #  is handled by the terminal. Thus pushing the current screen
        #  back into history
        #
        w(
            'bind -N "Clear history & screen"    M-l  send-keys C-l \\; '
            'run "sleep 0.3" \\; clear-history'
        )
        w()  # spacer

        #
        #  Save history for current pane, prompts for filename
        #
        #  Save as text              <prefix> M-h
        #  Save with escape codes    <prefix> M-e
        #
        #  When saved with escape code, less/most fails to display
        #  cat history-file will display the included colors correctly.
        #
        home_dir = os.path.expandvars("~")
        w(
            'bind -N "Save history to prompted file name (includes escapes)"  '
            'M-e  command-prompt -p "save history (includes escapes) to:" '
            f'-I "{home_dir}/tmux-e.history" "capture-pane -S - -E - -e ; '
            'save-buffer %1 ; delete-buffer"'
        )
        w(
            'bind -N "Save history to prompted file name (no escapes)"        '
            'M-h  command-prompt -p "save history (no escapes) to:" '
            f'-I "{home_dir}/tmux.history" "capture-pane -S - -E - ;'
            'save-buffer %1 ; delete-buffer"'
        )

        w(
            """
        #  Select, search, delete and even edit(!) paste buffers
        bind -N "Chose paste buffer(-s)"  B  choose-buffer
        """
        )
        w(
            'bind -N "Kill pane in focus"       x  confirm-before -p '
            '"kill-pane #T (#P)? (y/n)" '
            '"set -s detach-on-destroy off \\; kill-pane"'
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
        w = self.write
        w(
            """
        #
        #   ======  Pane frame lines  ======
        #
        """
        )
        #
        #  If you get frame lines drawn as x and q, you need to set
        #  an UTF-8 LANG
        #  sample: export LANG=en_US.UTF-8
        #  You should also be able to solve it by starting tmux with param -u
        #  Finally here is an in tmux hack to solve the pane border issue
        #  set -ga terminal-overrides ',*:enacs@:smacs@:rmacs@:acsc@'
        #

        if self.vers_ok(1.9):
            #
            #  Works both on bright and dark backgrounds
            #
            if self.t2_env:
                #
                #  Make pane splits clearly belong to the T2_ENV
                #
                border_active = "colour119"  # 203 - bright green
                border_other = "colour104"  # 245 - pale lilac
            else:
                #
                #  Ptimary env
                #
                border_active = "colour203"  # 203 - bright orange close to red
                border_other = "colour245"  # 245 - low intensity grey

            w(
                f"""set -g pane-active-border-style fg={border_active}
                  set -g pane-border-style fg={border_other}
            """
            )

        # if self.vers_ok(3.3):
        #     # Needs to wait until a window exists
        #     w(
        #         f'run -b "sleep 1 ; {self.tmux_bin} '
        #         'set pane-border-indicators arrows"\n'
        #     )

        #
        #  Pane title and size
        #
        pane_label = ""
        if self.vers_ok(2.3) and not self.is_tmate():
            if self.show_pane_title:
                pane_label += "#T "
            if self.show_pane_size:
                pane_label += "(#{pane_width}x#{pane_height}) "
            if pane_label:
                pane_label = " " + pane_label  # set initial spacer
                w(f'\nset -g pane-border-format "{pane_label}"')

        if self.vers_ok(2.6):
            if pane_label:
                #
                #  Default label is pane nr
                #
                w(
                    """
                set-hook -g after-split-window  "selectp -T '#D'"
                set-hook -g after-new-session   "selectp -T '#D'"
                set-hook -g after-new-window    "selectp -T '#D'"
                """
                )

                #
                #  Display pane frame lines when
                #   a) more than one pane is present
                #   b) not in a zoomed state
                #
                w(
                    "set-hook -g window-layout-changed "
                    '"set-window -F pane-border-status '
                    '\\"#{?#{==:#{window_panes},1},off,top}\\""'
                )
                w(
                    'set-hook -g after-resize-pane      "run-shell \\"'
                    "if [ #{window_zoomed_flag} -eq 1 ]; then "
                    '$TMUX_BIN set pane-border-status off; fi\\""\n'
                )

            if self.show_pane_title:
                w(
                    'bind -N "Set pane title"  P  command-prompt -p '
                    '"Pane title: " "select-pane -T \\"%%\\""'
                )
        elif self.vers_ok(2.3) and not self.is_tmate():
            w(
                """
            set -g pane-border-status top

            bind  P  display "Pane title setting needs 2.6"
            """
            )

    def pane_navigation(self):
        w = self.write
        w(
            """
        #
        #   ======  Pane Navigation  ======
        #
        """
        )

        if self.bind_meta:
            w(
                """bind -N "Select pane left  - P h"  -n  M-Left   select-pane -L
            bind -N "Select pane right  - P l" -n  M-Right  select-pane -R
            bind -N "Select pane up  - P k"    -n  M-Up     select-pane -U
            bind -N "Select pane down  - P j"  -n  M-Down   select-pane -D
            """
            )
            if self.vers_ok(2.4):
                #
                #  In copy-mode M-Up/Down Scrolls half page, doesn't seem
                #  to be an important feature.
                #  Better to keep them to their normal setting as per above
                #
                w(
                    'bind -N "Select pane up"   -T "copy-mode"  M-Up  '
                    "  select-pane -U"
                )
                w(
                    'bind -N "Select pane down" -T "copy-mode"  M-Down  '
                    "select-pane -D"
                )
        else:
            w(
                """#  skipping adv keys, if resourced
            unbind -n  M-Left
            unbind -n  M-Right
            unbind -n  M-Up
            unbind -n  M-Down"""
            )

        w(
            """#  Rebind without repeat
        bind -N "Select pane up"        Up     select-pane -U
        bind -N "Select pane down"      Down   select-pane -D
        bind -N "Select pane left"      Left   select-pane -L
        bind -N "Select pane right"     Right  select-pane -R"""
        )

        w(
            """
        bind -N "Select pane left"  -r  h      select-pane -L
        bind -N "Select pane right" -r  l      select-pane -R
        bind -N "Select pane up"    -r  k      select-pane -U
        bind -N "Select pane down"  -r  j      select-pane -D
        """
        )

    def pane_splitting(self):
        w = self.write
        w(
            """
        #
        #   ======  Pane Splitting  ======
        #
        """
        )
        #
        #  The defaults just covers splitting the pane right and down.
        #  I am using PgUp/PgDn & Home/End to get a more logical input, and
        #  also to allow left/up splits.
        #

        if self.vers_ok(1.7):
            if self.bind_meta:
                w(
                    'bind -N "Split pane to the right  - P C-l" -n  '
                    'C-M-Right  split-window -h  -c "#{pane_current_path}"'
                )
                w(
                    'bind -N "Split pane below  - P C-j"    -n  '
                    'C-M-Down   split-window -v  -c "#{pane_current_path}"'
                )
                if self.vers_ok(2.0):
                    w(
                        'bind -N "Split pane to the left  - P C-h"  '
                        "-n  C-M-Left   split-window -hb -c "
                        '"#{pane_current_path}"'
                    )
                    w(
                        'bind -N "Split pane above  - P C-k"      '
                        "-n  C-M-Up     split-window -vb -c "
                        '"#{pane_current_path}"'
                    )
                w()
            else:
                w(
                    """#  skipping adv keys, if resourced
                unbind -n  C-M-Right
                unbind -n  C-M-Down
                unbind -n  C-M-Left
                unbind -n  C-M-Up
                """
                )

        w(
            'bind -N "Split pane to the right"  C-l  '
            'split-window -h  -c "#{pane_current_path}"'
        )
        w(
            'bind -N "Split pane below"     C-j  '
            'split-window -v  -c "#{pane_current_path}"'
        )
        if self.vers_ok(2.0):
            w(
                'bind -N "Split pane to the left"   C-h  '
                'split-window -hb -c "#{pane_current_path}"'
            )
            w(
                'bind -N "Split pane above"       C-k  '
                'split-window -vb -c "#{pane_current_path}"'
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
        if self.bind_meta:
            w("bind -N 'Resize pane 1 up  - P K'     -n  M-S-Up     resize-pane -U")
            w("bind -N 'Resize pane 1 down  - P J'   -n  M-S-Down   resize-pane -D")
            w("bind -N 'Resize pane 1 left  - P H'   -n  M-S-Left   resize-pane -L")
            w("bind -N 'Resize pane 1 right  - P L'  -n  M-S-Right  resize-pane -R")
        else:
            w(
                """#  skipping adv keys, if resourced
            unbind -n  M-S-Up
            unbind -n  M-S-Down
            unbind -n  M-S-Left
            unbind -n  M-S-Right"""
            )

        w(
            """
        bind -N "Resize pane 1 up"            -r  K          resize-pane -U
        bind -N "Resize pane 1 down"          -r  J          resize-pane -D
        bind -N "Resize pane 1 left"          -r  H          resize-pane -L
        bind -N "Resize pane 1 right"         -r  L          resize-pane -R
        """
        )
        if self.vers_ok(1.8):
            height_notice = "Pane height"
            if not self.vers_ok(3.3):
                height_notice += " (add 1 for panes next to status bar)"
            w(
                'bind -N "Set pane size (w x h)"  s  command-prompt -p '
                f'"Pane width","{height_notice}" '
                '"resize-pane -x %1 -y %2"'
            )
        else:
            w(
                'bind -N "Navigate not available warning"  s  '
                'display "Set pane size needs 1.8"'
            )

    #
    #  Actions bound to Alt uppercase keys. The iSH console doesn't
    #  generate the correct sequences, so must be remapped via user-keys
    #  Further you need to bind those user keys to the intended action.
    #  To avoid having to repeat code I use special methods handling such
    #  keys, for terminals relaying on user-keys, they can be bound to
    #  the intended action fairly simply.
    #
    def display_plugins_used_UK(self, M_P: str = "M-P"):
        """iSH console doesn't generate correct ALT - Upper Case sequences,
        so when that is the env, intended keys must be bound as user keys.
        To make that without having two separate snippets of code doing
        the same and keeping them in sync, the default parameters are
        the "normal" case, when used for iSH console, the
        user keys will be given
        """
        w = self.write
        if M_P != "M-P":
            note_prefix = "M-P - "
        else:
            note_prefix = ""
        w(
            f'bind -N "{note_prefix}List all plugins defined"  {M_P}  '
            f'run "$TMUX_BIN display \\"Generating response\\" ; {__main__.__file__} {self.conf_file} -p2"'
        )

    def kill_tmux_server_UK(self, M_X: str = "M-X"):
        """iSH console doesn't generate correct ALT - Upper Case sequences,
        so when that is the env, intended keys must be bound as user keys.
        To make that without having two separate snippets of code doing
        the same and keeping them in sync, the default parameters are
        the "normal" case, when used for iSH console, the
        user keys will be given
        """
        w = self.write
        if M_X != "M-X":
            note_prefix = "M-X - "
        else:
            note_prefix = ""
        w(
            f'bind -N "{note_prefix}Kill tmux server"  {M_X}  '
            "confirm-before -p "
            f'"kill tmux server {self.conf_file}? (y/n)" kill-server'
        )

    def split_entire_window_UK(
        self, M_H: str = "M-H", M_J: str = "M-J", M_K: str = "M-K", M_L: str = "M-L"
    ):
        """iSH console doesn't generate correct ALT - Upper Case sequences,
        so when that is the env, intended keys must be bound as user keys.
        To make that without having two separate snippets of code doing
        the same and keeping them in sync, the default parameters are
        the "normal" case, when used for iSH console, the
        user keys will be given
        """
        w = self.write
        if self.vers_ok(2.3) and not self.is_tmate():
            #
            #  tmate does not support split-window -f  despite they claim
            #  to be 2.4 compatible and this is a 2.3 feature...
            #

            #  Some shortcuts to avoid re-typing
            b = 'bind -N "'
            n_base = "Split window "
            sw = "split-window -f"
            pcb = '-c "#{pane_current_path}"'  # line is not to long

            if M_H != "M-H":
                pref = "M-H - "
            else:
                pref = ""
            w(f'{b}{pref}{n_base}horizontally left"   {M_H}  {sw}hb {pcb}')

            if M_J != "M-J":
                pref = "M-J - "
            else:
                pref = ""
            w(f'{b}{pref}{n_base}vertically down"     {M_J}  {sw}v  {pcb}')

            if M_K != "M-K":
                pref = "M-K - "
            else:
                pref = ""
            w(f'{b}{pref}{n_base}vertically up"       {M_K}  {sw}vb {pcb}')

            if M_L != "M-L":
                pref = "M-L - "
            else:
                pref = ""
            w(f'{b}{pref}{n_base}horizontally right"  {M_L}  {sw}h  {pcb}')

    #
    #  Utility methods
    #
    def mkscript_toggle_mouse(self):
        #  The {} encapsulating the script needs to be doubled to escape them
        toggle_mouse_sh = [
            f"""
{self.fnc_toggle_mouse}() {{
    #  This is so much easier to do in a proper script...
    old_state=$($TMUX_BIN show -gv mouse)
    if [ "$old_state" = "on" ]; then
        new_state="off"
    else
        new_state="on"
    fi
    $TMUX_BIN set -g mouse $new_state
    $TMUX_BIN display "mouse: $new_state"
}}"""
        ]
        self.es.create(self.fnc_toggle_mouse, toggle_mouse_sh)

    #
    #  Inspection of tmux-conf version to see if it is compatible
    #
    def check_libs_compatible(self):
        try:
            lib_vers_found = self.lib_version.split()[0]
            # [:len(TMUX_CONF_NEEDED)]
        except AttributeError:
            print()
            print(f"ERROR: Needs tmux_conf lib version: {TMUX_CONF_NEEDED}")
            print("       Failed to read version, probably too old()")
            print()
            sys.exit(1)

        maj_vers_found = ".".join(lib_vers_found.split(".")[:2])
        maj_vers_needed = ".".join(TMUX_CONF_NEEDED.split(".")[:2])

        if maj_vers_found != maj_vers_needed:
            self.incompatible_tmux_conf(
                lib_vers_found,
                "Major version incompatible!",
                f"needs: {maj_vers_needed}",
            )

        min_vers_found = lib_vers_found.split(".")[2]
        min_vers_needed = TMUX_CONF_NEEDED.split(".")[2]
        if min_vers_found < min_vers_needed:
            self.incompatible_tmux_conf(lib_vers_found, "Version to old!")

    def incompatible_tmux_conf(
        self, lib_vers_found: str, reason: str, details: str = ""
    ):
        print()
        print("ERROR: Incompatible tmux-conf package")
        print()
        print(reason)
        if details:
            print()
            print(details)
        print()
        print(f"vers found: {lib_vers_found}   needs: {TMUX_CONF_NEEDED}")
        sys.exit(1)


if __name__ == "__main__":
    BaseConfig().run()
