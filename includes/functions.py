import time, os.path
from distutils import spawn
from Tkinter import *
from RPi import GPIO
import USBDevice, Settings, Script, Output
from PhotoThread import *

override_button_pressed = False

def quit(some_var):
	"""Beendet die App."""
	global root
	root.destroy()

def override_button_press(some_var): 
	global override_button_pressed
	override_button_pressed = True

def check_button_pressed(first_run=False):
	"""This method uses polling to wait for someone to push the button."""
	global root, override_button_pressed
	if first_run: override_button_pressed = False
	button_pressed = GPIO.input(12)
	if button_pressed or override_button_pressed:
		start_run()
	else:
		root.after(5, check_button_pressed)

def start_run():
	"""Starts a new run. Is called whenever someone pushes the button (when the script is waiting for it, of course)."""
	global filename_schema
	global canvas
	global width, space
	filename_schema = time.strftime("photos/%Y%m%d-%H%M%S---{}.jpg")
	width = space*2+Settings.IMAGE_SIZE
	print "width: " + str(width)
	canvas.pack()
	Script.next_step()

def display_text(string):
	"""Displays a text on the screen."""
	global canvas
	global text
	canvas.delete(text)
	text = canvas.create_text(w/2, h/2, text=string, fill="#45ADA6", anchor="c", font="Lucida 90", justify=CENTER)
	Output.debug("Text: " + string.replace("\n", "\\n"))

def do_clear_screen():
	global canvas
	canvas.delete(ALL)

def call_photo_thread(number):
	"""Tells PhotoThread to take a photo and waits for it to return."""
	Output.debug("This is call_photo_thread().")
	global photo_thread
	global filename_schema
	Output.debug("photo_thread: " + str(photo_thread))
	photo_thread.set_data(filename_schema.format(number), number)
	photo_thread.run()
	while True:
		print "Warte auf photo_taken..."
		if photo_thread.photo_taken:
			break
		time.sleep(0.1)

def do_show_overview():
	"""Displays the 4 pictures on the screen. Uses PhotoLoadThreads and still is pretty slow..."""
	global canvas
	border = 50
	img_size = (h - 3*50) / 2
	canvas.delete(ALL)
	for i in range(4):
		print "Warte auf Nummer " + str(i)
		photo_load_threads()[i].join()
		print "Zeige Photo von Nummer " + str(i)
		photo_load_threads()[i].show_photo(canvas)

def check_things():
	"""Checks for various prerequisites to be fulfilled."""

	# Check the time - if the raspberry has no network connection, it can't get the current
	# time via NTP and it will use January 1st, 1970. We check for this and quit, if this happens.
	if (time.strftime("%Y") == "1970"):
		raise "Current time not set. Please execute 'sudo date -s \"20140726 13:14:55\"' and try again."

	# Kamera
	# USBDevice.find() will raise an error if there is no camera matching CAMERA_ID found.
	USBDevice.find()

	# usbreset
	if (not os.path.isfile("usbreset")):
		raise "'usbreset' not found in the photobooth directory. Compile it by running 'gcc usbreset.c -o usbreset && chmod +x usbreset'."

	# gphoto2
	if (not spawn.find_executable("gphoto2")):
		raise "gphoto2 does not seem to be installed... Try 'sudo apt-get install gphoto2' and try again."

def root(): return root

def init():
	"""Initializes the photo booth."""
	global root, w, h, space, canvas, text, filename_schema, photo_thread, usb_device
	check_things()

	root = Tk()
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.wm_attributes("-topmost", 1)
	root.focus()
	root.focus_force()
	root.geometry("%dx%d+0+0" % (w, h))

	space = (h-4*Settings.IMAGE_SIZE)/5

	canvas = Canvas(root, width=w, height=h, bg="Black")
	canvas.pack()

	text = canvas.create_text(w/2, h/2, text="PhotoBooth v"+Settings.VERSION, fill="red", anchor="c")

	filename_schema = "photos/this-should-not-happen---{}.jpg"

	photo_thread = PhotoThread(w, h)

	GPIO.setup(12, GPIO.IN)

	root.focus_set()
	root.focus_force()
	root.bind("<Q>", quit)
	root.bind("<space>", override_button_press)
	root.after(2000, lambda: Script.start())
	root.mainloop()
