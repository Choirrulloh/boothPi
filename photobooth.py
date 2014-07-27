#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import time
import subprocess, threading
import re
import Image, ImageTk, ImageOps
import RPi.GPIO as GPIO
import os, sys

IMAGE_SIZE = 500

def quit():
	root.destroy()

class PhotoThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.photo_taken = False

	def set_data(self, filename, number):
		self.filename = filename
		self.number = number
	
	def run(self):
		self.photo_taken = False
		# Take the photo
		reset_usb()
		print("This is take_photo().")
		process = subprocess.Popen("gphoto2 --capture-image-and-download --force-overwrite --filename " + self.filename, stdout=subprocess.PIPE, shell=True)
		while True:
			line = process.stdout.readline()
			if line == '':
				break
			if line.startswith("New file is in"):
				self.photo_taken = True

		global photo_load_threads
		photo_load_threads[self.number-1] = PhotoLoadThread(self.filename, self.number-1)
		photo_load_threads[self.number-1].start()

class PhotoLoadThread(threading.Thread):
	def __init__(self, filename, index):
		threading.Thread.__init__(self)
		self.filename = filename
		self.index = index
		self.image = None

	def run(self):
		print "PhotoLoadThread " + str(self.index) + " starting..."
		global images, canvas
		# Load the photo
		print "PhotoLoadThread " + str(self.index) + ": Opening..."
		self.image = Image.open(self.filename)
		print "PhotoLoadThread " + str(self.index) + ": Fitting..."
		self.image = ImageOps.fit(self.image, (IMAGE_SIZE, IMAGE_SIZE)) # image.thumbnail((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
		print "PhotoLoadThread " + str(self.index) + ": TKing..."
		images[self.index] = ImageTk.PhotoImage(self.image)
		print "PhotoLoadThread " + str(self.index) + " finished."

	def show_photo(self, canvas):
		global w, h, IMAGE_SIZE
		x = 0
		y = 0
		anchor = ""

		if (self.index / 2 == 0):
			anchor = "s"
			y = h/2 - 25
		else:
			anchor = "n"
			y = h/2 + 25

		if (self.index % 2 == 0):
			anchor += "e"
			x = w/2 - 25
		else:
			anchor += "w"
			x = w/2 + 25

		canvas.create_image(x, y, image=images[self.index], anchor=anchor)
		#canvas.create_image(space, self.index*space + (self.index-1)*IMAGE_SIZE, image=images[self.index], anchor="nw")
		canvas.pack()

line = 0
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

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#w, h = 200, 200
root.overrideredirect(1)
root.wm_attributes("-topmost", 1)
root.focus()
root.geometry("%dx%d+0+0" % (w, h))

space = (h-4*IMAGE_SIZE)/5

images = [None, None, None, None]
photo_load_threads = [None, None, None, None]

canvas = Canvas(root, width=w, height=h, bg="Black")
canvas.pack()

text = canvas.create_text(w/2, h/2, text="PhotoBooth v0.1", fill="red", anchor="c")

filename_schema = "photos/this-should-not-happen---{}.jpg"

photo_thread = PhotoThread()

GPIO.setup(12, GPIO.IN)

def detect_usb():
	print "In detect_usb()"
	result = subprocess.Popen("lsusb", stdout=subprocess.PIPE).stdout.read()
	match = re.search("Bus (\d{3}) Device (\d{3}): ID 04a9:3110", result)
	if match != None:
		result = "/dev/bus/usb/" + match.group(1) + "/" + match.group(2)
		print "Path to USB device: " + result
		return result
	raise "USB Device not found!"

usb_device = detect_usb()

def check_button_pressed():
	global root
	button_pressed = GPIO.input(12)
	if button_pressed:
		start_run()
	else:
		root.after(5, check_button_pressed)

def start_run():
	global filename_schema
	global canvas
	global h, space
	global line
	global text_offset
	filename_schema = time.strftime("photos/%Y%m%d-%H%M%S---{}.jpg")
	print "h: " + str(h)
	width = space*2+IMAGE_SIZE
	print "width: " + str(width)
	canvas.pack()
	line = 0
	advance_line()

def reset_usb():
	global usb_device
	print "In reset_usb()"
	cmd = os.path.abspath(os.path.dirname(sys.argv[0])) + "/usbreset " + usb_device
	print "Executing: " + cmd
	subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).stdout.read()

def display_text(string):
	global canvas
	global text
	canvas.delete(text)
	text = canvas.create_text(w/2, h/2, text=string, fill="#45ADA6", anchor="c", font="Lucida 90", justify=CENTER)

def take_photo(number):
	global photo_thread
	global filename_schema
	photo_thread.set_data(filename_schema.format(number), number)
	photo_thread.run()
	while True:
		print "Warte auf photo_taken..."
		if photo_thread.photo_taken:
			break
		time.sleep(0.1)

def show_overview():
	global photo_load_threads, canvas
	border = 50
	img_size = (h - 3*50) / 2
	canvas.delete(ALL)
	for i in range(4):
		print "Warte auf Nummer " + str(i)
		photo_load_threads[i].join()
		print "Zeige Photo von Nummer " + str(i)
		photo_load_threads[i].show_photo(canvas)

def advance_line():
	global line
	global lines
	if line>=len(lines):
		line = 0
		return
	current_line = lines[line]
	if current_line[1]=="text":
		print("Text: " + current_line[2])
		display_text(current_line[2])
	elif current_line[1]=="photo":
		print("Photo! Nummer " + str(current_line[2]))
		take_photo(current_line[2])
	elif current_line[1]=="overview":
		show_overview()
	elif current_line[1]=="clear":
		global canvas
		canvas.delete(ALL)
	print("Warte: " + str(current_line[0]))
	if line+1<len(lines):
		root.after(current_line[0], advance_line)
	else:
		root.after(1000, check_button_pressed)
	line += 1

def init():
	global lines
	display_text(lines[len(lines)-1][2])
	root.after(1000, check_button_pressed)

root.focus_set()
root.bind("<Escape>", quit)
root.after(2000, init)
root.mainloop()

