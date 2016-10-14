from threading import Thread
import time, subprocess
import Output, USBDevice, Settings
from PhotoLoadThread import PhotoLoadThread

__photo_load_thread_array = [None, None, None, None]

def photo_load_threads(): return __photo_load_thread_array

class PhotoThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.photo_taken = False

	def set_data(self, filename, number, fullsize=False):
		Output.debug("This is PhotoThread.set_data().")
		Output.debug("filename: " + filename)
		Output.debug("number: " + str(number))
		self.filename = filename
		self.number = number
		self.fullsize = fullsize
	
	def run(self):
		Output.debug("This is PhotoThread.run().")
		self.photo_taken = False
		# Take the photo
		USBDevice.reset()
		if Settings.SIMULATE_USB_DEVICE:
			Output.debug("Simulation! Using includes/demo_"+str(self.number)+".jpg")
			self.filename="includes/demo_"+str(self.number)+".jpg"
			time.sleep(2)
		else:
			command = "gphoto2 --capture-image-and-download --force-overwrite --filename " + self.filename
			Output.notice("Executing: " + command)
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			while True:
				line = process.stdout.readline()
				if line.startswith("New file is in"):
					break
		photo_load_threads()[self.number-1] = PhotoLoadThread(self.filename, self.number-1, fullsize=self.fullsize)
		photo_load_threads()[self.number-1].start()
		self.photo_taken = True
