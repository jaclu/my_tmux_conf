#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2024: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
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

from base import BaseConfig
from utils import run_shell

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

KBD_TYPE_BRYDGE_10_2_MAX = "Brydge 10.2 MAX+"
KBD_TYPE_BRYDGE_10_2_ESC = "Brydge 10.2 MAX+ esc"
KBD_TYPE_YOOZON3 = "Yoozon 3"  # same as brydge
KBD_TYPE_LOGITECH_COMBO = "Logitech Combo-Touch"
KBD_TYPE_OMNITYPE = "Omnitype Keyboard"
KBD_TYPE_BLUETOOTH = "Bluetooh Keyboard"  # sadly generic name

def this_is_aok_kernel():
    try:
        with open("/proc/ish/version", "r", encoding="utf-8") as file:
            for line in file:
                if "aok" in line.lower():
                    return True
    except FileNotFoundError:
        pass
    return False


class IshConsole(BaseConfig):
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

    def local_overides(self) -> None:
        super().local_overides()
        #
        #  Only use this if the following conditions are met:
        #     1) kernel is ish
        #     2) not an ssh session,
        #     3) key escapes not handled by an outer tmux
        #
        if (not os.path.exists("/proc/ish")) or os.environ.get("SSH_CONNECTION"):
            #
            #  This c is only relevant on the iSH console itself
            #  and if no outer tmux is already handling the nav keys
            #
            return
        if os.environ.get(NAV_KEY_HANDLED_TAG):
            print("iSH console keyboard already handled by outer tmux!")
            return

        self.is_ish_console = True
        print("This is an iSH console, keyboard adoptions will be implemented")

        if not self.vers_ok(2.6):
            print("WARNING: tmux < 2.6 does not support user-keys, thus handling")
            print("         keyboard adaptions not supported on this version")
            return

        host_name = run_shell('hostname -s').lower()
        print( f"hostname: {host_name}" )
        if host_name in ("jacpad", "jacpad-aok"):
            self.ic_keyboard = KBD_TYPE_LOGITECH_COMBO
        elif host_name  in ("pad5", "pad5-aok"):
            self.ic_keyboard = KBD_TYPE_BRYDGE_10_2_ESC
        else:
            self.ic_keyboard = None

        if self.ic_keyboard in (KBD_TYPE_BRYDGE_10_2_MAX, KBD_TYPE_YOOZON3):
            self.ic_keyb_type_1()
        elif self.ic_keyboard in (
            KBD_TYPE_BRYDGE_10_2_ESC,
            KBD_TYPE_OMNITYPE,
            KBD_TYPE_BLUETOOTH,
        ):
            self.ic_keyb_type_2()
        elif self.ic_keyboard == KBD_TYPE_LOGITECH_COMBO:
            self.ic_keyb_type_3()
        else:
            #
            #  keyboard handling Esc directly, no custom keys
            #
            self.ic_nav_key_prefix("\\033")
        self.general_keyb_settings()

        self.ic_setup()

    #
    #  Specific Keyboards
    #
    def ic_keyb_type_1(self):
        #
        #  General settings seems to work for several keyboards
        #
        w = self.write
        esc_key = "\\302\\247"
        self.ic_nav_key_prefix(esc_key)

        w(
            """
        #
        #  Send ~ by shifting the "Escape key"
        #  Send back-tick by shifting it the key the 2nd time, ie
        #  pressing what normally would be ~ in order not to collide
        #  with Escape
        #
        set -s user-keys[220]  "\\302\\261"
        bind -N "Enables ~" -n User220 send '~'
        bind -T escPrefix -N "Enables backtick" -n  User220  send "\\`"

        # set -s user-keys[221]  "\\302\\257"
        # bind -N "Enables M-<" -n User221 send "M-<"
        # set -s user-keys[221]  "~"# KBD_TYPE_BRYDGE_10_2_MAX - M-+
        """
        )

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
        bind -T escPrefix  User220  send "\\`"
        """
        )

    def ic_keyb_type_3(self):
        #
        #  Logitech Combo-Touch"
        #
        pm_key = "\\302\\261"  # S-±
        esc_key = "\\302\\247"  # §
        self.ic_nav_key_prefix(pm_key, esc_key=esc_key)
        self.write(
            """
        #
        #  On this keyb, in iSH back-tick sends Escape
        #  this changes it back, Esc is available via §
        #
        set -s user-keys[202]  "\\033"
        bind -n User202  send "\\`"
        """
        )

    def ic_nav_key_prefix(self, prefix_key, esc_key="") -> None:
        w = self.write
        print(f"Assuming keyboard is: {self.ic_keyboard}")

        if self.vers_ok(2.1):
            tbl_opt = "T"
        else:
            tbl_opt = "t"

        w(
            f"""#
        #  Handle Prefix key
        #
        set -s user-keys[200]  "{prefix_key}"
        bind -N "Switch to -T navPrefix" -n User200 switch-client -{tbl_opt} navPrefix
        """
        )
        if esc_key:
            w(
                f"""#
                #  Virtual Escape key
                #
                set -s user-keys[201]  "{esc_key}"
                bind -n User201  send Escape
                """
            )
        else:
            w("bind -T navPrefix  User200  send Escape")  # Double tap for actual Esc
        if this_is_aok_kernel():
            w(
                """#
            #  Use shift-arrows for navigation
            #
            bind -n  S-Up     send-keys PageUp
            bind -n  S-Down   send-keys PageDown
            bind -n  S-Left   send-keys Home
            bind -n  S-Right  send-keys End
            """
            )
        else:
            w(
                """#
            #  Use nav prefix for navigation
            #
            bind -T navPrefix  Down     send PageDown
            bind -T navPrefix  Up       send PageUp
            bind -T navPrefix  Left     send Home
            bind -T navPrefix  Right    send End
            """
            )
        self.ic_indicate_nav_key_handled()

    def general_keyb_settings(self):
        self.write(
            """
        #
        #  General Keyboard bindings
        #
        #  € is Option+Shift+2 in United States layout
        set -s user-keys[210]  "\\342\\202\\254" # Usually: €
        bind -N "Enables €" -n User210 send '€'

        # M-+ default: ±
        # set -s user-keys[211] "\\302\\261"

        #
        #  Some keybs have issues with M-<
        #  the initial binding for this char
        #  instead triggers it to send this sequence
        #  Weird, but this seems to solve it
        #
        #set -s user-keys[211]  "\\302\\257"
        #bind -N "Enables M-<" -n User211 send "M-<"
        """
        )

    def ic_setup(self) -> None:
        #
        #  Since iSH console is limited to only M-numbers and M-S-numbers
        #  I use M-S-number for function keys normally, thus not being
        #  able to use keys like M-(
        #  To avoid this collision, set fn_keys_mapped accordingly
        #
        #  This does general iSH mapping, not focusing on keyboard specific
        #  customization needs
        #
        self.ic_fn_keys()
        self.ic_alt_upper_case(fn_keys_mapped=True)

    def ic_indicate_nav_key_handled(self):
        self.write(
            f"""#
        #  Indicates this tmux is handling ISH_NAV_KEY, to ensure
        #  nested tmuxes, dont parse it again.
        #
        {NAV_KEY_HANDLED_TAG}=1"""
        )

    def ic_fn_keys(self) -> None:
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
        w('bind -N "M-0 -> F10" -n  User110  send-keys F10')

    def ic_alt_upper_case(self, fn_keys_mapped: bool) -> None:
        w = self.write
        m_par_open = ""  # Only used if not fn_keys_mapped
        m_par_close = ""  # Only used if not fn_keys_mapped

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
            # ("35", "<"), - used in self.swap_window_uk()
            # ("36", ">"), - used in self.swap_window_uk()
            ("37", "?"),
            # Doesn't work on Omnitype Keyboard, works on Yoozon3
            ("38", "_"),
            # Doesn't work on Omnitype,Yoozon3, generates ~
            # ("39", "+"),
        ):
            if c == "N":
                #  Special case to avoid cutof at second -N
                #  on tmux < 3.1
                w(f"bind -n  User{i}  send M-{c}")
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
            m_par_open = "User59"
            m_par_close = "User60"

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
        self.split_entire_window_uk(
            m_h="User8", m_j="User10", m_k="User11", m_l="User12"
        )
        self.display_plugins_used_uk(m_p="User16")
        self.kill_tmux_server_uk(m_x="User24")
        self.swap_window_uk(m_less_than="User35", m_greater_than="User36")
        self.meta_ses_handling_uk(
            m_plus=self.usr_key_meta_plus,
            m_par_open=m_par_open,
            m_par_close=m_par_close,
            m_underscore="User38",
        )

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

    #
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
#  If this is run directly
#
if __name__ == "__main__":
    IshConsole().run()
