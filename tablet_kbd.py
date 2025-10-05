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
KBD_TOUCH = "Touch Keyboard"


class LimitedKbdSpecialHandling:
    """Groupings of user-keys"""

    def __init__(self, tmux_conf_instance):
        """Defines Userkey Function key mapping"""
        if not mtc_utils.LC_KEYBOARD:
            raise ImportWarning("No LC_KEYBOARD defined!")
        self.tc = tmux_conf_instance  # Primary tmux class, for backreferencing

        # To ensure no collisions in user-keys indexes, always use the same source
        self.key_2_uk = {
            # < 200 Handled by base.py
            "Escape": 200,
            "~": 201,
            "backtick": 202,
            "Delete": 203,
            "#": 204,
            # Keyboard specific reserved range 210-299
            # Alt upper case chars
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
        self.fn_key_2_uk = {
            # Pick up the userkey indexes
            1: self.key_2_uk["F1"],
            2: self.key_2_uk["F2"],
            3: self.key_2_uk["F3"],
            4: self.key_2_uk["F4"],
            5: self.key_2_uk["F5"],
            6: self.key_2_uk["F6"],
            7: self.key_2_uk["F7"],
            8: self.key_2_uk["F8"],
            9: self.key_2_uk["F9"],
            10: self.key_2_uk["F10"],
        }

        # ensures that some settings ate not overridden via inheritance
        self.has_been_handled = {
            "Escape": False,
            "~": False,
            "backtick": False,
            "Euro": False,
            "delete": False,
        }
        self.sequence_used = []

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

        print()
        if mtc_utils.LC_ORIGIN:
            print(f"===>  Session for limited console from:  {mtc_utils.LC_ORIGIN}")
        print(f"===>  {self.__class__.__name__}  -  kbd: {mtc_utils.LC_KEYBOARD}")
        print()
        self.tc.write(
            f"""
            #======================================================
            #
            #  Remap keys for limited console at: {mtc_utils.LC_ORIGIN}
            #
            #  {self.__class__.__name__}  -  kbd: {mtc_utils.LC_KEYBOARD}
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
        elif mtc_utils.LC_KEYBOARD == KBD_TOUCH:
            self.keyb_type_touch()
        else:
            msg = f"# Unrecognized iSH LC_KEYBOARD: {mtc_utils.LC_KEYBOARD}"
            self.tc.write(msg)
            print(msg)
            return False
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

    def keyb_type_2(self):  # , define_backtick=True):
        #
        #  General settings seems to work for several keyboards
        #
        # JacPad iSH KBD_BRYDGE_10_2_MAX
        # <Esc> 302 247   §
        # ~     302 261 (Shift Esc) +/- char
        # `     033 060 (C-M Esc)
        self.alternate_key_escape("\\302\\247")
        self.alternate_key_tilde("\\302\\261")
        # if define_backtick:
        #     self.alternate_key_backtick("\\033\\060")
        # self.alternate_key_euro("\\342\\202\\254")

    def keyb_type_combo_touch(self):
        #
        #  Logitech Combo Touch
        #
        self.alternate_key_escape("\\302\\247")
        self.alternate_key_backtick("\\033")  # sends Esc by default

    def keyb_type_touch(self):
        #
        #  Built in touch-keyb
        #
        self.tc.write("# No adaptations available for the touch keyboard")
        self.tc.write()  # spacer line
        # self.tc.use_prefix_arrow_nav_keys = True

    # ======================================================
    #
    #  alternate key handling
    #
    # ======================================================

    def alt_key_param_check(self, sequence, key):
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletKbd:alt_key_param_check({sequence}, {key}) "
                "must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.has_been_handled[key]:
            sys.exit(f"Alternate {key} key has already been defined")

    def alt_key_define(self, sequence, key):
        self.alt_key_param_check(sequence, key)
        if key == "backtick":
            send_str = "\\`"
        elif key == "delete":
            send_str = "DC"
        else:
            send_str = key

        self.tc.write(
            f"""#
            #  Replacement {key} key
            #
            {self.tc.opt_server} user-keys[{self.key_2_uk[key]}]  "{sequence}"
            bind -N "Send key" -n User{self.key_2_uk[key]}  send-keys {send_str}
            """
        )
        self.sequence_used.append(sequence)
        self.has_been_handled[key] = True

    def alternate_key_escape(self, sequence: str) -> None:
        self.alt_key_define(sequence, "Escape")

    def alternate_key_tilde(self, sequence: str) -> None:  # modifier=""
        self.alt_key_define(sequence, "~")

    def alternate_key_backtick(self, sequence: str) -> None:  # modifier=""
        self.alt_key_define(sequence, "backtick")

    def alternate_key_delete(self, sequence: str) -> None:
        self.alt_key_define(sequence, "delete")

    def hash_not_pound(self):
        sequence = "\\302\\243"
        self.tc.write(
            f"""
            # This keyb sends £ when it should send #
            {self.tc.opt_server} user-keys[{self.key_2_uk["#"]}] "{sequence}"
            bind -N "Send #" -n User{self.key_2_uk["#"]} send-keys  #
            """
        )
        self.sequence_used.append(sequence)

    def alternate_key_euro(self, sequence):
        key = "Euro"
        self.alt_key_param_check(sequence, key)
        self.tc.alternate_key_euro(sequence)
        self.sequence_used.append(sequence)
        self.has_been_handled[key] = True


class TermuxConsole(LimitedKbdSpecialHandling):
    """Used to adopt the Termux console"""

    def keyb_type_1(self):
        self.alternate_key_escape("\\140")
        # Recently all three below fail, so for now disabled
        # self.alternate_key_backtick("\\033\\140")
        # self.alternate_key_delete("\\033\\177")
        # self.alternate_key_euro("\\033\\100")  # same as on Darwin

        super().keyb_type_1()


class IshConsole(LimitedKbdSpecialHandling):
    """Used to adopt the iSH console
    This redefines the rather limited keyboard in order to make it more useful.
    """

    def __init__(self, tmux_conf_instance):
        super().__init__(tmux_conf_instance)
        self.auk = {
            # iSH Console can not generate Alt Upper Case characters, so they are mapped
            "M-A": "\\303\\205",
            "M-B": "\\304\\261",
            "M-C": "\\303\\207",
            "M-D": "\\303\\216",
            "M-E": "\\302\\264",
            "M-F": "\\303\\217",
            "M-G": "\\313\\235",
            "M-H": "\\303\\223",
            "M-I": "\\313\\206",
            "M-J": "\\303\\224",
            "M-K": "\\357\\243\\277",
            "M-L": "\\303\\222",
            "M-M": "\\303\\202",
            "M-N": "\\313\\234",
            "M-O": "\\303\\230",
            "M-P": "\\342\\210\\217",
            "M-Q": "\\305\\222",
            "M-R": "\\341\\200\\260",
            "M-S": "\\303\\215",
            "M-T": "\\313\\207",
            "M-U": "\\302\\250",
            "M-V": "\\342\\227\\212",
            "M-W": "\\342\\200\\236",
            "M-X": "\\313\\233",
            "M-Y": "\\303\\201",
            "M-Z": "\\302\\270",
            "M-_": "\\342\\200\\224",
            # On some keybs with a § there is a glitch in that
            # both S-§ and M-+ generate ±. Since M-+ is used, and S-§ not,
            # just ignore that S-§ ...
            "M-+": "\\302\\261",
            "M-{": "\\342\\200\\235",
            "M-}": "\\342\\200\\231",
            "M-|": "\\302\\273",
            "M-:": "\\303\\232",
            'M-"': "\\303\\206",
            "M-<": "\\302\\257",
            "M->": "\\313\\230",
            "M-?": "\\302\\277",
            "M-(": "\\302\\267",
            "M-)": "\\200\\232",
        }

    def config_console_keyb(self):
        if not super().config_console_keyb():
            return False

        if mtc_utils.LC_KEYBOARD == KBD_TOUCH:
            # No kbd remapping supported for touch kbd
            return True

        self.tc.write(
            """
        #
        #  Map Function keys
        # """
        )
        ms_fn_keys_mapped = False
        fn_keys_handling = 2
        if fn_keys_handling == 1:
            self.fn_keys()
        elif fn_keys_handling == 2:
            self.m_fn_keys()
        elif fn_keys_handling == 3:
            ms_fn_keys_mapped = True
            self.ms_fn_keys()

        self.define_muc_keys()
        self.alt_upper_case(ms_fn_keys_mapped)

        # use <prefix> arrows as PageUp/Dn Home/End
        self.tc.use_prefix_arrow_nav_keys = True
        return True

    def fn_keys(self):
        #
        #  For keybs that already handles M-#
        #  this just binds them to send F# and swaps M-0 -> F10
        #
        for i in range(1, 10):
            self.tc.write(f'bind -N "M-{i} -> F{i}"  -n  M-{i}  send-keys  F{i}')
        self.tc.write('bind -N "M-0 -> F10" -n  M-0  send-keys  F10')

    # ======================================================
    #
    #  Map specific keys by name/function to specific user-key indexes
    #  for consistency
    #
    # ======================================================

    def m_fn_keys(self) -> None:
        w = self.tc.write
        k2uk = self.key_2_uk

        fn_keys = (
            ("F1", "M-1", "\\033\\061"),
            ("F2", "M-2", "\\033\\062"),
            ("F3", "M-3", "\\033\\063"),
            ("F4", "M-4", "\\033\\064"),
            ("F5", "M-5", "\\033\\065"),
            ("F6", "M-6", "\\033\\066"),
            ("F7", "M-7", "\\033\\067"),
            ("F8", "M-8", "\\033\\070"),
            ("F9", "M-9", "\\033\\071"),
            ("F10", "M-0", "\\033\\060"),
        )
        for fn, key, sequence in fn_keys:
            w(f'{self.tc.opt_server}   user-keys[{k2uk[fn]}]  "{sequence}"  #     {key}')
            w(f"bind -N 'Send {key}' -n User{k2uk[fn]}    send-keys  {fn}")
        w()  # spacer line

    def ms_fn_keys(self) -> None:
        w = self.tc.write
        k2uk = self.key_2_uk

        fn_keys = (
            ("F1", "M-S-1", "\\342\\201\\204"),
            ("F2", "M-S-2", "\\342\\200\\271"),
            ("F3", "M-S-3", "\\342\\200\\272"),
            ("F4", "M-S-4", "\\357\\254\\201"),
            ("F5", "M-S-5", "\\357\\254\\202"),
            ("F6", "M-S-6", "\\342\\200\\241"),
            ("F7", "M-S-7", "\\342\\200\\241"),
            ("F8", "M-S-8", "\\302\\260"),
            ("F9", "M-S-9", "\\302\\267"),
            ("F10", "M-S-0", "\\342\\200\\232"),
        )
        for fn, key, sequence in fn_keys:
            if key == "M-S-2" and self.has_been_handled["euro"]:
                w("# M-S-2 used for euro symbol")
                continue
            w(f'{self.tc.opt_server}   user-keys[{k2uk[fn]}]  "{sequence}"  #     {key}')
            w(f"bind -N 'Send {key}' -n User{k2uk[fn]}    send-keys  {fn}")
        w()  # spacer line

    def define_muc_keys(self):
        self.tc.muc_keys = {
            mtc_utils.K_M_PLUS: f"User{self.key_2_uk['M-+']}",
            # mtc_utils.K_M_PAR_OPEN: f"User{self.key_2_uk['M-(']}",
            # mtc_utils.K_M_PAR_CLOSE: f"User{self.key_2_uk['M-)']}",
            mtc_utils.K_M_UNDERSCORE: f"User{self.key_2_uk['M-_']}",
            mtc_utils.K_M_P: f"User{self.key_2_uk['M-P']}",
            mtc_utils.K_M_X: f"User{self.key_2_uk['M-X']}",
        }

    def alt_upper_case_numbers(self):
        # use meta shift numbers as normal m- chars
        # Meta Shift numbers
        self.auk["M-!"] = "\\342\\201\\204"
        self.auk["M-#"] = "\\342\\200\\271"
        self.auk["M-$"] = "\\342\\200\\272"
        self.auk["M-%"] = "\\357\\254\\201"
        self.auk["M-^"] = "\\357\\254\\202"
        self.auk["M-&"] = "\\342\\200\\241"
        self.auk["M-*"] = "\\302\\260"
        # self.auk["M-("] = "\\302\\267"
        # self.auk["M-)"] = "\\342\\200\\232"

    def alt_upper_case(self, ms_fn_keys_mapped: bool = False) -> None:
        """If fn keys are not mapped to ms numbers, use them as regular M- chars"""

        k2uk = self.key_2_uk
        w = self.tc.write

        if not ms_fn_keys_mapped:
            self.alt_upper_case_numbers()

        w(  # not in root 308 310 311 312 316 324
            """
        #
        #  iSH console doesn't generate the right keys for alt-S characters
        #  Here they are interpreted by tmux
        #
        """
        )
        muc_values = set(self.tc.muc_keys.values())
        for key, sequence in self.auk.items():
            if sequence in self.sequence_used:
                # w(f'# --- already defined:    {k2uk[key]}   "{sequence}"      {key}')
                # w(f'# ---  sequence in use:   {k2uk[key]}   "{sequence}"      {key}')
                w(f"#                     User{k2uk[key]}                   {key}  alt key")
                continue
            w(f'{self.tc.opt_server}   user-keys[{k2uk[key]}]  "{sequence}"')
            if f"User{k2uk[key]}" in muc_values:
                # Display muc keys
                w(f"#                     User{k2uk[key]}                   {key}  muc_key")
            elif key == "M-N" and not self.tc.vers_ok(3.1):
                #    Special case to avoid cutof at second -N
                w("# tmux < 3.1 Fails to handle Meta N - so it is skipped")
            elif key == 'M-"':
                w(f"""bind -N 'Send {key}' -n User{k2uk[key]}     send-keys     '{key}' """)
            elif key in ("M-{", "M-}", "M-$"):
                w(f"""bind -N "Send {key}" -n User{k2uk[key]}     send-keys     "{key}" """)
            else:
                w(f'bind -N "Send {key}" -n User{k2uk[key]}     send-keys     {key}')
        w()  # spacer line

        # if any("User" in value for value in self.tc.muc_keys.values()):
        #     print("---  self.tc.muc_keys  ---")
        #     for k, u in self.tc.muc_keys.items():
        #         print(f" userkey: {u}   key: {k}")
        #     print()


def special_consoles_config(tmux_conf_instance):
    if not mtc_utils.LC_CONSOLE:
        # If this is not a special console, take no action
        return False

    if not mtc_utils.LC_KEYBOARD:
        # If there is no indication what keyboard is used, no specific adaptions
        # can be applied.
        # Here the assumption is usage of the touch-keyb
        mtc_utils.LC_KEYBOARD = KBD_TOUCH
        # <p> c-m = M
    if mtc_utils.LC_CONSOLE == "iSH":  # and not mtc_utils.IS_REMOTE:
        kbd = IshConsole(tmux_conf_instance)
    elif mtc_utils.LC_CONSOLE == "Termux":
        kbd = TermuxConsole(tmux_conf_instance)
    else:
        sys.exit(f"ERROR: Unrecognized LC_CONSOLE:  [{mtc_utils.LC_CONSOLE}]")

    if kbd.config_console_keyb():
        return True
    return False
