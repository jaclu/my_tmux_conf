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
KBD_LOGITECH_COMBO_TOUCH = "Logitech Combo Touch"
KBD_BRYDGE_10_2_MAX = "Brydge 10.2 MAX+"
KBD_YOOZON3 = "Yoozon 3"  # same as brydge
KBD_OMNITYPE = "Omnitype Keyboard"
KBD_BLUETOOTH = "Bluetooth Keyboard"  # sadly generic name


class BtKbdSpecialHandling:
    """Groupings of user-keys

    < 200 Handled by base.py
    200     Escape
    201     alternate backtick
    202     alternate delete
    210-219 Specific Keyboard bindings
    300-336  Alt Upper case
    350-359 Meta Shift Numbers(when not used for function keys)
    400-429 Function keys (only using up to 410)
    """

    # ensures that some settings ate not overridden via inheritance
    esc_has_been_handled = False
    euro_has_been_handled = False
    backtick_has_been_handled = False
    delete_has_been_handled = False

    def __init__(self, tmux_conf_instance):
        if not mtc_utils.LC_KEYBOARD:
            raise ImportWarning("No LC_KEYBOARD defined!")
        self.tc = tmux_conf_instance

    #
    #  Specific Keyboards
    #
    def keyb_type_1(self):
        #
        #  This keyb type already generates Esc on the key above tab
        #
        pass

    def keyb_type_2(self):
        #
        #  General settings seems to work for several keyboards
        #
        if not self.esc_has_been_handled:
            self.alternate_escape_key("\\302\\247")

    def keyb_type_combo_touch(self):
        #
        #  Logitech Combo Touch
        #
        #
        self.keyb_type_2()  # Same esc handling
        self.alternate_backtick_key("\\033", "backtick")
        self.tc.write(
            f"""#
            #  On this keyb, backtick (next to z) sends Escape
            #  this changes it back to send backtick, Esc is available via §
            #

            # This keyb sends £ when it should send #
            {self.tc.opt_server} user-keys[210] "\\302\\243"
            bind -N "Send #" -n User210 send '#'
            """
        )

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

    def euro_fix(self, sequence):
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletBtKbd:euro_fix({sequence}) must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.euro_has_been_handled:
            return
        self.tc.euro_fix(sequence)
        self.euro_has_been_handled = True

    def alternate_escape_key(self, sequence: str) -> None:
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletBtKbd:alternate_escape_key({sequence}) "
                "must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.esc_has_been_handled:
            return
        self.tc.write(
            f"""#
            #  Replacement Escape key
            #
            {self.tc.opt_server} user-keys[200]  "{sequence}"
            bind -N "Send Escape" -n User200  send Escape
            """
        )
        self.esc_has_been_handled = True

    def alternate_backtick_key(self, sequence: str, modifier="") -> None:
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletBtKbd:alternate_backtick_key({sequence}) "
                "must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.backtick_has_been_handled:
            return
        self.tc.write(
            f"""#
            #  Replacement Backtick key
            #
            {self.tc.opt_server} user-keys[201]  "{sequence}"
            bind -N "{modifier} - Send backtick" -n User201  send "\\`"
            """
        )
        self.backtick_has_been_handled = True

    def alternate_delete(self, sequence: str) -> None:
        if sequence[:1] != "\\":
            err_msg = (
                f"ERROR: TabletBtKbd:alternate_delete({sequence}) "
                "must be given in octal notation"
            )
            sys.exit(err_msg)
        if self.delete_has_been_handled:
            return
        self.tc.write(
            f"""#
            #  Replacement Delete (DC) key
            #
            {self.tc.opt_server} user-keys[202]  "{sequence}"
            bind -N "Send Delete (DC)" -n User202  send DC
            """
        )
        self.delete_has_been_handled = True


class TermuxConsole(BtKbdSpecialHandling):
    """Used to adopt the Termux console"""

    def keyb_type_1(self):
        self.alternate_escape_key("\\140")
        self.alternate_backtick_key("\\033\\140", "M-")
        self.alternate_delete("\\033\\177")
        self.euro_fix("\\033\\100")  # same as on Darwin
        super().keyb_type_1()


