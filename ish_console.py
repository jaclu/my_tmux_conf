#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  Changes needed if this runs on the iSH console
#
#  This checks if the session running this originates from an iSH node.
#  The iSH console has a very limited keyboard, very few keys are
#  defined, and most of the ALT keys are incorrect. So here ALT
#  uppercase is remapped and things bound to such keys are overridden to
#  use redefined keys, since a key configured to send the correct
#  sequence to applications inside tmux will not trigger actions bound
#  to those keys.
#
#  Find key codes using for example:  showkey -a and examine the output
#  in the 2nd collumn (octal)
#

# pylint: disable=C0116

"""Checks if this is run on the iSH console"""

import os
import sys

import base_config
from mtc_utils import IS_ISH, IS_ISH_AOK

NAV_KEY_HANDLED_TAG = "TMUX_HANDLING_ISH_NAV_KEY"

#
#  To make it easier to identify what keyboard to config
#  the names here match what you see in Bluetooth settings
#
#  Some don't seem to need any specific settings, and do fine
#  by just defining their nav key using the AOK nav_keys.sh
#  This goes for Keyboad names:
#    Omnitype
#
#  Brydge issues
#  M-+ works on regular Brydge, on Brydge prints ±
#  M-< fails to map special-key 35, inside tmux prints ¯ generates \302\257

#  Check base.py - search for switch-client -l - defined twice!!
#

# in use
KBD_LOGITECH_COMBO_TOUCH = "Logitech Combo Touch"
KBD_BRYDGE_10_2_MAX = "Brydge 10.2 MAX+"

# KBD_BRYDGE_10_2_ESC = "Brydge 10.2 MAX+ esc"
# KBD_YOOZON3 = "Yoozon 3"  # same as brydge
# KBD_OMNITYPE = "Omnitype Keyboard"
# KBD_BLUETOOTH = "Bluetooh Keyboard"  # sadly generic name


