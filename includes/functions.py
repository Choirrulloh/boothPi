import time, os, os.path
from distutils import spawn
from Tkinter import *
from RPi import GPIO
from random import randint
import USBDevice, Settings, Script, Output, Display, PhotoThread
#from PhotoThread import *

download_id = None

def quit(some_var):
	"""Beendet die App."""
	global root
	root.destroy()

def button_pressed(some_var=None):
	if Settings.WAIT_FOR_BUTTON_PRESS:
		Settings.WAIT_FOR_BUTTON_PRESS = False
		if Settings.ON_BUTTON_PRESS is not None:
			Output.debug("Button pressed. Running code")
			temp = Settings.ON_BUTTON_PRESS
			Settings.ON_BUTTON_PRESS = None
			try:
				Display.root().after_cancel(Settings.AFTER_ID)
			except Exception as e:
				pass
			temp()
		else:
			Output.debug("Button pressed, but Settings.ON_BUTTON_PRESS is None.")
	else:
		Output.debug("Button pressed, but we are not waiting for this event.")

def start_run(script):
	"""Starts a new run. Is called whenever someone pushes the button (when the script is waiting for it, of course)."""
	global filename_schema
	global download_id
	Settings.runs += 1
	download_id = ''.join(["%s" % randint(0, 9) for num in range(0, 8)])
	filename_schema = time.strftime("photos/%Y%m%d-%H%M%S---" + download_id + "---{}.jpg")
	Output.debug("start_run results: download_id=" + download_id + " filename_schema=" + filename_schema)
	script.next_step()

def call_photo_thread(number, is_temp_photo=False):
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

def init(script_to_run):
	"""Initializes the photo booth."""
	global filename_schema, photo_thread
	check_things()

	filename_schema = "photos/this-should-not-happen---{}.jpg"
	
	Settings.main_script = script_to_run
	
	Settings.runs = 0

	photo_thread = PhotoThread.PhotoThread()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Settings.GPIO, GPIO.IN)
	GPIO.add_event_detect(Settings.GPIO, GPIO.RISING, callback=button_pressed, bouncetime=200)

	Display.init(lambda: script_to_run.start())
