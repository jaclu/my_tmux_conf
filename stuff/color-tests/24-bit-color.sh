#!/usr/bin/env bash
#
#  Copyright (c) 2020-2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/tmux-multi-node
#
#  This file was originally taken from iterm2 https://github.com/gnachman/iTerm2/blob/master/tests/24-bit-color.sh
#
#   This file echoes four gradients with 24-bit color codes
#   to the terminal to demonstrate their functionality.
#   The foreground escape sequence is ^[38;2;<r>;<g>;<b>m
#   The background escape sequence is ^[48;2;<r>;<g>;<b>m
#   <r> <g> <b> range from 0 to 255 inclusive.
#   The escape sequence ^[0m returns output to default

SEPARATOR=':'

setBackgroundColor()
{
    echo -en "\x1b[48${SEPARATOR}2${SEPARATOR}$1${SEPARATOR}$2${SEPARATOR}$3""m"
}

resetOutput()
{
    echo -en "\x1b[0m\n"
}

# Gives a color $1/255 % along HSV
# Who knows what happens when $1 is outside 0-255
# Echoes "$red $green $blue" where
# $red $green and $blue are integers
# ranging between 0 and 255 inclusive
rainbowColor()
{ 
    (( h=$1/43 ))
    (( f=$1-43*h ))
    (( t=f*255/43 ))
    (( q=255-t ))

    if [[ $h -eq 0 ]]
    then
        echo "255 $t 0"
    elif [[ $h -eq 1 ]]
    then
        echo "$q 255 0"
    elif [[ $h -eq 2 ]]
    then
        echo "0 255 $t"
    elif [[ $h -eq 3 ]]
    then
        echo "0 $q 255"
    elif [[ $h -eq 4 ]]
    then
        echo "$t 0 255"
    elif [[ $h -eq 5 ]]
    then
        echo "255 0 $q"
    else
        # execution should never reach here
        echo "0 0 0"
    fi
}

for i in $(seq 0 127); do
    setBackgroundColor "$i" 0 0
    echo -en " "
done
resetOutput
for i in $(seq 255 128); do
    setBackgroundColor "$i" 0 0
    echo -en " "
done
resetOutput

for i in $(seq 0 127); do
    setBackgroundColor 0 "$i" 0
    echo -n " "
done
resetOutput
for i in $(seq 255 128); do
    setBackgroundColor 0 "$i" 0
    echo -n " "
done
resetOutput

for i in $(seq 0 127); do
    setBackgroundColor 0 0 "$i"
    echo -n " "
done
resetOutput
for i in $(seq 255 128); do
    setBackgroundColor 0 0 "$i"
    echo -n " "
done
resetOutput

for i in $(seq 0 127); do
    # shellcheck disable=SC2046
    setBackgroundColor $(rainbowColor "$i")
    echo -n " "
done
resetOutput
for i in $(seq 255 128); do
    # shellcheck disable=SC2046
    setBackgroundColor $(rainbowColor "$i")
    echo -n " "
done
resetOutput
