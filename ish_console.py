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
#  defined, and most of the shifted alt keys are incorrect. So here ALT
#  uppercase is remapped and things bound to such keys are overridden to
#  use redefined keys, since a key configured to send the correct
#  sequence to applications inside tmux will not trigger actions bound
#  to those keys.
#
#  Find key codes using for example:  showkey -a and examine the output
#  in the 2nd collumn (octal) rememer to 0 pad all numbers to three digits
#

# pylint: disable=C0116

"""Checks if this is run on the iSH console"""

import os
import sys

import base_config

#
#  To make it easier to identify what keyboard to config
#  the names here match what you see in Bluetooth settings when listed
#  otherwise just the deviced product name.
#  They are defined in the env based on hostname in ~/.common_rc
#

# in use
KBD_LOGITECH_COMBO_TOUCH = "Logitech Combo Touch"
KBD_BRYDGE_10_2_MAX = "Brydge 10.2 MAX+"
KBD_YOOZON3 = "Yoozon 3"  # same as brydge
KBD_OMNITYPE = "Omnitype Keyboard"
KBD_BLUETOOTH = "Bluetooh Keyboard"  # sadly generic name


class IshConsole(base_config.BaseConfig):
    """When running tmux from an iSH console this redefines the rather
    limited keyboard in order to make it more useful.

    Groupings of userkeys

      1-60  Alt Upper case
    100-129 Function keys
    200     Escape
    201     Navkey - no longer used
    210-219 General keyboard bindings
    220-    Specific Keyboard bindings

    If ISH_NAV_KEY is defined and not "None" use it
    """

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

    def content(self):
        # Map special keys before generating rest of conf
        self.ic_detect_console_keyb()
        super().content()

    def ic_detect_console_keyb(self) -> None:
        #
        #  Only use this if the following conditions are met:
        #     1) tmux >= 2.6
        #     2) LC_KEYBOARD is set
        #
        if not self.vers_ok(2.6):
            print("WARNING: tmux < 2.6 does not support user-keys, thus handling")
            print("         keyboard adaptions not supported on this version")
            return

        self.ic_keyboard = os.environ.get("LC_KEYBOARD")
        if not self.ic_keyboard:
            print("WARNING: IshConsole() was used without LC_KEYBOARD being set")
            print("         base.py should not have used this class")
            return

        self.is_ish_console = True
        print(f"This originated on an iSH console - keyboard: {self.ic_keyboard}")
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

        if self.ic_keyboard in (KBD_OMNITYPE, KBD_BLUETOOTH):
            # already handles esc
            self.ic_keyb_type_1()
        elif self.ic_keyboard in (KBD_BRYDGE_10_2_MAX, KBD_YOOZON3):
            self.ic_keyb_type_2()
        elif self.ic_keyboard == KBD_LOGITECH_COMBO_TOUCH:
            self.ic_keyb_type_combo_touch()
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
        #  This keyb type generates Esc on the backtick, backtick is done
        #  using C-backtick
        #
        pass

    def ic_keyb_type_2(self):
        #
        #  General settings seems to work for several keyboards
        #
        self.ic_virtual_escape_key("\\302\\247")

    def ic_keyb_type_combo_touch(self):
        #
        #  Logitech Combo Touch
        #
        self.ic_keyb_type_2()  # Same esc handling
        #
        #  On this keyb, in backtick sends Escape
        #  this changes it back to send backtick, Esc is available via §
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
                set -s user-keys[200]  "{esc_key}"
                bind -N "Send Escape" -n User200  send Escape
                """
        )

    def ic_common_setup(self) -> None:
        #
        #  This does general iSH mapping, not focusing on keyboard specific
        #  customization needs
        #

        #
        # Move this to base_config ?
        #
        # self.write(
        #     """
        # #
        # #  General Keyboard bindings
        # #
        # #  € is Option+Shift+2 in United States layout
        # on regular pc keyb: "\\033\\100" # M-@
        # on ish console:  "\\342\\202\\254"
        # bind -N "Enables €" -n User210 send '€'
        # """
        # )

        #
        #  Some keybs have issues with M-<
        #  the initial binding for this char
        #  instead triggers it to send this sequence
        #  Weird, but this seems to solve it
        #
        # set -s user-keys[211]  "\\302\\257"
        # bind -N "Enables M-<" -n User211 send "M-<"

        ms_fn_keys_mapped = False

        fn_keys_handling = 0
        if fn_keys_handling == 0:
            # no function keys mapping
            pass
        elif fn_keys_handling == 1:
            self.ic_fn_keys()
        elif fn_keys_handling == 2:
            self.ic_m_fn_keys()
        elif fn_keys_handling == 3:
            ms_fn_keys_mapped = True
            self.ic_ms_fn_keys()

        self.ic_alt_upper_case(ms_fn_keys_mapped)

    def ic_fn_keys(self):
        #
        #  For keybs that already handles M-#
        #  this just binds them to send F#
        #
        w = self.write
        for i in range(1, 10):
            w(f'bind -N "M-{i} -> F{i}"  -n  M-{i}  send-keys  F{i}')
        w('bind -N "M-0 -> F10" -n  M-0  send-keys  F10')

    def ic_m_fn_keys(self) -> None:
        w = self.write
        w(
            """
        #
        #  This will map M-number to F1 - F10
        #
        set -s user-keys[101] "\\033\\061"  #  M-1
        set -s user-keys[102] "\\033\\062"  #  M-2
        set -s user-keys[103] "\\033\\063"  #  M-3
        set -s user-keys[104] "\\033\\064"  #  M-4
        set -s user-keys[105] "\\033\\065"  #  M-5
        set -s user-keys[106] "\\033\\066"  #  M-6
        set -s user-keys[107] "\\033\\067"  #  M-7
        set -s user-keys[108] "\\033\\070"  #  M-8
        set -s user-keys[109] "\\033\\071"  #  M-9
        set -s user-keys[110] "\\033\\060"  #  M-0
        """
        )
        for i in range(1, 10):
            w(f'bind -N "M-{i} -> F{i}"  -n  User10{i}  send-keys F{i}')
        w('bind -N "M-0 -> F10" -n  User110  send-keys  F10')

    def ic_ms_fn_keys(self) -> None:
        w = self.write
        w(
            """
        #
        #  This will map M-S-number to F1 - F10
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

    def ic_alt_upper_case(self, ms_fn_keys_mapped: bool = False) -> None:
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

        set -s user-keys[60]  "\\342\\200\\224"  # M-_

        # On some keybs with a § there is a glitch in that
        # both S-§ and M-+ generate ±. Since M-+ is used, and S-§ not,
        # just ignore that S-§ also triggers this feature
        set -s user-keys[61] "\\302\\261"       # M-+

        set -s user-keys[62]  "\\342\\200\\235" # M-{
        set -s user-keys[63]  "\\342\\200\\231" # M-}
        set -s user-keys[64]  "\\302\\273"      # M-|
        set -s user-keys[65]  "\\303\\232"      # M-:
        set -s user-keys[66]  "\\303\\206"      # M-\"
        set -s user-keys[67]  "\\302\\257"      # M-<
        set -s user-keys[68]  "\\313\\230"      # M->
        set -s user-keys[69]  "\\302\\277"      # M-?
        """
        )

        for i, c in (
            ("1", "A"),
            ("2", "B"),
            ("3", "C"),
            ("4", "D"),
            ("5", "E"),
            ("6", "F"),
            ("7", "G"),
            # ("8", "H"), -  used in  auc_split_entire_window()
            ("9", "I"),
            # ("10", "J"), - used in  auc_split_entire_window()
            # ("11", "K"), - used in  auc_split_entire_window()
            # ("12", "L"), - used in  auc_split_entire_window()
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
            # ("60", "_"), - used in  auc_meta_ses_handling()
            # ("61", "+"), - used in  auc_meta_ses_handling()
            ("62", "{"),
            ("63", "}"),
            ("64", "|"),
            ("65", ":"),
            ("66", '\\"'),
            # ("67", "<"), - used in  auc_swap_window()
            # ("68", ">"), - used in  auc_swap_window()
            ("69", "?"),
            # Doesn't work on Omnitype Keyboard, works on Yoozon3
        ):
            if c == "N":
                #  Special case to avoid cutof at second -N
                #  on tmux < 3.1
                w(f"bind -N 'Enables M-N' -n  User{i}  send M-{c}")
            else:
                w(f'bind -N "Enables M-{c}" -n  User{i}  send "M-{c}"')

        if not ms_fn_keys_mapped:
            #  Collides with F1 - F10 remapping
            w(
                """
            set -s user-keys[80]  "\\342\\200\\232"  # M-)
            set -s user-keys[81]  "\\342\\201\\204"  # M-!
            set -s user-keys[82]  "\\342\\202\\254"  # M-@
            set -s user-keys[83]  "\\342\\200\\271"  # M-#
            set -s user-keys[84]  "\\342\\200\\272"  # M-$
            set -s user-keys[85]  "\\357\\254\\201"  # M-%
            set -s user-keys[86]  "\\357\\254\\202"  # M-^
            set -s user-keys[87]  "\\342\\200\\241"  # M-&
            set -s user-keys[88]  "\\302\\260"       # M-*
            set -s user-keys[89]  "\\302\\267"       # M-(
            """
            )
            for i, c in (
                # ("80", ")"), - used in  auc_meta_ses_handling()
                ("81", "!"),
                ("82", "@"),
                ("83", "#"),
                ("84", "$"),
                ("85", "%"),
                ("86", "^"),
                ("87", "&"),
                ("88", "*"),
                # ("89", "("), - used in  auc_meta_ses_handling()
            ):
                w(f'bind -N "Enables M-{c}" -n  User{i}  send "M-{c}"')
        w()

        #
        #  AAARRGH
        #  User-keys aren't parsed by tmux if they are bound to
        #  send-keys. If the resulting key has an action,
        #  we need to override and bind the user-key to this action.
        #  this is handled by the auc_ methods
        #

    #
    #  Overrides for things using shifted meta chars
    #
    def auc_meta_ses_handling(  # used by iSH Console
        self,
        muc_plus: str = "User61",
        muc_par_open: str = "User89",
        muc_par_close: str = "User80",
        muc_underscore: str = "User60",
    ):
        super().auc_meta_ses_handling(
            muc_plus=muc_plus,
            muc_par_open=muc_par_open,
            muc_par_close=muc_par_close,
            muc_underscore=muc_underscore,
        )

    def auc_swap_window(  # used by iSH Console
        self, muc_less_than: str = "User67", muc_greater_than: str = "User68"
    ):
        super().auc_swap_window(muc_less_than, muc_greater_than)

    def auc_display_plugins_used(self, muc_s_p: str = "User16"):  # used by iSH Console
        super().auc_display_plugins_used(muc_s_p)

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
