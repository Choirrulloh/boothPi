import Settings, Output, Display, functions

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
		Display.display_text(additional)
	elif command=="photo":
		Output.debug("Photo! Number " + str(additional))
		functions.call_photo_thread(additional)
	elif command=="overview":
		Display.show_overview()
	elif command=="clear":
		Display.clear()
	elif command=="wait":
		Output.debug("Calling check_button_pressed...")
		functions.check_button_pressed(first_run=True)
		return

	if lines[line][1]=="photo":
		delay = max(delay - Settings.PHOTO_DELAY, 1)

	if Settings.DEBUG_SHORT_DELAYS:
		delay = delay / 100 + 1
		
	Output.debug("Waiting: " + str(delay))

	Display.root().after(delay, next_step)
