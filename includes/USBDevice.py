import subprocess, re, os, sys
import Settings
import Output

__path = None

def find():
	"""Returns the USB port address of the camera."""
	global __path
	Output.debug("In USBDevice.find()")
	if Settings.SIMULATE_USB_DEVICE:
		__path = "/dev/bus/usb/042/023"
		Output.debug("Simulation! Pretending the device is " + __path + ".")
		return __path
	result = subprocess.Popen("gphoto2 --auto-detect", stdout=subprocess.PIPE, shell=True).stdout.read()
	Output.debug("Result of `gphoto2 --auto-detect`: " + result)
	match = re.compile("(?P<camera>[^\n]+?) +usb:(?P<device>[0-9]{3}),(?P<port>[0-9]{3})",re.MULTILINE).search(result)
	if match != None:
		Output.notice("Found camera: " + match.group('camera') + " on USB port " + match.group('device') + "," + match.group('port'))
		__path = "/dev/bus/usb/" + match.group('device') + "/" + match.group('port')
		Output.notice("Path is now: " + __path)
		return __path
	raise "Camera not found. Connect it to the Pi, switch it on and verify that `gphoto2 --auto-detect` finds it."

def get_path():
	if __path:
		return __path
	else:
		return find()

def reset():
	"""Calls usbreset to reset the USB port."""
	Output.debug("In USBDevice.reset()")
	if Settings.SIMULATE_USB_DEVICE:
		Output.debug("Simulation. Resetting nothing.")
		return
	cmd = os.path.abspath(os.path.dirname(sys.argv[0])) + "/usbreset " + get_path()
	Output.debug("Executing: " + cmd)
	subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).stdout.read()
