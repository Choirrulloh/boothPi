class PhotoLoadThread(threading.Thread):
	def __init__(self, filename, index):
		threading.Thread.__init__(self)
		self.filename = filename
		self.index = index
		self.image = None

	def run(self):
		print "PhotoLoadThread " + str(self.index) + " starting..."
		global images, canvas
		# Load the photo
		print "PhotoLoadThread " + str(self.index) + ": Opening..."
		self.image = Image.open(self.filename)
		print "PhotoLoadThread " + str(self.index) + ": Fitting..."
		self.image = ImageOps.fit(self.image, (IMAGE_SIZE, IMAGE_SIZE))
		print "PhotoLoadThread " + str(self.index) + ": TKing..."
		images[self.index] = ImageTk.PhotoImage(self.image)
		print "PhotoLoadThread " + str(self.index) + " finished."

	def show_photo(self, canvas):
		global w, h, IMAGE_SIZE
		x = 0
		y = 0
		anchor = ""

		if (self.index / 2 == 0):
			anchor = "s"
			y = h/2 - 25
		else:
			anchor = "n"
			y = h/2 + 25

		if (self.index % 2 == 0):
			anchor += "e"
			x = w/2 - 25
		else:
			anchor += "w"
			x = w/2 + 25

		canvas.create_image(x, y, image=images[self.index], anchor=anchor)
		canvas.pack()