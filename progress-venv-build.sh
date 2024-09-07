#!/bin/sh

while true; do
    printf "size: %s   -  file count:  %s\n" $(du -sh .venv/ | cut -f1) $(find .venv | wc -l)
    sleep 1
done
