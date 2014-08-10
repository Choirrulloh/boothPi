from threading import Thread
import Settings, Output, Display
import Image, ImageTk, ImageOps

__images = [None, None, None, None]

def images(): return __images

class PhotoLoadThread(Thread):
	def __init__(self, filename, index):
		Thread.__init__(self)
		self.filename = filename
		self.index = index
		self.image = None

	def run(self):
		Output.debug("PhotoLoadThread " + str(self.index) + " starting...")
		# Load the photo
		Output.debug("PhotoLoadThread " + str(self.index) + ": Opening...")
		self.image = Image.open(self.filename)
		Output.debug("PhotoLoadThread " + str(self.index) + ": Fitting...")
		self.image = ImageOps.fit(self.image, (Display.image_size(), Display.image_size()))
		Output.debug("PhotoLoadThread " + str(self.index) + ": TKing...")
		images()[self.index] = ImageTk.PhotoImage(self.image)
		Output.debug("PhotoLoadThread " + str(self.index) + " finished.")

	def get_photo(self):
		return images()[self.index]

