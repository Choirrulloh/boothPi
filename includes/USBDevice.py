import subprocess, re
import Settings

__path = None

def find():
	"""Returns the USB port address of the USB device given in CAMERA_ID."""
	print "In USBDevice.find()"
	global __path
	result = subprocess.Popen("lsusb", stdout=subprocess.PIPE).stdout.read()
	match = re.search("Bus (\d{3}) Device (\d{3}): ID " + Settings.CAMERA_ID, result)
	if match != None:
		__path = "/dev/bus/usb/" + match.group(1) + "/" + match.group(2)
		print "Path to USB device: " + __path
		return __path
	raise "USB Device " + Settings.CAMERA_ID + " not found! Check your camera's ID with 'lsusb' and modify CAMERA_ID in photobooth.py."

def get_path():
	if __path:
		return __path
	else:
		return find()

def reset():
	"""Calls usbreset to reset the USB port."""
	print "In USBDevice.reset()"
	cmd = os.path.abspath(os.path.dirname(sys.argv[0])) + "/usbreset " + get_path()
	print "Executing: " + cmd
	subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).stdout.read()
