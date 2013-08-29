#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import time
import subprocess
import re
import Image, ImageTk, ImageOps
import RPi.GPIO as GPIO

IMAGE_SIZE = 240

def quit():
	root.destroy()


line = 0
lines = [
	[1500, "text", "5"],
	[1500, "text", "4"],
	[1500, "text", "3"],
	[1500, "text", "2"],
	[100, "text", "1"],
	[1, "photo", 1],
	[3000, "text", "Sehr schön.\nGleich dassselbe nochmal.\nFertig?"],
	[1500, "text", "3"],
	[1500, "text", "2"],
	[100, "text", u"Lächeln!"],
	[1, "photo", 2],
	[3000, "text", "Jetzt kommt Nummer 3!"],
	[1500, "text", "3"],
	[1500, "text", "2"],
	[100, "text", "1"],
	[1, "photo", 3],
	[3000, "text", "Und Nummer 4.\nDann habt ihr es\nauch schon hinter euch."],
	[1500, "text", "3"],
	[1500, "text", "2"],
	[100, "text", "1"],
	[1, "photo", 4],
	[5000, "text", "Danke, das war's.\n\nViel Spaß noch\nauf der Hochzeit. ;-)"],
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

canvas = Canvas(root, width=w, height=h, bg="Black")
canvas.pack()

text = canvas.create_text(w/2, h/2, text="PhotoBooth v0.1", fill="red", anchor="c")

filename_schema = "photos/this-should-not-happen---{}.jpg"

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
	print "check_button_pressed()"
	button_pressed = GPIO.input(12)
	if button_pressed:
		start_run()
	else:
		root.after(5, check_button_pressed)

def start_run():
	global filename_schema
	global canvas
	global h, space
	filename_schema = time.strftime("%Y%m%d-%H%M%S---{}.jpg")
	print "h: " + str(h)
	width = space*2+IMAGE_SIZE
	print "width: " + str(width)
	canvas.create_rectangle(0, 0, width, h, fill="White")
	canvas.pack()
	advance_line()

def reset_usb():
	global usb_device
	print "In reset_usb()"
	cmd = "/home/pi/usbreset " + usb_device
	print "Executing: " + cmd
	subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).stdout.read()

def display_text(string):
	global canvas
	global text
	canvas.delete(text)
	text = canvas.create_text(w/2, h/2, text=string, fill="#45ADA6", anchor="c", font="Lucida 90", justify=CENTER)

def take_photo(number):
	global filename_schema
	global canvas
	global images
	global space
	reset_usb()
	print("This is take_photo() in dummy mode")
	result = subprocess.Popen("gphoto2 --capture-image-and-download --force-overwrite --filename " + filename_schema.format(number), stdout=subprocess.PIPE, shell=True).stdout.read()
	print result
	display_text("Lade Daten...")
	canvas.pack()
	image = Image.open(filename_schema.format(number))
	print "1"
	image = ImageOps.fit(image, (IMAGE_SIZE, IMAGE_SIZE)) # image.thumbnail((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
	print "1.1"
	images[number-1] = ImageTk.PhotoImage(image)
	print "2"
	canvas.create_image(space, number*space + (number-1)*IMAGE_SIZE, image=images[number-1], anchor="nw")
	print "3"
	canvas.pack()
	print "4"

def show_overview():
	global filename_schema, canvas, images, w, h
	border = 50
	img_size = (h - 3*50) / 2
	for i in range(1, 4):
		img = Image.open(filename_schema.format(i))
		img = ImageOps.fit(img, (img_size, img_size))
		images[i-1] = ImageTk.PhotoImage(img)
		canvas.create_image(i % 2 + 1, (i-1) / 2, image=images[i], anchor="nw")
	canvas.pack()

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

