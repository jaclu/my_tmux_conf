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

echo
echo "On some systems like iSH or Termux, creating the venv can take a really"
echo "long time. Running this in paralell will indicate if something is"
echo "happening or the system has gotten stuck."
echo "Expected results when completed are (aproximations):"

if [ "$(uname -o)" = "Android" ]; then
    echo "  size  29M  -  file count: 1520"
elif [ "$(uname -s)" = "Linux" ]; then
    echo "  size  13M  -  file count: 997"
else
    echo "  size  unknown  -  file count: unknown"
fi
echo

while true; do
    printf "size: %s   -  file count:  %s\n" \
	   "$(du -sh "$my_tmux_conf_location"/.venv/ | cut -f1)" \
	   "$(find "$my_tmux_conf_location"/.venv | wc -l)"
    sleep 1
done
