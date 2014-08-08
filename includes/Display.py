from Tkinter import *
import Settings, Output, functions, PhotoThread

__root = None
__canvas = __debug = None
__w = __h = 0

def quit(some_var):
	"""Beendet die App."""
	global __root
	__root.destroy()

def display_text(string):
	"""Displays a text on the screen."""
	global __text, __canvas, __w, __h
	__canvas.delete(__text)
	__text = __canvas.create_text(__w/2, __h/2, text=string, fill="#45ADA6", anchor="c", font="Lucida 90", justify=CENTER)
	Output.debug("Text: " + string.replace("\n", "\\n"))

def display_debug(string):
	"""Displays debug strings on screen."""
	global __debug
	if __canvas:
		if __debug:
			__canvas.delete(__debug)
		__debug = __canvas.create_text(0, 0, text=string, fill="#aaaaaa", font="Lucida 12", anchor="nw")

def clear():
	global __canvas
	__canvas.delete(ALL)

def show_overview():
	"""Displays the 4 pictures on the screen. Uses PhotoLoadThreads and still is pretty slow..."""
	global __canvas
	__canvas.delete(ALL)
	for i in range(4):
		Output.debug("Warte auf Nummer " + str(i))
		PhotoThread.photo_load_threads()[i].join()
		Output.debug("Zeige Photo von Nummer " + str(i))
		PhotoThread.photo_load_threads()[i].show_photo(__canvas, __w, __h)

def root(): return __root

def init(function_to_start_with):
	"""Initializes the display."""
	global __root, __w, __h, space, __canvas, __text, filename_schema, photo_thread, usb_device

	__root = Tk()
	__w, __h = __root.winfo_screenwidth(), __root.winfo_screenheight()
	__root.wm_attributes("-topmost", 1)
	__root.focus()
	__root.focus_force()
	__root.geometry("%dx%d+0+0" % (__w, __h))

	space = (__h-4*Settings.IMAGE_SIZE)/5

	__canvas = Canvas(__root, width=__w, height=__h, bg="Black")
	__canvas.pack()

	__text = __canvas.create_text(__w/2, __h/2, text="PhotoBooth v"+Settings.VERSION, fill="red", anchor="c")

	__root.focus_set()
	__root.focus_force()
	__root.bind("<Q>", quit)
	__root.bind("<space>", functions.override_button_press)
	__root.after(2000, function_to_start_with)
	__root.mainloop()
