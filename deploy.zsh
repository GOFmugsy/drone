#!/bin/zsh

CPYDIR="/Volumes/CIRCUITPY"

if [ ! -d "$CPYDIR" ]; then
	echo "$CPYDIR not found" >&2
	exit 1
fi

cp code.py $CPYDIR/