class IshConsole(BtKbdSpecialHandling):
    """Used to adopt the iSH console
    This redefines the rather limited keyboard in order to make it more useful.
    """

    def keyb_type_combo_touch(self):
        self.euro_fix("\\342\\202\\254")
        super().keyb_type_combo_touch()

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
        # bind -N "Enables M-<" -n User211 send "M-<"

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
        uk_func = self.define_fn_user_keys()
        w = self.tc.write
        w(
            f"""
        #
        #  This will map M-number to F1 - F10
        #
        {self.tc.opt_server} user-keys[{uk_func[1]}] "\\033\\061"  #  M-1
        {self.tc.opt_server} user-keys[{uk_func[2]}] "\\033\\062"  #  M-2
        {self.tc.opt_server} user-keys[{uk_func[3]}] "\\033\\063"  #  M-3
        {self.tc.opt_server} user-keys[{uk_func[4]}] "\\033\\064"  #  M-4
        {self.tc.opt_server} user-keys[{uk_func[5]}] "\\033\\065"  #  M-5
        {self.tc.opt_server} user-keys[{uk_func[6]}] "\\033\\066"  #  M-6
        {self.tc.opt_server} user-keys[{uk_func[7]}] "\\033\\067"  #  M-7
        {self.tc.opt_server} user-keys[{uk_func[8]}] "\\033\\070"  #  M-8
        {self.tc.opt_server} user-keys[{uk_func[9]}] "\\033\\071"  #  M-9
        {self.tc.opt_server} user-keys[{uk_func[0]}] "\\033\\060" #  M-0
        """
        )
        for i, key in uk_func.items():
            if i == 0:
                w(f'bind -N "M-{i} -> F10"  -n  User{key}  send-keys F10')
            else:
                w(f'bind -N "M-{i} -> F{i}"  -n  User{key}  send-keys F{i}')

    def ms_fn_keys(self) -> None:
        uk_func = self.define_fn_user_keys()
        w = self.tc.write
        w(
            f"""
        #
        #  This will map M-S-number to F1 - F10
        #
        {self.tc.opt_server} user-keys[{uk_func[1]}] "\\342\\201\\204"  #  M-S-1
        {self.tc.opt_server} user-keys[{uk_func[2]}] "\\342\\202\\254"  #  M-S-2
        {self.tc.opt_server} user-keys[{uk_func[3]}] "\\342\\200\\271"  #  M-S-3
        {self.tc.opt_server} user-keys[{uk_func[4]}] "\\342\\200\\272"  #  M-S-4
        {self.tc.opt_server} user-keys[{uk_func[5]}] "\\357\\254\\201"  #  M-S-5
        {self.tc.opt_server} user-keys[{uk_func[6]}] "\\357\\254\\202"  #  M-S-6
        {self.tc.opt_server} user-keys[{uk_func[7]}] "\\342\\200\\241"  #  M-S-7
        {self.tc.opt_server} user-keys[{uk_func[8]}] "\\302\\260"       #  M-S-8
        {self.tc.opt_server} user-keys[{uk_func[9]}] "\\302\\267"       #  M-S-9
        {self.tc.opt_server} user-keys[{uk_func[0]}] "\\342\\200\\232"  #  M-S-0
        """
        )
        for i, key in uk_func.items():
            if i == 0:
                w(f'bind -N "M-S-{i} -> F10"  -n  User{key}  send-keys F10')
            else:
                w(f'bind -N "M-S-{i} -> F{i}"  -n  User{key}  send-keys F{i}')

    def define_fn_user_keys(self):
        """Defines Userkey Function key mapping"""
        return {
            1: 401,
            2: 402,
            3: 403,
            4: 404,
            5: 405,
            6: 406,
            7: 407,
            8: 408,
            9: 409,
            0: 410,
        }

    def alt_upper_case(self, ms_fn_keys_mapped: bool = False) -> None:
        """If fn keys are not mapped to ms numbers, use them as regular M- chars"""
        uk_ms_char = {
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
        }

        #  Collides with meta-shift F1 - F10 remapping
        uk_ms_numb = {
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
        }

        self.tc.muc_keys = {
            "muc_plus": f"User{uk_ms_char['M-+']}",
            "muc_par_open": f"User{uk_ms_numb['M-(']}",
            "muc_par_close": f"User{uk_ms_numb['M-)']}",
            "muc_underscore": f"User{uk_ms_char['M-_']}",
            "muc_P": f"User{uk_ms_char['M-P']}",
            "muc_X": f"User{uk_ms_char['M-X']}",
            "muc_H": f"User{uk_ms_char['M-H']}",
            "muc_J": f"User{uk_ms_char['M-J']}",
            "muc_K": f"User{uk_ms_char['M-K']}",
            "muc_L": f"User{uk_ms_char['M-L']}",
        }

        w = self.tc.write
        # argh inside f-strings {/} needs to be contained in variables...
        # curly_open = "{"
        # curly_close = "}"
        w(
            f"""
        #
        #  iSH console doesn't generate the right keys for
        #  Alt upper case chars, so here they are defined
        #
        {self.tc.opt_server} user-keys[{uk_ms_char["M-A"]}]  "\\303\\205"  # M-A
        {self.tc.opt_server} user-keys[{uk_ms_char["M-B"]}]  "\\304\\261"  # M-B
        {self.tc.opt_server} user-keys[{uk_ms_char["M-C"]}]  "\\303\\207"  # M-C
        {self.tc.opt_server} user-keys[{uk_ms_char["M-D"]}]  "\\303\\216"  # M-D
        {self.tc.opt_server} user-keys[{uk_ms_char["M-E"]}]  "\\302\\264"  # M-E
        {self.tc.opt_server} user-keys[{uk_ms_char["M-F"]}]  "\\303\\217"  # M-F
        {self.tc.opt_server} user-keys[{uk_ms_char["M-G"]}]  "\\313\\235"  # M-G
        {self.tc.opt_server} user-keys[{uk_ms_char["M-H"]}]  "\\303\\223"  # M-H
        {self.tc.opt_server} user-keys[{uk_ms_char["M-I"]}]  "\\313\\206"  # M-I
        {self.tc.opt_server} user-keys[{uk_ms_char["M-J"]}]  "\\303\\224"  # M-J
        {self.tc.opt_server} user-keys[{uk_ms_char["M-K"]}]  "\\357\\243\\277"  # M-K
        {self.tc.opt_server} user-keys[{uk_ms_char["M-L"]}]  "\\303\\222"  # M-L
        {self.tc.opt_server} user-keys[{uk_ms_char["M-M"]}]  "\\303\\202"  # M-M
        {self.tc.opt_server} user-keys[{uk_ms_char["M-N"]}]  "\\313\\234"  # M-N
        {self.tc.opt_server} user-keys[{uk_ms_char["M-O"]}]  "\\303\\230"  # M-O
        {self.tc.opt_server} user-keys[{uk_ms_char["M-P"]}]  "\\342\\210\\217"  # M-P
        {self.tc.opt_server} user-keys[{uk_ms_char["M-Q"]}]  "\\305\\222"  # M-Q
        {self.tc.opt_server} user-keys[{uk_ms_char["M-R"]}]  "\\341\\200\\260"  # M-R
        {self.tc.opt_server} user-keys[{uk_ms_char["M-S"]}]  "\\303\\215"  # M-S
        {self.tc.opt_server} user-keys[{uk_ms_char["M-T"]}]  "\\313\\207"  # M-T
        {self.tc.opt_server} user-keys[{uk_ms_char["M-U"]}]  "\\302\\250"  # M-U
        {self.tc.opt_server} user-keys[{uk_ms_char["M-V"]}]  "\\342\\227\\212"  # M-V
        {self.tc.opt_server} user-keys[{uk_ms_char["M-W"]}]  "\\342\\200\\236"  # M-W
        {self.tc.opt_server} user-keys[{uk_ms_char["M-X"]}]  "\\313\\233"  # M-X
        {self.tc.opt_server} user-keys[{uk_ms_char["M-Y"]}]  "\\303\\201"  # M-Y
        {self.tc.opt_server} user-keys[{uk_ms_char["M-Z"]}]  "\\302\\270"  # M-Z
        {self.tc.opt_server} user-keys[{uk_ms_char["M-_"]}]  "\\342\\200\\224"  # M-_


        # On some keybs with a § there is a glitch in that
        # both S-§ and M-+ generate ±. Since M-+ is used, and S-§ not,
        # just ignore that S-§ also triggers this feature
        #  self.tc.opt_server  user-keys[61] "\\302\\261"       # M-+
        {self.tc.opt_server} user-keys[{uk_ms_char["M-+"]}]  "\\302\\261"  # M-+

        {self.tc.opt_server} user-keys[{uk_ms_char["M-{"]}]  "\\342\\200\\235"  # M-{{
        {self.tc.opt_server} user-keys[{uk_ms_char["M-}"]}]  "\\342\\200\\231"  # M-}}

        {self.tc.opt_server} user-keys[{uk_ms_char["M-|"]}]  "\\302\\273"  # M-|
        {self.tc.opt_server} user-keys[{uk_ms_char["M-:"]}]  "\\303\\232"  # M-:
        {self.tc.opt_server} user-keys[{uk_ms_char['M-"']}]  "\\303\\206"  # M-"
        {self.tc.opt_server} user-keys[{uk_ms_char["M-<"]}]  "\\302\\257"  # M-<
        {self.tc.opt_server} user-keys[{uk_ms_char["M->"]}]  "\\313\\230"  # M->
        {self.tc.opt_server} user-keys[{uk_ms_char["M-?"]}]  "\\302\\277"  # M-?
        """
        )

        for sequence, key in uk_ms_char.items():
            if sequence in (
                "M-H",  # used in  auc_split_entire_window()
                "M-J",  # used in  auc_split_entire_window()
                "M-K",  # used in  auc_split_entire_window()
                "M-L",  # used in  auc_split_entire_window()
                "M-P",  # used in  auc_display_plugins_used()
                "M-X",  # used in  auc_kill_tmux_server()
                "M-_",  # used in  auc_meta_ses_handling()
                "M-+",  # used in  auc_meta_ses_handling()
            ):
                continue
            if sequence == "M-N":
                #    Special case to avoid cutof at second -N
                #    on tmux < 3.1
                w(f"bind -N 'Enables M-N' -n  User{key}  send {sequence}")
            elif sequence == 'M-"':
                w(f"bind -N 'Enables {sequence}' -n  User{key}  send '{sequence}'")
            else:
                w(f'bind -N "Enables {sequence}" -n  User{key}  send "{sequence}"')

        if not ms_fn_keys_mapped:
            # use meta shift numbers as normal m- chars
            w(
                f"""
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-!"]}]  "\\342\\201\\204"  # M-!
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-@"]}]  "\\342\\202\\254"  # M-@
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-#"]}]  "\\342\\200\\271"  # M-#
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-$"]}]  "\\342\\200\\272"  # M-$
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-%"]}]  "\\357\\254\\201"  # M-%
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-^"]}]  "\\357\\254\\202"  # M-^
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-&"]}]  "\\342\\200\\241"  # M-&
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-*"]}]  "\\302\\260"      # M-*
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-("]}]  "\\302\\267"      # M-(
            {self.tc.opt_server} user-keys[{uk_ms_numb["M-)"]}]  "\\342\\200\\232"  # M-)
            """
            )
            for sequence, key in uk_ms_numb.items():
                if sequence in ("M-(", "M-)"):
                    continue  # - used in  auc_meta_ses_handling()
                w(f'bind -N "Enables {sequence}" -n  User{key}  send "{sequence}"')

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
        # If there is no indication what keyboard is used, no adaptions
        # can be applied, so might as well return
        # tmux_conf_instance.write("# ><> no LC_CONSOLE detected")
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
