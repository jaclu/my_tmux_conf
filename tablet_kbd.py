#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
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
KBD_LOGITECH_COMBO_TOUCH = "Logitech Combo Touch"  # JacPad
KBD_BRYDGE_10_2_MAX = "Brydge 10.2 MAX+"
KBD_YOOZON3 = "Yoozon 3"  # same as brydge
KBD_OMNITYPE = "Omnitype Keyboard"
KBD_BLUETOOTH = "Bluetooth Keyboard"  # Pad5 - sadly generic name


class LimitedKbdSpecialHandling:
    """Groupings of user-keys

    < 200 Handled by base.py
    200     Escape
    201     alternate backtick
    202     alternate delete
    210-219 Specific Keyboard bindings
    300-336  Alt Upper case

    400-429 Function keys (only using up to 410)
    """

    # ensures that some settings ate not overridden via inheritance
    esc_has_been_handled = False
    euro_has_been_handled = False
    backtick_has_been_handled = False
    delete_has_been_handled = False

    # To ensure no collisions in user-keys indexes, always use the same source
    key_2_uk = {
        "Escape": 200,
        "backtick": 201,
        "Delete": 202,
        "#": 203,
        # Keyboard specific reserved range 210-299
        "M-A": 301,
        "M-B": 302,
        "M-C": 303,
        "M-D": 304,
        "M-E": 305,
        "M-F": 306,
        "M-G": 307,
        "M-H": 308,  # -  used in  auc_split_entire_window()
        "M-I": 309,  # -  used in  auc_split_entire_window()
        "M-J": 310,  # -  used in  auc_split_entire_window()
        "M-K": 311,  # -  used in  auc_split_entire_window()
        "M-L": 312,  # -  used in  auc_split_entire_window()
        "M-M": 313,
        "M-N": 314,
        "M-O": 315,
        "M-P": 316,
        "M-Q": 317,
        "M-R": 318,
        "M-S": 319,
        "M-T": 320,
        "M-U": 321,
        "M-V": 322,
        "M-W": 323,
        "M-X": 324,
        "M-Y": 325,
        "M-Z": 326,
        "M-_": 327,  # - used in  auc_meta_ses_handling
        "M-+": 328,  # - used in  auc_meta_ses_handling()
        "M-{": 329,
        "M-}": 330,
        "M-|": 331,
        "M-:": 332,
        'M-"': 333,
        "M-<": 334,
        "M->": 335,
        "M-?": 336,
        # 350-359 Meta Shift Numbers(when not used for function keys)
        "M-!": 350,
        "M-@": 351,
        "M-#": 352,
        "M-$": 353,
        "M-%": 354,
        "M-^": 355,
        "M-&": 356,
        "M-*": 357,
        "M-(": 358,
        "M-)": 359,
        # Function keys - listed without modifiers here, but could be
        # defined with modifiers
        "F1": 401,
        "F2": 402,
        "F3": 403,
        "F4": 404,
        "F5": 405,
        "F6": 406,
        "F7": 407,
        "F8": 408,
        "F9": 409,
        "F10": 410,
    }
    fn_key_2_uk = {
        #
        1: key_2_uk["F1"],
        2: key_2_uk["F2"],
        3: key_2_uk["F3"],
        4: key_2_uk["F4"],
        5: key_2_uk["F5"],
        6: key_2_uk["F6"],
        7: key_2_uk["F7"],
        8: key_2_uk["F8"],
        9: key_2_uk["F9"],
        10: key_2_uk["F10"],
    }

    def __init__(self, tmux_conf_instance):
        """Defines Userkey Function key mapping"""
        if not mtc_utils.LC_KEYBOARD:
            raise ImportWarning("No LC_KEYBOARD defined!")
        self.tc = tmux_conf_instance  # Primary tmux class, for backreferencing

        #     2: key_2_uk["F2"],
        #     3: key_2_uk["F3"],
        #     4: self.key_2_uk["F4"],
        #     5: self.key_2_uk["F5"],
        #     6: self.key_2_uk["F6"],
        #     7: self.key_2_uk["F7"],
        #     8: self.key_2_uk["F8"],
        #     9: self.key_2_uk["F9"],
        #     10: self.key_2_uk["F10"],
        # }

    def config_console_keyb(self) -> bool:
        #
        #  Only use this if the following conditions are met:
        #     1) tmux >= 2.6
        #     2) LC_KEYBOARD is set
        #
        if not self.tc.vers_ok(2.6):
            msg = """WARNING: tmux < 2.6 does not support user-keys, thus handling
            keyboard adaptions not supported on this version"""
            print(msg)
            self.tc.write(msg)
            return False

        print(f"This originated on a console - using keyboard: {mtc_utils.LC_KEYBOARD}")
        self.tc.write(
            f"""
            #======================================================
            #
            #  Remap keys for limited console
            #  Console type: {self.__class__.__name__}
            #  using keyboard: {mtc_utils.LC_KEYBOARD}
            #
            #======================================================
            """
        )
        if mtc_utils.LC_KEYBOARD in (KBD_OMNITYPE, KBD_BLUETOOTH):
            # already handles esc
            self.keyb_type_1()
        elif mtc_utils.LC_KEYBOARD in (
            KBD_BRYDGE_10_2_MAX,
            KBD_YOOZON3,
        ):
            self.keyb_type_2()
        elif mtc_utils.LC_KEYBOARD == KBD_LOGITECH_COMBO_TOUCH:
            self.keyb_type_combo_touch()
        # else:
        #     msg = f"# Unrecognized iSH LC_KEYBOARD: {mtc_utils.LC_KEYBOARD}"
        #     self.tc.write(msg)
        #     print(msg)
        #     return False
        return True

    # ======================================================
    #
    #  Specific Keyboards
    #
    # ======================================================

    def keyb_type_1(self):
        #
        #  This keyb type already generates Esc on the key above tab
        #
        self.alternate_key_euro("\\342\\202\\254")

    def keyb_type_2(self):
        #
        #  General settings seems to work for several keyboards
        #
        if not self.esc_has_been_handled:
            self.alternate_key_escape("\\302\\247")
        # self.alternate_key_euro("\\342\\202\\254")

    def keyb_type_combo_touch(self):
        #
        #  Logitech Combo Touch
        #
        self.keyb_type_2()  # Same esc handling
        self.alternate_backtick_key("\\033", "backtick")

    # ======================================================
    #
    #  alternate key handling
    #
    # ======================================================

    def alternate_key_escape(self, sequence: str) -> None:
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletKbd:alternate_key_escape({sequence}) "
                "must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.esc_has_been_handled:
            return
        self.tc.write(
            f"""#
            #  Replacement Escape key
            #
            {self.tc.opt_server} user-keys[{self.key_2_uk["Escape"]}]  "{sequence}"
            bind -N "Send Escape" -n User{self.key_2_uk["Escape"]}  send-keys Escape
            """
        )
        self.esc_has_been_handled = True

    def alternate_key_delete(self, sequence: str) -> None:
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletKbd:alternate_key_delete({sequence}) "
                "must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.delete_has_been_handled:
            return
        self.tc.write(
            f"""#
            #  Replacement Delete (DC) key
            #
            {self.tc.opt_server} user-keys[{self.key_2_uk["Delete"]}]  "{sequence}"
            bind -N "Send Delete (DC)" -n User{self.key_2_uk["Delete"]}  send-keys DC
            """
        )
        self.delete_has_been_handled = True

    def alternate_key_hash(self):
        self.tc.write(
            f"""
            # This keyb sends £ when it should send #
            {self.tc.opt_server} user-keys[{self.key_2_uk["#"]}] "\\302\\243"
            bind -N "Send #" -n User{self.key_2_uk["#"]} send-keys '#'
            """
        )

    def alternate_key_euro(self, sequence):
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletKbd:alternate_key_euro({sequence}) "
                "must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.euro_has_been_handled:
            return
        self.tc.alternate_key_euro(sequence)
        self.euro_has_been_handled = True

    def alternate_backtick_key(self, sequence: str, modifier="") -> None:
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletKbd:alternate_backtick_key({sequence}) "
                "must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.backtick_has_been_handled:
            return
        self.tc.write(
            f"""#
            #  Replacement Backtick key
            #
            {self.tc.opt_server} user-keys[{self.key_2_uk["backtick"]}]  "{sequence}"
            bind -N "{modifier} - Send backtick" -n \
                User{self.key_2_uk["backtick"]}  send-keys "\\`"
            """
        )
        self.backtick_has_been_handled = True


