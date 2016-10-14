#!/usr/bin/env python
# -*- coding: utf-8 -*-

from includes import Settings

# Time (in ms) this specific camera needs between telling it to take a photo and it actually taking a photo.
# It's best to determine this by try-and-error...
# 900ms is the correct value for an EOS 400D in manual mode.
Settings.PHOTO_DELAY=900

Settings.PADDING = 20

Settings.VERSION="2"

Settings.SIMULATE_USB_DEVICE = False
Settings.DEBUG = False
Settings.DEBUG_SHORT_DELAYS = False


from Tkinter import *
import RPi.GPIO as GPIO
from includes import PhotoThread, PhotoLoadThread, USBDevice, functions, Script

# We define three scripts
main = Script.Script()
run = Script.Script()
express = Script.Script()

# Main will be the main script.
# It will tell the people to sit down, look at the accessoires and then push the button. Then it will run the "run" script.
main.show_text(             text="Hinsetzen,\nAccessoires aussuchen,\nfertig machen\n-\nund dann den großen\nroten Knopf drücken.")
main.wait_for_button_press()
main.branch(run)

# The run script for a standard run of the photobooth.
# init_run() has to be called at the beginning of each run!
run.init_run()
# Thanks to branch_on_keypress, you can switch to the "express" script by pressing the button during the first countdown.
run.countdown(             start=10, end=1, branch_on_keypress=express)
run.take_photo(1)
run.show_text(delay=4000,  text="Sehr schön.\nDas gleiche Spiel nochmal.\nFertig?")
run.countdown(             start=7, end=2)
run.show_text(             text="Lächeln!")
run.take_photo(2)
run.show_text(delay=4000,  text="Jetzt kommt Nummer 3!")
# Yes, the countdown only goes down to 6. It's to surprise the people and in return get (more or less) funny pictures of people not really ready for a photo.
run.countdown(             start=7, end=6)
run.take_photo(3)
run.show_text(delay=4000,  text="Verarscht. :-P")
run.show_text(delay=4000,  text="Jetzt Nummer 4.\nDann habt ihr es\nauch schon hinter euch.")
run.countdown(             start=7, end=1)
run.take_photo(4)
run.show_text(delay=4000,  text="Das war's auch schon...\n\nBleibt aber mal noch sitzen...")
run.show_text(delay=4000,  text="Lasst uns doch mal\neinen Blick auf die\nFotos werfen!")
# The overview and the last text can be shortened by pushing the button, thanks to "branch_on_keypress=run".
run.show_overview(delay=25000, branch_on_keypress=run)
run.clear_screen()
run.show_text(delay=10000, text="Jetzt seid ihr aber fertig.\nViel Spaß noch.\n\nNächstes Mal drückt zum Start\n2x den Knopf, dann geht es schneller.", branch_on_keypress=run)
run.branch(main)

# The express run script. Not much text, just (shorter) countdowns and photos.
# This doesn't call init_run(), because it can only be reached after the "run" script has run init_run(). (But it also wouldn't hurt to do it again here.)
express.show_text(delay=2000, text="Express-Mode!\n4x 5 Sekunden!")
express.countdown(          start=5, end=1, additional_text="Photo 1")
express.take_photo(1)
express.countdown(          start=5, end=1, additional_text="Photo 2")
express.take_photo(2)
express.countdown(          start=5, end=1, additional_text="Photo 3")
express.take_photo(3)
express.countdown(          start=5, end=1, additional_text="Photo 4")
express.take_photo(4)
express.show_text(delay=5000, text="Bereite Fotos vor...")
express.show_overview(delay=20000)
express.clear_screen()
express.branch(main)

# Start the app with the "main" script.
functions.init(main)

