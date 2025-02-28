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
