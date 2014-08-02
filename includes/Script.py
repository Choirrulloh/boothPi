import Settings, Output
from functions import *

lines = []
line = 0

def show_text(text, delay=1000):
	lines.append([delay, "text", text])

def take_photo(index):
	lines.append([1, "photo", index])

def show_overview(delay):
	lines.append([delay, "overview", None])

def clear_screen():
	lines.append([1, "clear", None])

def wait_for_button_press():
	lines.append([1, "wait", None])

def countdown(start, end, delay=1000):
	if (end > start):
		raise "countdown has to go from a large number to a smaller number."
	for number in range(start, end-1, -1):
		lines.append([delay, "text", str(number)])

def start():
	line = 0
	next_step()

def next_step():
	global line

	delay, command, additional = lines[line]
	line += 1
	if line>=len(lines):
		line = 0

	if command=="text":
		print("Text: " + additional)
		display_text(additional)
	elif command=="photo":
		print("Photo! Nummer " + str(additional))
		call_photo_thread(additional)
	elif command=="overview":
		do_show_overview()
	elif command=="clear":
		do_clear_screen()
	elif command=="wait":
		print("Warte auf button_pressed")
		root().after(1, lambda: check_button_pressed(first_run=True))
		return

	if lines[line][1]=="photo":
		delay = max(delay - Settings.PHOTO_DELAY, 1)
		
	print("Warte: " + str(delay))

	root().after(delay, Script.next_step)
