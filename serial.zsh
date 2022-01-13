#!/bin/zsh

TTYUSB="/dev/tty.usbmodem101"

if [[ ! -a "$TTYUSB" ]]; then
	echo "$TTYUSB not found" >&2
	exit 1
fi

screen $TTYUSB
