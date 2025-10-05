#!/usr/bin/env bash
#
#  Copyright (c) 2020-2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/tmux-multi-node
#
#  Original picked from the net
#

for i in {0..255}; do
    printf "\\x1b[38;5;%smcolour%s\\x1b[0m\\n" "$i" "$i"
done
