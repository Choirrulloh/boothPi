#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import time
import subprocess, threading
import re
import Image, ImageTk, ImageOps
import RPi.GPIO as GPIO
import os, os.path, sys
from includes import PhotoThread, PhotoLoadThread, USBDevice
from includes.functions import *

# Size the thumbnails will be shown on screen.
IMAGE_SIZE = 500

# This script will look for a camera with the following USB-ID. Check yours with 'lsusb'.
CAMERA_ID = "04a9:3110"

VERSION="0.2"

Script.show_text(             text="Hinsetzen,\nAccessoires aussuchen,\nfertig machen\n-\nund dann den großen\nroten Knopf drücken.")
Script.wait_for_button_press()
Script.show_text(             text="9")
Script.show_text(             text="8")
Script.show_text(             text="7")
Script.show_text(             text="6")
Script.show_text(             text="5")
Script.show_text(             text="4")
Script.show_text(             text="3")
Script.show_text(             text="2")
Script.show_text(delay=100,   text="1")
Script.take_photo(1)
Script.show_text(delay=4000,  text="Sehr schön.\nDas gleiche Spiel nochmal.\nFertig?")
Script.show_text(             text="7")
Script.show_text(             text="6")
Script.show_text(             text="5")
Script.show_text(             text="4")
Script.show_text(             text="3")
Script.show_text(             text="2")
Script.show_text(delay=100,   text=u"Lächeln!")
Script.take_photo(2)
Script.show_text(delay=4000,  text="Jetzt kommt Nummer 3!")
Script.show_text(             text="7")
Script.show_text(delay=100,   text="6")
Script.take_photo(3)
Script.show_text(delay=4000,  text="Verarscht. :-P")
Script.show_text(delay=4000,  text="Jetzt Nummer 4.\nDann habt ihr es\nauch schon hinter euch.")
Script.show_text(             text="7")
Script.show_text(             text="6")
Script.show_text(             text="5")
Script.show_text(             text="4")
Script.show_text(             text="3")
Script.show_text(             text="2")
Script.show_text(delay=100,   text="1")
Script.take_photo(4)
Script.show_text(delay=4000,  text="Das war's auch schon...\n\nBleibt aber mal noch sitzen...")
Script.show_text(delay=4000,  text="Lasst uns doch mal\neinen Blick auf die\nFotos werfen!")
Script.show_overview(delay=25000)
Script.clear_screen()
Script.show_text(delay=10000, text="Jetzt seid ihr aber fertig.\nViel Spaß noch.\n\n(Ihr dürft mich gerne auch\nnochmal nutzen.) ;-)")


init()

