#!/bin/sh

#
#  On some systems like iSH or Termux, creating the venv
#  can take a really long time. Running this in paralell
#  will indicate if something is happening or the system
#  got stuck. Expected result when completed is
#  size aprox 29M and file count: 1520
#
while true; do
    printf "size: %s   -  file count:  %s\n" \
	   "$(du -sh .venv/ | cut -f1)" "$(find .venv | wc -l)"
    sleep 1
done
