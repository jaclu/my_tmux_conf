# TODO

## 25-04-30 Clear pane shortcut issue

the root bind overrides the prefix bind as is, Consider to use something that can be done
in t2 without being eaten up by main env, ideally with a basic key for accessibility even
on limited keyboard scenarios

## M-S Left/Right temp disabled 25-03-10

they used to be used for split pane, will become next/prev window once I have
unlearned to use them for pane split

## Full access to your own plugins

Come up with a simple way to indicate using this notation where it is allowed

`set -g @plugin 'git@github.com/user/plugin'`

## plugins to check

[try to be mostly bind compatible](https://github.com/tmux-plugins/tmux-pain-control)

## M-9 & M-0 collides with ish_console

windows_handling() - M-9 & M-0 collides with ish_console

## investigate detach-on-destroy

for 24bit color, check if it is mosh session, if so ensure mosh >= 1.4

## Ensure that all sessions get the tpm_init_indicator set & cleared

### Python tools

need to reconfigure vscode so that they work again

- black
- bandit
- flake8
- pylint
