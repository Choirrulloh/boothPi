lines = []
line = 0

def show_text(text, delay=1000):
	lines << [delay, "text", additional]

def take_photo(index):
	lines << [1, "photo", index]

def show_overview(delay):
	lines << [delay, "overview", None]

def clear_screen():
	lines << [1, "clear", None]

def wait_for_button_press():
	lines << [1, "wait", None]

def start():
	line = 0
	next_step()

def next_step():
	global root

	if line>=len(lines):
		line = 0
		return
	delay, command, additional = lines[line]
	line += 1
	if command=="text":
		print("Text: " + additional)
		display_text(additional)
	elif command=="photo":
		print("Photo! Nummer " + str(additional))
		take_photo(additional)
	elif command=="overview":
		show_overview()
	elif command=="clear":
		global canvas
		canvas.delete(ALL)
	elif command=="wait":
		print("Warte auf button_pressed")
		root.after(1, check_button_pressed)
		return
	print("Warte: " + str(delay))

	root.after(delay, Script.next_step)