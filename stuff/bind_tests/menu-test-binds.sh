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
    # shellcheck disable=SC2154 # nav_home defined in scripts/dialog_handling.sh
    set -- 0.0 M Left "Back to Main menu  $nav_home" main.sh
    menu_generate_part 1 "$@"
    # shellcheck disable=SC2154 # cfg_display_cmds defined in scripts/dialog_handling.sh
    $cfg_display_cmds && display_commands_toggle 2 # give this its own menu part idx

    set -- 0.0 S 0.0 C l "last-window" last-window
    menu_generate_part 3 "$@"
}


#===============================================================
#
#   Main
#
#===============================================================

# shellcheck disable=SC2034
menu_name="Test binds"

#  Full path to tmux-menux plugin, remember to do one /.. for each subfolder
D_TM_BASE_PATH=$HOME/t2/tmux/plugins/tmux-menus

# shellcheck source=/dev/null
. "$D_TM_BASE_PATH"/scripts/dialog_handling.sh
