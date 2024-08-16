# TODO

## Multi user deploy plan

Make this possible to use by more than one user on the same system

Use a file ~/.my_tmux_conf with some variables:

repo_location - checkout folder, set on deploy if not pressent
bin_destination - where myt & rt should be installed by ./deploy

myt & rt should read this file to find where my_tmux_conf is located

## investigate detach-on-destroy

for 24bit color, check if it is mosh session, if so ensure mosh >= 1.4

## Ensure that all sessions get the tpm_init_indicator set & cleared

### Python tools

need to reconfigure vscode so that they work again

- black
- bandit
- flake8
- pylint
