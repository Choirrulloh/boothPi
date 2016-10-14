from Tkinter import *
import threading, glob, os
import Settings, Output, functions, PhotoThread

__root = None
__canvas = __debug = None
__w = __h = __image_size = 0

def quit(some_var):
	"""Beendet die App."""
	global __root
	__root.destroy()

def image_size(fullscreen=False):
        if fullscreen: return min(__w, __h)
        return __image_size

def display_text(string):
	"""Displays a text on the screen."""
	global __text, __canvas, __w, __h
	__canvas.delete(__text)
	__text = __canvas.create_text(__w/2, __h/2, text=string, fill=Settings.TEXT_COLOR, anchor="c", font=Settings.TEXT_FONT, justify=CENTER)
	Output.debug("Text: " + string.replace("\n", "\\n"))

def display_debug(string):
	"""Displays debug strings on screen."""
	global __debug
	if not threading.current_thread().__class__.__name__ == "_MainThread":
		return
	if __canvas:
		if __debug:
			__canvas.delete(__debug)
		__debug = __canvas.create_text(0, 0, text=string, fill="#aaaaaa", font="Lucida 12", anchor="nw")

def display_stats(some_var):
        clear()
        text = "Runs during this instance: {}\n".format(Settings.runs)
        text+= "Number of images in photos/: {}\n".format(len(glob.glob("photos/*---*---?.jpg")))
        text+= "\n"
        st = os.statvfs("photos/")
        text+= "Space available: {} MB\n".format(st.f_bavail * st.f_frsize / 1024 / 1024)
        text+= "\n"
        text+= "Press any key to continue"
        __canvas.create_text(0, 0, text=text, anchor="nw", font="Lucida 30", fill="white")
        Settings.ON_BUTTON_PRESS = Settings.main_script.start
        Settings.WAIT_FOR_BUTTON_PRESS = True
        
def display_help(some_var):
        clear()
        text = "Shift-Q: Quit this app.\n"
        text+= "Shift-S: Show some stats.\n"
        text+= "Shift-P: Make and display a single photo.\n"
        text+= "Shift-D: Toggle debug mode.\n"
        text+= "\n"
        text+= "Control-Shift-Alt-Q: Shutdown.\n"
        text+= "\n"
        text+= "Press any key to continue."
        __canvas.create_text(0, 0, text=text, anchor="nw", font="Lucida 30", fill="white")
        Settings.ON_BUTTON_PRESS = Settings.main_script.start
        Settings.WAIT_FOR_BUTTON_PRESS = True

def remove_debug_text():
	if __canvas and __debug:
		__canvas.delete(__debug)

def clear():
	global __canvas
	__canvas.delete(ALL)

def show_overview():
	"""Displays the 4 pictures on the screen. Uses PhotoLoadThreads and still is pretty slow..."""
	global __canvas, __image_size, __w, __h, download_id
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
        id = __canvas.create_text(__w, __h, text="{} {}".format(functions.download_id[0:4], functions.download_id[4:8]), fill="white", font=Settings.TEXT_ID_FONT, anchor="se")
        box = __canvas.create_rectangle(__canvas.bbox(id), fill="black")
        __canvas.tag_lower(box, id)
        __canvas.pack()

def show_single_photo():
        global __canvas, __w, __h
        clear()
        Output.debug("This is show_single_photo().")
        Output.debug("Waiting for PhotoLoadThread to join...")
        PhotoThread.photo_load_threads()[0].join()
        Output.debug("Getting photo...")
        __canvas.create_image(__w/2, __h/2, image=PhotoThread.photo_load_threads()[0].get_photo(), anchor="c")
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
	if Settings.FULLSCREEN: __root.attributes("-fullscreen", True)
	__root.focus()
	__root.focus_force()
	__root.geometry("%dx%d+0+0" % (__w, __h))

	__image_size = (min(__w, __h)-Settings.PADDING)/2

	__canvas = Canvas(__root, width=__w, height=__h, bg="Black")
	__canvas.pack()

	__text = __canvas.create_text(__w/2, __h/2, text="PhotoBooth v"+Settings.VERSION, fill="red", anchor="c")

	__root.focus_set()
	__root.focus_force()
	__root.bind("<Shift_L>", lambda e: None)
	__root.bind("<Control_L>", lambda e: None)
	__root.bind("<Alt_L>", lambda e: None)
	
	__root.bind("<Shift-Q>", quit)
	__root.bind("<Shift-D>", toggle_debug_mode)
	__root.bind("<Shift-P>", functions.single_photo)
	__root.bind("<Shift-S>", display_stats)
	__root.bind("<Control-Shift-Alt-Q>", functions.shutdown)
	__root.bind("<Shift-H>", display_help)
	
	__root.bind("<Key>", functions.button_pressed)
	
	__root.after(2000, function_to_start_with)
	__root.mainloop()
