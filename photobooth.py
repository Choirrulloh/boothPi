#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import time
import subprocess, threading
import re
import Image, ImageTk, ImageOps
import RPi.GPIO as GPIO
import os, os.path, sys
from includes.PhotoThread import PhotoThread
from includes.PhotoLoadThread import PhotoLoadThread
from includes.functions import *

# Size the thumbnails will be shown on screen.
IMAGE_SIZE = 500

# This script will look for a camera with the following USB-ID. Check yours with 'lsusb'.
CAMERA_ID = "04a9:3110"

VERSION="0.2"

lines = [
	[1000, "text", "9"],
	[1000, "text", "8"],
	[1000, "text", "7"],
	[1000, "text", "6"],
	[1000, "text", "5"],
	[1000, "text", "4"],
	[1000, "text", "3"],
	[1000, "text", "2"],
	[100, "text", "1"],
	[1, "photo", 1],
	[4000, "text", "Sehr schön.\nDas gleiche Spiel nochmal.\nFertig?"],
	[1000, "text", "7"],
	[1000, "text", "6"],
	[1000, "text", "5"],
	[1000, "text", "4"],
	[1000, "text", "3"],
	[1000, "text", "2"],
	[100, "text", u"Lächeln!"],
	[1, "photo", 2],
	[4000, "text", "Jetzt kommt Nummer 3!"],
	[1000, "text", "7"],
	[100, "text", "6"],
	[1, "photo", 3],
	[4000, "text", "Verarscht. :-P"],
	[4000, "text", "Jetzt Nummer 4.\nDann habt ihr es\nauch schon hinter euch."],
	[1000, "text", "7"],
	[1000, "text", "6"],
	[1000, "text", "5"],
	[1000, "text", "4"],
	[1000, "text", "3"],
	[1000, "text", "2"],
	[100, "text", "1"],
	[1, "photo", 4],
	[4000, "text", "Das war's auch schon...\n\nBleibt aber mal noch sitzen..."],
	[4000, "text", "Lasst uns doch mal\neinen Blick auf die\nFotos werfen!"],
	[25000, "overview"],
	[1, "clear"],
	[10000, "text", "Jetzt seid ihr aber fertig.\nViel Spaß noch.\n\n(Ihr dürft mich gerne auch\nnochmal nutzen.) ;-)"],
	[1, "text", "Hinsetzen,\nAccessoires aussuchen,\nfertig machen\n-\nund dann den großen\nroten Knopf drücken."]
]


init()

