#!/bin/sh

error_msg() {
    printf 'ERROR: %s\n' >/dev/stderr "$1"
    exit 1
}

do_action() {
    tmx_vers="$1"
    [ -z "$tmx_vers" ] && error_msg "do_action() - no param"
    tmx_cmd=~/.asdf/installs/tmux/"$tmx_vers"/bin/tmux

    # cmd="$tmx_cmd -V"
    cmd="$tmx_cmd list-commands"

    echo "do_action($tmx_vers)"
    $cmd >/dev/null
    ex_cde="$?"
    if [ "$ex_cde" != 0 ]; then
	error_msg "Cmd failed: $cmd"
    fi
}


oldest_first() {
    do_action 0.8
    do_action 0.9
    do_action 1.0
    do_action 1.1
    do_action 1.4
    do_action 1.5
    do_action 1.6
    do_action 1.7
    do_action 1.8
    do_action 1.9
    do_action 1.9a
    do_action 2.0
    do_action 2.1
    do_action 2.2
    do_action 2.3
    do_action 2.4
    do_action 2.5
    do_action 2.6
    do_action 2.7
    do_action 2.8
    do_action 2.9
    do_action 2.9a
    do_action 3.0
    do_action 3.0a
    do_action 3.1
    do_action 3.1a
    do_action 3.1b
    do_action 3.1c
    do_action 3.2
    do_action 3.2a
    do_action 3.3
    do_action 3.3a
    do_action 3.4
    do_action 3.5
    do_action 3.5a
}

newest_first() {
    do_action 3.5a
    do_action 3.5
    do_action 3.4
    do_action 3.3a
    do_action 3.3
    do_action 3.2a
    do_action 3.2
    do_action 3.1c
    do_action 3.1b
    do_action 3.1a
    do_action 3.1
    do_action 3.0a
    do_action 3.0
    do_action 2.9a
    do_action 2.9
    do_action 2.8
    do_action 2.7
    do_action 2.6
    do_action 2.5
    do_action 2.4
    do_action 2.3
    do_action 2.2
    do_action 2.1
    do_action 2.0
    do_action 1.9a
    do_action 1.9
    do_action 1.8
    do_action 1.7
    do_action 1.6
    do_action 1.5
    do_action 1.4
    do_action 1.1
    do_action 1.0
    do_action 0.9
    do_action 0.8
}



newest_first
