#!/bin/bash
xset s noblank
xset s off
xset s 0
xset -dpms
echo
echo -n "Current system time is: "
date "+%d.%m.%Y %H:%M"
echo
echo "If this is correct, please just press ENTER."
echo "If it is not correct, please enter the current date/time in the format 'YYYYMMDD HH:MM' and press ENTER to confirm."
echo "Example: On May 17th 2016, 3:14pm you'd enter '20160517 15:14'."
echo
read time
echo
if [ "$time" = "" ]; then
	echo "Not changing time."
else
	sudo date -s "$time"
fi
python boothPi.py
