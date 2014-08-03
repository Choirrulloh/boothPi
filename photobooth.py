#!/usr/bin/env python
# -*- coding: utf-8 -*-

from includes import Settings

# Size the thumbnails will be shown on screen.
Settings.IMAGE_SIZE = 500

# Time (in ms) this specific camera needs between telling it to take a photo and it actually taking a photo.
# It's best to determine this by try-and-error...
# 900ms is the correct value for an EOS 400D in manual mode.
Settings.PHOTO_DELAY=900

Settings.VERSION="2"

Settings.SIMULATE_USB_DEVICE = False
Settings.DEBUG = True


from Tkinter import *
import RPi.GPIO as GPIO
from includes import PhotoThread, PhotoLoadThread, USBDevice, Script
from includes.functions import *


Script.show_text(             text="Hinsetzen,\nAccessoires aussuchen,\nfertig machen\n-\nund dann den großen\nroten Knopf drücken.")
Script.wait_for_button_press()
Script.countdown(             start=10, end=1)
Script.take_photo(1)
Script.show_text(delay=4000,  text="Sehr schön.\nDas gleiche Spiel nochmal.\nFertig?")
Script.countdown(             start=7, end=2)
Script.show_text(             text=u"Lächeln!")
Script.take_photo(2)
Script.show_text(delay=4000,  text="Jetzt kommt Nummer 3!")
Script.countdown(             start=7, end=6)
Script.take_photo(3)
Script.show_text(delay=4000,  text="Verarscht. :-P")
Script.show_text(delay=4000,  text="Jetzt Nummer 4.\nDann habt ihr es\nauch schon hinter euch.")
Script.countdown(             start=7, end=1)
Script.take_photo(4)
Script.show_text(delay=4000,  text="Das war's auch schon...\n\nBleibt aber mal noch sitzen...")
Script.show_text(delay=4000,  text="Lasst uns doch mal\neinen Blick auf die\nFotos werfen!")
Script.show_overview(delay=25000)
Script.clear_screen()
Script.show_text(delay=10000, text="Jetzt seid ihr aber fertig.\nViel Spaß noch.\n\n(Ihr dürft mich gerne auch\nnochmal nutzen.) ;-)")


init()

