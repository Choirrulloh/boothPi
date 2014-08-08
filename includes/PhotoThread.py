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

	def set_data(self, filename, number):
		Output.debug("This is PhotoThread.set_data().")
		Output.debug("filename: " + filename)
		Output.debug("number: " + str(number))
		self.filename = filename
		self.number = number
	
	def run(self):
		Output.debug("This is PhotoThread.run().")
		self.photo_taken = False
		# Take the photo
		USBDevice.reset()
		if Settings.SIMULATE_USB_DEVICE:
			Output.debug("Simulation! Using photos/demo_"+str(self.number)+".jpg")
			self.filename="photos/demo_"+str(self.number)+".jpg"
			time.sleep(2)
			self.photo_taken = True
		else:
			command = "gphoto2 --capture-image-and-download --force-overwrite --filename " + self.filename
			Output.notice("Executing: " + command)
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			while True:
				line = process.stdout.readline()
				if line == '':
					break
				if line.startswith("New file is in"):
					self.photo_taken = True

		photo_load_threads()[self.number-1] = PhotoLoadThread(self.filename, self.number-1)
		photo_load_threads()[self.number-1].start()
