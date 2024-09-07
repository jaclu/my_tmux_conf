#!/bin/sh

#  where  my_tmux_conf is located
f_destination="$HOME"/.config/my_tmux_conf_location
[ ! -f "$f_destination" ] && {
    echo "Location of my_tmux_conf repo not stored, go to repo folder"
    echo "and run ./deploy to solve his"
    exit 1
}

my_tmux_conf_location="$(cat "$f_destination")"
[ ! -d "$my_tmux_conf_location" ] && {
    echo "Location of my_tmux_conf repo incorrect, go to repo folder"
    echo "and run ./deploy to solve his"
    exit 1
}

# more detailed results, not sure yet if its worthwhile to display.
# py 3.12.2 Darwin  12M - 996
# iSH Debian 10 - iPad 7th 8 mins
#   py 3.12.2       13M - 996
# py 3.12.3 Linux   13M - 997
# iSH Alpine 3.20 - iPad 7th 8 mins
#   py 3.12.3       12.4M   - 996

echo
echo "On some systems like iSH or Termux, creating the venv can take a really"
echo "long time."
if [ -d /proc/iSH ]; then
    echo " example: iPad 7th - 8 mins"
fi
echo "Running this in paralell will indicate status of the venv install, be aware"
echo "that sometimes it takes a while for any changes to happen, so give it time..."
echo "Expected results when completed (they migt go higher during the process)"
echo "are aproximately:"

if [ "$(uname -o)" = "Android" ]; then
    echo "  size  29M  -  file count: 1520"
elif [ "$(uname -s)" = "Linux" ] || [ "$(uname -s)" = "Darwin" ]; then
    echo "  size  13M  -  file count: 997"
fi
echo

d_venv="$my_tmux_conf_location"/.venv
while true; do
    if [ -d "$d_venv" ]; then
	printf "size: %s   -  file count:  %s\n" \
	       "$(du -sh  | cut -f1)" \
	       "$(find "$my_tmux_conf_location"/.venv | wc -l)"
    else
	echo "Not present ATM: $d_venv"
	fi
    sleep 1
done
