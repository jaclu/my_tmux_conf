#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
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
import os

from base import BaseConfig


class IshConsole(BaseConfig):
    """When running tmux from an iSH console this redefines the rather
    limited keyboard in order to make it more useful.

    If ISH_NAV_KEY is defined and not "None" use it
    """

    def local_overides(self) -> None:
        super().local_overides()
        #
        #  Only use this if client is iSH using a nav-key
        #
        self.ish_nav_key = os.environ.get("ISH_NAV_KEY") or ""

        if self.ish_nav_key in ("None", ""):
            #
            # This is not running on the iSH console, so no special
            # handling is needed
            #
            return

        print(f">> nav_key: [{self.ish_nav_key}]")
        self.ic_setup()

    def ic_setup(self) -> None:
        if self.ish_nav_key == "shift":
            self.ic_nav_key_mod("S")
        elif self.ish_nav_key == "ctrl":
            self.ic_nav_key_mod("C")
        else:
            self.ic_nav_key_esc_prefix()

        #
        #  Since iSH console is limited to only M-numbers and M-S-numbers
        #  I use M-S-number for function keys normally, thus not being
        #  able to use keys like M-(
        #  To avoid this collision, set fn_keys_mapped accordingly
        #
        self.ic_fn_keys()
        self.ic_alt_upper_case(fn_keys_mapped=True)

    def ic_nav_key_mod(self, mod_char: str) -> None:
        self.write(
            f"""
        bind -N "S-Up = PageUp"     -n  {mod_char}-Up     send-keys PageUp
        bind -N "S-Down = PageDown" -n  {mod_char}-down   send-keys PageDown
        bind -N "S-Left = Home"     -n  {mod_char}-Left   send-keys Home
        bind -N "S-Right = End"     -n  {mod_char}-Right  send-keys End
        """
        )

    def ic_nav_key_esc_prefix(self) -> None:
        self.write(
            f"""
        #  Use Esc as prefix for nav-keys
        set -s user-keys[200]  "{self.ish_nav_key}"  # multiKeyBT

        bind -n User200 switch-client -T multiKeyBT

        bind -T multiKeyBT  Down     send PageDown
        bind -T multiKeyBT  Up       send PageUp
        bind -T multiKeyBT  Left     send Home
        bind -T multiKeyBT  Right    send End
        bind -T multiKeyBT  User200  send Escape
        """
        )

    def ic_fn_keys(self) -> None:
        w = self.write
        #
        #  This will map M-S number to F1 - F10
        #
        w(
            """
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
        set -s user-keys[32]  "\\303\\232"  # M-:
        set -s user-keys[33]  "\\303\\206"  # M-\"
        set -s user-keys[34]  "\\302\\273"  # M-\\
        set -s user-keys[35]  "\\302\\257"  # M-<
        set -s user-keys[36]  "\\313\\230"  # M->
        set -s user-keys[37]  "\\302\\277"  # M-?

        # Doesn't work on Omnitype
        # set -s user-keys[38]  "\\342\\200\\224"  # M-_
        # Doesn't work on Omnitype,Yoozon3
        # set -s user-keys[39]  "\\302\\261"       # M-+
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
            ("35", "<"),
            ("36", ">"),
            ("37", "?"),
            # Doesn't work on Omnitype Keyboard, works on Yoozon3
            ("38", "_"),
            # Doesn't work on Omnitype,Yoozon3, generates ~
            ("39", "+"),
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
            set -s user-keys[41]  "\\342\\201\\204"  # M-!
            set -s user-keys[42]  "\\342\\202\\254"  # M-@
            set -s user-keys[43]  "\\342\\200\\271"  # M-#
            set -s user-keys[44]  "\\342\\200\\272"  # M-$
            set -s user-keys[45]  "\\357\\254\\201"  # M-%
            set -s user-keys[46]  "\\357\\254\\202"  # M-^
            set -s user-keys[47]  "\\342\\200\\241"  # M-&
            set -s user-keys[48]  "\\302\\260"       # M-*
            set -s user-keys[49]  "\\302\\267"       # M-(
            set -s user-keys[50]  "\\342\\200\\232"  # M-)
            """
            )

            for i, c in (
                ("41", "!"),
                ("42", "@"),
                ("43", "#"),
                ("44", "$"),
                ("45", "%"),
                ("46", "^"),
                ("47", "&"),
                ("48", "*"),
                ("49", "("),
                ("50", ")"),
            ):
                w(f'bind -N "Enables M-{c}" -n  User{i}  send "M-{c}"')
        w()

        #
        #  AAARRGH
        #  User-keys aren't parsed by tmux if they are bound to
        #  send-keys. If the resulting key has an action,
        #  we need to override and bind the user-key to this action.
        #
        self.display_plugins_used_UK(M_P="User16")
        self.kill_tmux_server_UK(M_X="User24")
        self.split_entire_window_UK(
            M_H="User8", M_J="User10", M_K="User11", M_L="User12"
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
#  If this is run directly
#
if __name__ == "__main__":
    IshConsole().run()
