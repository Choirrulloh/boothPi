import time, os.path
from distutils import spawn
from Tkinter import *
from RPi import GPIO
import USBDevice, Settings, Script, Output, Display, PhotoThread
#from PhotoThread import *

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
		Display.root().after(5, check_button_pressed)

def start_run():
	"""Starts a new run. Is called whenever someone pushes the button (when the script is waiting for it, of course)."""
	global filename_schema
	global canvas
	global width, space
	filename_schema = time.strftime("photos/%Y%m%d-%H%M%S---{}.jpg")
	Script.next_step()

def call_photo_thread(number):
	"""Tells PhotoThread to take a photo and waits for it to return."""
	Output.debug("This is call_photo_thread().")
	global photo_thread
	global filename_schema
	Output.debug("photo_thread: " + str(photo_thread))
	photo_thread.set_data(filename_schema.format(number), number)
	photo_thread.run()
	while True:
		Output.debug("Warte auf photo_taken...")
		if photo_thread.photo_taken:
			break
		time.sleep(0.1)

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
	global filename_schema, photo_thread
	check_things()

	filename_schema = "photos/this-should-not-happen---{}.jpg"

	photo_thread = PhotoThread.PhotoThread()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(12, GPIO.IN)

	Display.init(lambda: Script.start())