class TermuxConsole(LimitedKbdSpecialHandling):
    """Used to adopt the Termux console"""

    def keyb_type_1(self):
        self.alternate_key_escape("\\140")
        # self.alternate_backtick_key("\\033\\140", "M-")
        self.alternate_key_delete("\\033\\177")
        self.alternate_key_euro("\\033\\100")  # same as on Darwin
        super().keyb_type_1()


class IshConsole(LimitedKbdSpecialHandling):
    """Used to adopt the iSH console
    This redefines the rather limited keyboard in order to make it more useful.
    """

    def config_console_keyb(self):
        if not super().config_console_keyb():
            return False

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
        # bind -N "Enables M-<" -n User211 send-keys "M-<"

        ms_fn_keys_mapped = False

        fn_keys_handling = 2
        if fn_keys_handling == 1:
            self.fn_keys()
        elif fn_keys_handling == 2:
            self.m_fn_keys()
        elif fn_keys_handling == 3:
            ms_fn_keys_mapped = True
            self.ms_fn_keys()

        self.alt_upper_case(ms_fn_keys_mapped)

        # use <prefix> arrows as PageUp/Dn Home/End
        self.tc.use_prefix_arrow_nav_keys = True
        return True

    def fn_keys(self):
        #
        #  For keybs that already handles M-#
        #  this just binds them to send F#
        #
        w = self.tc.write
        for i in range(1, 10):
            w(f'bind -N "M-{i} -> F{i}"  -n  M-{i}  send-keys  F{i}')
        w('bind -N "M-0 -> F10" -n  M-0  send-keys  F10')

    def m_fn_keys(self) -> None:
        w = self.tc.write
        fn_uk = self.fn_key_2_uk

        w(
            f"""
        #
        #  This will map M-number to F1 - F10
        #
        {self.tc.opt_server} user-keys[{fn_uk[1]}] "\\033\\061"  #  M-1
        {self.tc.opt_server} user-keys[{fn_uk[2]}] "\\033\\062"  #  M-2
        {self.tc.opt_server} user-keys[{fn_uk[3]}] "\\033\\063"  #  M-3
        {self.tc.opt_server} user-keys[{fn_uk[4]}] "\\033\\064"  #  M-4
        {self.tc.opt_server} user-keys[{fn_uk[5]}] "\\033\\065"  #  M-5
        {self.tc.opt_server} user-keys[{fn_uk[6]}] "\\033\\066"  #  M-6
        {self.tc.opt_server} user-keys[{fn_uk[7]}] "\\033\\067"  #  M-7
        {self.tc.opt_server} user-keys[{fn_uk[8]}] "\\033\\070"  #  M-8
        {self.tc.opt_server} user-keys[{fn_uk[9]}] "\\033\\071"  #  M-9
        {self.tc.opt_server} user-keys[{fn_uk[10]}] "\\033\\060" #  M-0
        """
        )
        for i, key in fn_uk.items():
            w(f'bind -N "M-{i} -> F{i}"  -n  User{key}  send-keys F{i}')

    def ms_fn_keys(self) -> None:
        w = self.tc.write
        fn_uk = self.fn_key_2_uk
        w(
            f"""
        #
        #  This will map M-S-number to F1 - F10
        #
        {self.tc.opt_server} user-keys[{fn_uk[1]}] "\\342\\201\\204"  #  M-S-1
        {self.tc.opt_server} user-keys[{fn_uk[3]}] "\\342\\200\\271"  #  M-S-3
        {self.tc.opt_server} user-keys[{fn_uk[4]}] "\\342\\200\\272"  #  M-S-4
        {self.tc.opt_server} user-keys[{fn_uk[5]}] "\\357\\254\\201"  #  M-S-5
        {self.tc.opt_server} user-keys[{fn_uk[6]}] "\\357\\254\\202"  #  M-S-6
        {self.tc.opt_server} user-keys[{fn_uk[7]}] "\\342\\200\\241"  #  M-S-7
        {self.tc.opt_server} user-keys[{fn_uk[8]}] "\\302\\260"       #  M-S-8
        {self.tc.opt_server} user-keys[{fn_uk[9]}] "\\302\\267"       #  M-S-9
        {self.tc.opt_server} user-keys[{fn_uk[10]}] "\\342\\200\\232"  #  M-S-0"""
        )
        if self.euro_has_been_handled:
            w("# M-S-2 used for euro symbol")
        else:
            w(f'{self.tc.opt_server} user-keys[{fn_uk[2]}] "\\342\\202\\254"  #  M-S-2')

        for i, key in fn_uk.items():
            w(f'bind -N "M-S-{i} -> F{i}"  -n  User{key}  send-keys F{i}')

    # ======================================================
    #
    #  Map specific keys by name/function to specific user-key indexes
    #  for consistency
    #
    # ======================================================

    def alt_upper_case(self, ms_fn_keys_mapped: bool = False) -> None:
        """If fn keys are not mapped to ms numbers, use them as regular M- chars"""

        k2uk = self.key_2_uk
        w = self.tc.write

        self.tc.muc_keys = {
            mtc_utils.K_M_PLUS: f"User{k2uk['M-+']}",
            mtc_utils.K_M_PAR_OPEN: f"User{k2uk['M-(']}",
            mtc_utils.K_M_PAR_CLOSE: f"User{k2uk['M-)']}",
            mtc_utils.K_M_UNDERSCORE: f"User{k2uk['M-_']}",
            mtc_utils.K_M_P: f"User{k2uk['M-P']}",
            mtc_utils.K_M_X: f"User{k2uk['M-X']}",
        }

        auk = {}
        auk["M-A"] = "\\303\\205"
        auk["M-B"] = "\\304\\261"
        auk["M-C"] = "\\303\\207"
        auk["M-D"] = "\\303\\216"
        auk["M-E"] = "\\302\\264"
        auk["M-F"] = "\\303\\217"
        auk["M-G"] = "\\313\\235"
        auk["M-H"] = "\\303\\223"
        auk["M-I"] = "\\313\\206"
        auk["M-J"] = "\\303\\224"
        auk["M-K"] = "\\357\\243\\277"
        auk["M-L"] = "\\303\\222"
        auk["M-M"] = "\\303\\202"
        auk["M-N"] = "\\313\\234"
        auk["M-O"] = "\\303\\230"
        auk["M-P"] = "\\342\\210\\217"
        auk["M-Q"] = "\\305\\222"
        auk["M-R"] = "\\341\\200\\260"
        auk["M-S"] = "\\303\\215"
        auk["M-T"] = "\\313\\207"
        auk["M-U"] = "\\302\\250"
        auk["M-V"] = "\\342\\227\\212"
        auk["M-W"] = "\\342\\200\\236"
        auk["M-X"] = "\\313\\233"
        auk["M-Y"] = "\\303\\201"
        auk["M-Z"] = "\\302\\270"
        auk["M-_"] = "\\342\\200\\224"
        auk["M-{"] = "\\342\\200\\235"
        auk["M-}"] = "\\342\\200\\231"
        auk["M-|"] = "\\302\\273"
        auk["M-:"] = "\\303\\232"
        auk["M-<"] = "\\302\\257"
        auk["M->"] = "\\313\\230"
        auk["M-?"] = "\\302\\277"

        # On some keybs with a § there is a glitch in that
        # both S-§ and M-+ generate ±. Since M-+ is used, and S-§ not,
        # just ignore that S-§ also triggers this feature
        #  self.tc.opt_server  user-keys[61] "\\302\\261"       # M-+
        auk["M-+"] = "\\302\\261"

        # argh inside f-strings {/} needs to be contained in variables...
        # curly_open = "{"
        # curly_close = "}"
        w(  # not in root 308 310 311 312 316 324
            """
        #
        #  iSH console doesn't generate the right keys for alt-S characters
        #  Here they are interpreted by tmux
        #
        """
        )
        muc_values = set(self.tc.muc_keys.values())
        for key, sequence in auk.items():
            if f"User{k2uk[key]}" in muc_values:
                w(f"#  {key}  User{k2uk[key]} - used by: self.tc.muc_keys")
                continue

            w(f"set          -s user-keys[{k2uk[key]}] '{sequence}'")
            w(f"bind -N 'Send {key}' -n User{k2uk[key]}  send-keys '{key}'")

        # TO DO: reinsert this after M-:
        # {self.tc.opt_server} user-keys[{k2uk['M-"']}]  "\\303\\206"  # M-"

        if any("User" in value for value in self.tc.muc_keys.values()):
            print("---  self.tc.muc_keys  ---")
            for k, v in self.tc.muc_keys.items():
                print(f"  key: {k} value: {v}")
            print()

        muc_values = set(self.tc.muc_keys.values())
        # for key, sequence in k2uk.items():
        for key_name, user_key in k2uk.items():
            if f"User{user_key}" in muc_values:
                w(f"#  {key_name}  User{user_key} - used by: self.tc.muc_keys")
                continue

            if key_name == "M-N":
                #    Special case to avoid cutof at second -N
                #    on tmux < 3.1
                w(f"bind -N 'Enables M-N' -n  User{user_key}  send-keys {key_name}")
            w(f"bind -N 'Enables {key_name}' -n  User{user_key}  send-keys '{key_name}'")

        if not ms_fn_keys_mapped:
            # use meta shift numbers as normal m- chars
            w(
                f"""
            # Meta Shift numbers
            {self.tc.opt_server} user-keys[{k2uk["M-!"]}]  "\\342\\201\\204"  # M-!
            {self.tc.opt_server} user-keys[{k2uk["M-#"]}]  "\\342\\200\\271"  # M-#
            {self.tc.opt_server} user-keys[{k2uk["M-$"]}]  "\\342\\200\\272"  # M-$
            {self.tc.opt_server} user-keys[{k2uk["M-%"]}]  "\\357\\254\\201"  # M-%
            {self.tc.opt_server} user-keys[{k2uk["M-^"]}]  "\\357\\254\\202"  # M-^
            {self.tc.opt_server} user-keys[{k2uk["M-&"]}]  "\\342\\200\\241"  # M-&
            {self.tc.opt_server} user-keys[{k2uk["M-*"]}]  "\\302\\260"      # M-*
            {self.tc.opt_server} user-keys[{k2uk["M-("]}]  "\\302\\267"      # M-(
            {self.tc.opt_server} user-keys[{k2uk["M-)"]}]  "\\342\\200\\232"  # M-)
            """
            )

            # when euro is used this seems unneeded, check with it disabled...
            # if self.euro_has_been_handled:
            #     w("# M-@ used for euro symbol")
            # else:
            #     w(
            #         f"{self.tc.opt_server} user-keys[{k2uk['M-@']}]"
            #         '  "\\342\\202\\254"  # M-@'
            #     )

            for key_name, user_key in k2uk.items():
                if f"User{user_key}" in muc_values:
                    w(f"#  {key_name}  User{user_key} - used by: self.tc.muc_keys")
                    continue  # - used in  auc_meta_ses_handling()
                if key_name == "M-@" and self.euro_has_been_handled:
                    w(f"#  {key_name}  User{user_key} - used for: Euro")
                    continue  # was used for euro symbol
                w(f"bind -N 'Enables {key_name}' -n  User{user_key}  send '{key_name}'")
        w()

        #
        #  AAARRGH
        #  User-keys aren't parsed by tmux if they are bound to
        #  send-keys. If the resulting key has an action,
        #  we need to override and bind the user-key to this action.
        #  this is handled by the auc_ methods
        #


def special_consoles_config(tmux_conf_instance):
    if not mtc_utils.LC_CONSOLE:
        # If this is not a special console, take no action
        return False
    if not mtc_utils.LC_KEYBOARD:
        # If there is no indication what keyboard is used, no adaptions
        # can be applied, so might as well return
        # tmux_conf_instance.write("# ><> no LC_KEYBOARD detected")
        return False
    if mtc_utils.LC_CONSOLE == "iSH":  # and not mtc_utils.IS_REMOTE:
        kbd = IshConsole(tmux_conf_instance)
    elif mtc_utils.LC_CONSOLE == "Termux":
        kbd = TermuxConsole(tmux_conf_instance)
    else:
        sys.exit(f"ERROR: Unrecognized LC_CONSOLE:  [{mtc_utils.LC_CONSOLE}]")

    if kbd.config_console_keyb():
        return True
    return False
