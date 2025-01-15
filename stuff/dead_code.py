#!/usr/bin/env python3
#
#  -*- mode: python; mode: fold -*-
#
#  Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#

"""Placeholder for dead code, maybe will be used again"""

from base import BaseConfig  # BaseConfig


class NotUsedtPlugins(BaseConfig):
    """Things not used ATM in DefaultPlugins"""

    skip_plugin_fzf_session_switch = False
    use_plugin_jump = False
    skip_plugin_tmux_fzf = False

    def plugin_fzf_session_switch(self) -> list:  # 3.3
        """can be used on older versions with limitations"""
        if self.skip_plugin_fzf_session_switch:
            vers_min = -1.0
        else:
            vers_min = 3.3
        return [
            "vndmp4/tmux-fzf-session-switch",
            vers_min,
            """
            # set -g @fzf-goto-session 's'  # trigger key
            # set -g @fzf-goto-session-without-prefix 'true'
            # set-option -g @fzf-goto-session-only 'true'
            """,
        ]

    def plugin_jump(self) -> list:  # 1.8
        """Good idea but doesn't seem to work on upper case

        Jump to word(-s) on the screen that you want to copy,
        without having to use the mouse.
        Default trigger: <prefix> j
        """
        if self.use_plugin_jump:
            min_vers = 1.8
        else:
            min_vers = -1.0  # Dont use

        return [
            "jaclu/tmux-jump",  # was Lenbok
            min_vers,
            #
            #  The weird jump key syntax below is how I both sneak in
            #  a note and make the key not to depend on prefix :)
            #
            """#  Additional dependency: ruby >= 2.3
            set -g @jump-key "-N plugin_Lenbok/tmux-jump -n  M-j"
            set -g @jump-keys-position 'off_left'
            """,
        ]

    def plugin_tmux_fzf(self) -> list:
        """Not impressed so far"""
        if self.skip_plugin_tmux_fzf:
            vers_min = -1.0
        else:
            vers_min = 2.0
        return [
            "sainnhe/tmux-fzf",
            vers_min,
            """
            # TMUX_FZF_LAUNCH_KEY="C-f"
            # TMUX_FZF_PREVIEW=0  # disable preview
            # TMUX_FZF_PREVIEW_FOLLOW=0  # disable preview follow
            # TMUX_FZF_ORDER="session|window|pane|command|keybinding|clipboard|process"
            """,
        ]