class IshConsole(base_config.BaseConfig):
    """When running tmux from an iSH console this redefines the rather
    limited keyboard in order to make it more useful.

    Groupings of userkeys

      1-60  Alt Upper case
    100-129 Function keys
    200     Navkey
    210-219 General keyboard bindings
    220-    Specific Keyboard bindings

    If ISH_NAV_KEY is defined and not "None" use it
    """

    is_ish_console = False
    ic_keyboard = None
    # aok_nav_key_handling = "/etc/opt/AOK/tmux_nav_key_handling"
    # aok_nav_key = "/etc/opt/AOK/tmux_nav_key"
    ish_nav_key = None

    usr_key_meta_plus = "User211"

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
        print("Using IshConsole()")
        super().__init__(
            parse_cmd_line=parse_cmd_line,
            conf_file=conf_file,
            tmux_bin=tmux_bin,
            tmux_version=tmux_version,
            replace_config=replace_config,
            clear_plugins=clear_plugins,
            plugins_display=plugins_display,
        )
        # set to defaults, in case a keyb doesnt rebind the key
        self.muc_plus = "M-+"
        self.muc_par_open = "M-("
        self.muc_par_close = "M-)"
        self.muc_underscore = "M-_"

    def content(self):
        # Map special keys before generating rest of conf
        self.ic_detect_console_keyb()
        super().content()

    def ic_detect_console_keyb(self) -> None:
        #
        #  Only use this if the following conditions are met:
        #     1) tmux >= 2.6
        #     2) kernel is ish
        #     3) not an ssh session,
        #     3) keyboard remappings not handled by an outer tmux
        #
        if not self.vers_ok(2.6):
            print("WARNING: tmux < 2.6 does not support user-keys, thus handling")
            print("         keyboard adaptions not supported on this version")
            return

        if (not IS_ISH) or os.environ.get("SSH_CONNECTION"):
            #
            #  This c is only relevant on the iSH console itself
            #  and if no outer tmux is already handling the nav keys
            #
            return

        if NAV_KEY_HANDLED_TAG in os.environ:
            print("iSH console nav key already handled by outer tmux!")
            return
        self.ic_keyboard = os.environ.get("LC_KEYBOARD")
        self.is_ish_console = True
        print("This is an iSH console, keyboard adoptions will be implemented")
        # host_name = run_shell("hostname -s").lower()
        # print(f"hostname: {host_name}")
        # if host_name in ("jacpad", "jacpad-aok"):
        #     self.ic_keyboard = KBD_LOGITECH_COMBO_TOUCH
        # elif host_name in ("pad5", "pad5-aok"):
        #     self.ic_keyboard = KBD_BRYDGE_10_2_ESC
        # else:
        #     sys.exit(
        #         f"ERROR: Style already assiged as: {self.style}, "
        #         f"Can not use style: {this_style}"
        #     )
        #     self.ic_keyboard = None

        self.write(
            f"""
            #======================================================
            #
            #  Remap keys for limited console
            #  using keyboard: {self.ic_keyboard}
            #
            #======================================================
            """
        )

        if self.ic_keyboard == KBD_LOGITECH_COMBO_TOUCH:
            self.ic_keyb_type_combo_touch()
        elif self.ic_keyboard == KBD_BRYDGE_10_2_MAX:
            self.ic_keyb_type_1()
        # elif self.ic_keyboard in (
        #     KBD_BRYDGE_10_2_ESC,
        #     KBD_OMNITYPE,
        #     KBD_BLUETOOTH,
        # ):
        #     self.ic_keyb_type_2()
        else:
            msg = f"Unrecognized LC_KEYBOARD: {self.ic_keyboard}"
            self.write(msg)
            print(msg)
            sys.exit(1)  # f"ERROR: Unknown LC_KEYBOARD: {self.ic_keyboard}")

        self.ic_common_setup()

    #
    #  Specific Keyboards
    #
    def ic_keyb_type_1(self):
        #
        #  General settings seems to work for several keyboards
        #
        self.ic_virtual_escape_key("\\302\\247")
        # both S-§ and M-+ generate this key
        # Since M-+ is used, just ignore S-§ also triggering this feature
        self.write('set -s user-keys[220]  "\\302\\261"')  # ±
        self.muc_plus = "User220"

    def ic_keyb_type_2(self):
        #
        #  General generating Esc directly
        #
        w = self.write
        esc_key = "\\033"
        self.ic_nav_key_prefix(esc_key)

        w(
            """
        #
        #  Send ~ by shifting the "Escape key"
        #  Send back-tick by shifting it the key the 2nd time, ie
        #  pressing what normally would be ~ in order not to collide
        #  with Escape
        #
        set -s user-keys[220]  "\\176"
        bind -N "Enables ~" -n User220 send '~'
        bind -T escPrefix -N "Send backtick"  User220  send "\\`"
        """
        )

    def ic_keyb_type_combo_touch(self):
        #
        #  Logitech Combo Touch
        #
        self.ic_keyb_type_1()
        #
        #  On this keyb, in iSH back-tick sends Escape
        #  this changes it back, Esc is available via §
        #
        self.write(
            """
        set -s user-keys[221]  "\\033"
        bind -N "Send backtick"  -n User221  send "\\`" # map backtick back from Escape
        """
        )

    def ic_virtual_escape_key(self, esc_key: str) -> None:
        self.write(
            f"""#
                #  Virtual Escape key
                #
                set -s user-keys[201]  "{esc_key}"
                bind -N "Send Escape" -n User201  send Escape
                """
        )

    def NOT_ic_nav_key_prefix(self, prefix_key, esc_key="", prefix_comment="") -> None:
        # Only set esc_key, if different from prefix
        w = self.write
        print(f"Assuming keyboard is: {self.ic_keyboard}")

        if prefix_comment:
            prefix_comment = f"# {prefix_comment}"

        if self.vers_ok(2.1):
            tbl_opt = "T"
        else:
            tbl_opt = "t"

        s = f"-{tbl_opt} navPrefix  {prefix_comment}"
        w(
            f"""#
        #  Handle Prefix key
        #
        set -s user-keys[200]  "{prefix_key}"
        bind -N "Switch to -T navPrefix" -n User200 switch-client {s}
        """
        )
        if esc_key:
            w(
                f"""#
                #  Virtual Escape key
                #
                set -s user-keys[201]  "{esc_key}"
                bind -N "Send Escape" -n User201  send Escape
                """
            )
        else:
            # Double tap for actual Esc
            w("bind -T navPrefix -N 'Send Escape'  User200  send Escape")
        if IS_ISH_AOK:
            w(
                """#
            #  Use shift-arrows for navigation
            #
            bind -N "Send PageUp" -n  S-Up     send-keys PageUp
            bind -N "Send PageDown" -n  S-Down   send-keys PageDown
            bind -N "Send Home" -n  S-Left   send-keys Home
            bind -N "Send End" -n  S-Right  send-keys End
            """
            )
        else:
            w(
                f"""#
            #  Use nav prefix for navigation
            #
            bind -T navPrefix  -N "Send PageUp" Up       send PageUp
            bind -T navPrefix  -N "Send PageDown" Down     send PageDown
            bind -T navPrefix  -N "Send Home" Left     send Home
            bind -T navPrefix  -N "Send End" Right    send End
            #
            #  Indicates this tmux is handling ISH_NAV_KEY, to ensure
            #  nested tmuxes, dont parse it again.
            #
            {NAV_KEY_HANDLED_TAG}=1
            """
            )

    def ic_common_setup(self) -> None:
        #
        #  Since iSH console is limited to only M-numbers and M-S-numbers
        #  I use M-S-number for function keys normally, thus not being
        #  able to use keys like M-(
        #  To avoid this collision, set fn_keys_mapped accordingly
        #
        #  This does general iSH mapping, not focusing on keyboard specific
        #  customization needs
        #
        self.write(
            """
        #
        #  General Keyboard bindings
        #
        #  € is Option+Shift+2 in United States layout
        set -s user-keys[210]  "\\342\\202\\254" # Usually: €
        bind -N "Enables €" -n User210 send '€'
        """
        )
        #
        #  Some keybs have issues with M-<
        #  the initial binding for this char
        #  instead triggers it to send this sequence
        #  Weird, but this seems to solve it
        #
        # set -s user-keys[211]  "\\302\\257"
        # bind -N "Enables M-<" -n User211 send "M-<"
        self.ic_fn_keys()
        self.ic_alt_upper_case(fn_keys_mapped=True)

    def ic_fn_keys(self) -> None:
        self.ic_m_fn_keys()

    def ic_m_fn_keys(self) -> None:
        w = self.write
        w(
            """
        #
        #  This will map M-S number to F1 - F10
        #
        set -s user-keys[101] "\\33\\061"  #  M-1
        set -s user-keys[102] "\\33\\062"  #  M-2
        set -s user-keys[103] "\\33\\063"  #  M-3
        set -s user-keys[104] "\\33\\064"  #  M-4
        set -s user-keys[105] "\\33\\065"  #  M-5
        set -s user-keys[106] "\\33\\066"  #  M-6
        set -s user-keys[107] "\\33\\067"  #  M-7
        set -s user-keys[108] "\\33\\070"  #  M-8
        set -s user-keys[109] "\\33\\071"  #  M-9
        set -s user-keys[110] "\\33\\060"  #  M-0
        """
        )
        for i in range(1, 10):
            w(f'bind -N "M-{i} -> F{i}"  -n  User10{i}  send-keys F{i}')
        w('bind -N "M-0 -> F10" -n  User110  send-keys F10')

    def ic_ms_fn_keys(self) -> None:
        w = self.write
        w(
            """
        #
        #  This will map M-S number to F1 - F10
        #
        set -s user-keys[101] "\\342\\201\\204"  #  M-S-1
        set -s user-keys[102] "\\342\\202\\254"  #  M-S-2
        set -s user-keys[103] "\\342\\200\\271"  #  M-S-3
        set -s user-keys[104] "\\342\\200\\272"  #  M-S-4
        set -s user-keys[105] "\\357\\254\\201"  #  M-S-5
        set -s user-keys[106] "\\357\\254\\202"  #  M-S-6
        set -s user-keys[107] "\\342\\200\\241"  #  M-S-7
        set -s user-keys[108] "\\302\\260"       #  M-S-8
        set -s user-keys[109] "\\302\\267"       #  M-S-9
        set -s user-keys[110] "\\342\\200\\232"  #  M-S-0
        """
        )
        for i in range(1, 10):
            w(f'bind -N "M-S-{i} -> F{i}"  -n  User10{i}  send-keys F{i}')
        w('bind -N "M-S-0 -> F10" -n  User110  send-keys F10')

    def ic_alt_upper_case(self, fn_keys_mapped: bool) -> None:
        w = self.write
        w(
            """
        #
        #  iSH console doesn't generate the right keys for
        #  Alt upper case chars, so here they are defined
        #
        set -s user-keys[1]   "\\303\\205"       #  M-A
        set -s user-keys[2]   "\\304\\261"       #  M-B
        set -s user-keys[3]   "\\303\\207"       #  M-C
        set -s user-keys[4]   "\\303\\216"       #  M-D
        set -s user-keys[5]   "\\302\\264"       #  M-E
        set -s user-keys[6]   "\\303\\217"       #  M-F
        set -s user-keys[7]   "\\313\\235"       #  M-G
        set -s user-keys[8]   "\\303\\223"       #  M-H
        set -s user-keys[9]   "\\313\\206"       #  M-I
        set -s user-keys[10]  "\\303\\224"       #  M-J
        set -s user-keys[11]  "\\357\\243\\277"  #  M-K
        set -s user-keys[12]  "\\303\\222"       #  M-L
        set -s user-keys[13]  "\\303\\202"       #  M-M
        set -s user-keys[14]  "\\313\\234"       #  M-N
        set -s user-keys[15]  "\\303\\230"       #  M-O
        set -s user-keys[16]  "\\342\\210\\217"  #  M-P
        set -s user-keys[17]  "\\305\\222"       #  M-Q
        set -s user-keys[18]  "\\341\\200\\260"  #  M-R
        set -s user-keys[19]  "\\303\\215"       #  M-S
        set -s user-keys[20]  "\\313\\207"       #  M-T
        set -s user-keys[21]  "\\302\\250"       #  M-U
        set -s user-keys[22]  "\\342\\227\\212"  #  M-V
        set -s user-keys[23]  "\\342\\200\\236"  #  M-W
        set -s user-keys[24]  "\\313\\233"       #  M-X
        set -s user-keys[25]  "\\303\\201"       #  M-Y
        set -s user-keys[26]  "\\302\\270"       #  M-Z

        set -s user-keys[30]  "\\342\\200\\235"  # M-{
        set -s user-keys[31]  "\\342\\200\\231"  # M-}
        set -s user-keys[32]  "\\303\\232"       # M-:
        set -s user-keys[33]  "\\303\\206"       # M-\"
        set -s user-keys[34]  "\\302\\273"       # M-\\
        set -s user-keys[35]  "\\302\\257"       # M-<
        set -s user-keys[36]  "\\313\\230"       # M->
        set -s user-keys[37]  "\\302\\277"       # M-?
        set -s user-keys[38]  "\\342\\200\\224"  # M-_
        """
        )
        # set -s user-keys[39]  "\\302\\261"       # M-+
        # set -s user-keys[39]  "\\176"     # brydge generates ~ inside tmux

        for i, c in (
            ("1", "A"),
            ("2", "B"),
            ("3", "C"),
            ("4", "D"),
            ("5", "E"),
            ("6", "F"),
            ("7", "G"),
            ("8", "H"),
            ("9", "I"),
            ("10", "J"),
            ("11", "K"),
            ("12", "L"),
            ("13", "M"),
            ("14", "N"),
            ("15", "O"),
            ("16", "P"),
            ("17", "Q"),
            ("18", "R"),
            ("19", "S"),
            ("20", "T"),
            ("21", "U"),
            ("22", "V"),
            ("23", "W"),
            ("24", "X"),
            ("25", "Y"),
            ("26", "Z"),
            ("30", "{"),
            ("31", "}"),
            ("32", ":"),
            ("33", '\\"'),
            ("34", "|"),
            #  Fails on Omnitype, Yoozon3
            #  ends up generating:
            # ¯
            # 194 0302 0xc2
            # 175 0257 0xaf
            # ("35", "<"), - used in self.auc_swap_window()
            # ("36", ">"), - used in self.auc_swap_window()
            ("37", "?"),
            # Doesn't work on Omnitype Keyboard, works on Yoozon3
            ("38", "_"),
            # Doesn't work on Omnitype,Yoozon3, generates ~
            # ("39", "+"),
        ):
            if c == "N":
                #  Special case to avoid cutof at second -N
                #  on tmux < 3.1
                w(f"bind -N 'Enables M-N' -n  User{i}  send M-{c}")
            else:
                w(f'bind -N "Enables M-{c}" -n  User{i}  send "M-{c}"')

        if not fn_keys_mapped:
            #  Collides with F1 - F10 remapping
            w(
                """
            set -s user-keys[51]  "\\342\\201\\204"  # M-!
            set -s user-keys[52]  "\\342\\202\\254"  # M-@
            set -s user-keys[53]  "\\342\\200\\271"  # M-#
            set -s user-keys[54]  "\\342\\200\\272"  # M-$
            set -s user-keys[55]  "\\357\\254\\201"  # M-%
            set -s user-keys[56]  "\\357\\254\\202"  # M-^
            set -s user-keys[57]  "\\342\\200\\241"  # M-&
            set -s user-keys[58]  "\\302\\260"       # M-*
            set -s user-keys[59]  "\\302\\267"       # M-(
            set -s user-keys[60]  "\\342\\200\\232"  # M-)
            """
            )
            self.muc_par_open = "User59"
            self.muc_par_close = "User60"

            for i, c in (
                ("51", "!"),
                ("52", "@"),
                ("53", "#"),
                ("54", "$"),
                ("55", "%"),
                ("56", "^"),
                ("57", "&"),
                ("58", "*"),
                ("59", "("),
                ("60", ")"),
            ):
                w(f'bind -N "Enables M-{c}" -n  User{i}  send "M-{c}"')
        w()

        #
        #  AAARRGH
        #  User-keys aren't parsed by tmux if they are bound to
        #  send-keys. If the resulting key has an action,
        #  we need to override and bind the user-key to this action.
        #
        # self.auc_split_entire_window(
        #     m_h="User8", m_j="User10", m_k="User11", m_l="User12"
        # )
        # self.auc_display_plugins_used(m_p="User16")
        # self.auc_kill_tmux_server(m_x="User24")
        # self.auc_swap_window(m_less_than="User35", m_greater_than="User36")
        # self.auc_meta_ses_handling(
        #     m_plus=self.usr_key_meta_plus,
        #     muc_par_open=muc_par_open,
        #     muc_par_close=muc_par_close,
        #     m_underscore="User38",
        # )

        w(
            """
        #
        # Alt - HJKL splits pane
        #"""
        )
        #
        #  Do these one line at a time, in order for the source to be
        #  more readable
        #
        w(
            'bind -N "Split pane to the right" -n  User12  '
            'split-window -h  -c "#{pane_current_path}"'
        )
        w(
            'bind -N "Split pane below"        -n  User10  '
            'split-window -v  -c "#{pane_current_path}"'
        )
        if self.vers_ok("2.0"):
            w(
                'bind -N "Split pane to the left"  -n  User8   '
                'split-window -hb -c "#{pane_current_path}"'
            )
            w(
                'bind -N "Split pane above"        -n  User11  '
                'split-window -vb -c "#{pane_current_path}"'
            )

    #  Not used stuff
    #
    # def ic_nav_key_mod(self, mod_char: str) -> None:
    #     self.write(
    #         f"""
    #     bind -N "S-Up = PageUp"     -n  {mod_char}-Up     send-keys PageUp
    #     bind -N "S-Down = PageDown" -n  {mod_char}-down   send-keys PageDown
    #     bind -N "S-Left = Home"     -n  {mod_char}-Left   send-keys Home
    #     bind -N "S-Right = End"     -n  {mod_char}-Right  send-keys End
    #     """
    #     )

    #
    #  Overrides for things defining shifted meta chars
    #
    def auc_meta_ses_handling(  # used by iSH Console
        self,
        muc_plus: str = "M-+",
        muc_par_open: str = "M-(",
        muc_par_close: str = "M-)",
        muc_underscore: str = "M-_",
    ):
        # doesnt seem possible to use self.variables as defaults...
        if self.muc_plus != "M-+":
            muc_plus = self.muc_plus
        if self.muc_par_open != "M-(":
            muc_par_open = self.muc_par_open
        if self.muc_par_close != "M-)":
            muc_par_close = self.muc_par_close
        if self.muc_underscore != "M-)":
            muc_underscore = self.muc_underscore
        super().auc_meta_ses_handling(
            muc_plus, muc_par_open, muc_par_close, muc_underscore
        )

    def auc_swap_window(  # used by iSH Console
        self, muc_less_than: str = "User35", muc_greater_than: str = "User36"
    ):
        super().auc_swap_window(muc_less_than, muc_greater_than)

    def auc_display_plugins_used(self, muc_p: str = "User16"):  # used by iSH Console
        super().auc_display_plugins_used(muc_p)

    def auc_kill_tmux_server(self, muc_x: str = "User24"):  # used by iSH Console
        super().auc_kill_tmux_server(muc_x)  # used by iSH Console

    def auc_split_entire_window(
        self, muc_h="User8", muc_j="User10", muc_k="User11", muc_l="User12"
    ):
        super().auc_split_entire_window(muc_h, muc_j, muc_k, muc_l)


#
#  If this is run directly
#
if __name__ == "__main__":
    IshConsole().run()
