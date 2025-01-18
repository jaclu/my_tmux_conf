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
#  in the 2nd column (octal) remember to 0 pad all numbers to three digits
#

# pylint: disable=C0116

"""Checks if this is run on the iSH console"""

import sys

import mtc_utils

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
KBD_BLUETOOTH = "Bluetooth Keyboard"  # sadly generic name


class TabletBtKbd:
    """When running tmux from an iSH console this redefines the rather
    limited keyboard in order to make it more useful.

    Groupings of user-keys

      1-60  Alt Upper case
    100-129 Function keys
    180-190 Handled by base.py
    200     Escape
    201     Navkey - no longer used
    210-219 General keyboard bindings
    220-    Specific Keyboard bindings
    """

    ic_keyboard = None

    # pylint: disable=too-many-positional-arguments,too-many-arguments
    def __init__(self, tmux_conf_instance):
        self.tc = tmux_conf_instance
        print("Using TabletBtKbd() class")

        self.tc.muc_defaults = {
            "muc_plus": "User61",
            "muc_par_open": "User89",
            "muc_par_close": "User80",
            "muc_underscore": "User60",
            "muc_s_p": "User16",
            "muc_x": "User24",
            "muc_h": "User8",
            "muc_j": "User10",
            "muc_k": "User11",
            "muc_l": "User12",
        }

    # def content(self):
    #     # Map special keys before generating rest of conf
    #     self.ic_detect_console_keyb()

    def ic_detect_console_keyb(self) -> bool:
        #
        #  Only use this if the following conditions are met:
        #     1) tmux >= 2.6
        #     2) LC_KEYBOARD is set
        #
        if not mtc_utils.LC_KEYBOARD:
            print("WARNING: TabletBtKbd() was used without LC_KEYBOARD being set")
            return False

        if not self.tc.vers_ok(2.6):
            print("WARNING: tmux < 2.6 does not support user-keys, thus handling")
            print("         keyboard adaptions not supported on this version")
            return False

        # use <prefix> arrows as PageUp/Dn Home/End
        self.tc.use_ish_prefix_arrow_nav_keys = True

        print(f"This originated on an iSH console - keyboard: {mtc_utils.LC_KEYBOARD}")
        self.tc.write(
            f"""
            #======================================================
            #
            #  Remap keys for limited console
            #  using keyboard: {mtc_utils.LC_KEYBOARD}
            #
            #======================================================
            """
        )

        if mtc_utils.LC_KEYBOARD in (KBD_OMNITYPE, KBD_BLUETOOTH):
            # already handles esc
            self.ic_keyb_type_1()
        elif mtc_utils.LC_KEYBOARD in (KBD_BRYDGE_10_2_MAX, KBD_YOOZON3):
            self.ic_keyb_type_2()
        elif mtc_utils.LC_KEYBOARD == KBD_LOGITECH_COMBO_TOUCH:
            self.ic_keyb_type_combo_touch()
        else:
            msg = f"Unrecognized LC_KEYBOARD: {mtc_utils.LC_KEYBOARD}"
            self.tc.write(msg)
            print(msg)
            sys.exit(1)  # f"ERROR: Unknown LC_KEYBOARD: {mtc_utils.LC_KEYBOARD}")

        self.ic_common_setup()
        return True

    #
    #  Specific Keyboards
    #
    def ic_keyb_type_1(self):
        #
        #  This keyb type already generates Esc on the key above tab
        #
        self.tc.euro_fix("\\342\\202\\254")

    def ic_keyb_type_2(self):
        #
        #  General settings seems to work for several keyboards
        #
        self.ic_virtual_escape_key("\\302\\247")

    def ic_keyb_type_combo_touch(self):
        #
        #  Logitech Combo Touch
        #
        #
        self.ic_keyb_type_2()  # Same esc handling
        self.tc.euro_fix("\\342\\202\\254")
        self.tc.write(
            """#
            #  On this keyb, backtick (next to z) sends Escape
            #  this changes it back to send backtick, Esc is available via §
            #
            set -s user-keys[221]  "\\033"
            # map backtick back from Escape
            bind -N "Send backtick"  -n User221  send "\\`"

            # Tthis keyb sends £ when it should send #
            set -s user-keys[222] "\\302\\243"
            bind -N "Send #" -n User222 send '#'
            """
        )

    def ic_virtual_escape_key(self, esc_key: str) -> None:
        self.tc.write(
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
        w = self.tc.write
        for i in range(1, 10):
            w(f'bind -N "M-{i} -> F{i}"  -n  M-{i}  send-keys  F{i}')
        w('bind -N "M-0 -> F10" -n  M-0  send-keys  F10')

    def ic_m_fn_keys(self) -> None:
        w = self.tc.write
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
        w = self.tc.write
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
        w = self.tc.write
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
            ("67", "<"),
            ("68", ">"),
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
