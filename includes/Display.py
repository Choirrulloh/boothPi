from Tkinter import *
import Settings, Output, functions, PhotoThread

__root = None
__canvas = __debug = None
__w = __h = __image_size = 0

def quit(some_var):
	"""Beendet die App."""
	global __root
	__root.destroy()

def image_size(): return __image_size

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

def remove_debug_text():
	if __canvas and __debug:
		__canvas.delete(__debug)

def clear():
	global __canvas
	__canvas.delete(ALL)

def show_overview():
	"""Displays the 4 pictures on the screen. Uses PhotoLoadThreads and still is pretty slow..."""
	global __canvas, __image_size
	__canvas.delete(ALL)
	Output.debug("image_size is " + str(__image_size))
	for i in range(4):
		plt = PhotoThread.photo_load_threads()[i]
		if i==0 or i==1:
			y = __h/2 - Settings.PADDING/2
			anchor = "s"
		if i==2 or i==3:
			y = __h/2 + Settings.PADDING/2
			anchor = "n"
		if i==0 or i==2:
			x = __w/2 - Settings.PADDING/2
			anchor = anchor + "e"
		if i==1 or i==3:
			x = __w/2 + Settings.PADDING/2
			anchor = anchor + "w"
		Output.debug("Warte auf Nummer " + str(i))
		plt.join()
		Output.debug("Zeige Photo von Nummer " + str(i))
		__canvas.create_image(x, y, image=plt.get_photo(), anchor=anchor)
                __canvas.pack()

def root(): return __root

def toggle_debug_mode(event):
	Settings.DEBUG = not Settings.DEBUG
	if not Settings.DEBUG:
		remove_debug_text()

def init(function_to_start_with):
	"""Initializes the display."""
	global __root, __w, __h, space, __canvas, __text, __image_size

	__root = Tk()
	__w, __h = __root.winfo_screenwidth(), __root.winfo_screenheight()
	__root.wm_attributes("-topmost", 1)
	__root.focus()
	__root.focus_force()
	__root.geometry("%dx%d+0+0" % (__w, __h))

	__image_size = (min(__w, __h)-Settings.PADDING)/2

	__canvas = Canvas(__root, width=__w, height=__h, bg="Black")
	__canvas.pack()

	__text = __canvas.create_text(__w/2, __h/2, text="PhotoBooth v"+Settings.VERSION, fill="red", anchor="c")

	__root.focus_set()
	__root.focus_force()
	__root.bind("<Q>", quit)
	__root.bind("<D>", toggle_debug_mode)
	__root.bind("<Key>", functions.override_button_press)
	__root.after(2000, function_to_start_with)
	__root.mainloop()
