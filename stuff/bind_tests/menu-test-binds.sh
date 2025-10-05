#!/bin/sh
#
#   Copyright (c) 2022-2025: Jacob.Lundqvist@gmail.com
#   License: MIT
#
#   Part of https://github.com/jaclu/tmux-menus
#
#   Handling pane
#

static_content() {
    # shellcheck disable=SC2154
    $cfg_display_cmds && display_commands_toggle 1

    set -- 0.0 S
    set -- "$@" 0.0 C l "last-window" last-window
    menu_generate_part 2 "$@"
}


#===============================================================
#
#   Main
#
#===============================================================

# shellcheck disable=SC2034
menu_name="Test binds"

#  Full path to tmux-menux plugin, remember to do one /.. for each subfolder
D_TM_BASE_PATH=~/t2/tmux/plugins/tmux-menus

# shellcheck source=/dev/null
. "$D_TM_BASE_PATH"/scripts/dialog_handling.sh
