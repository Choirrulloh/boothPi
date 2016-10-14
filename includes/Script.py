import Settings, Output, Display, functions

class Script:
	def __init__(self):
		self.lines = []
		self.line = 0
		
	def show_text(self, text, delay=1000, branch_on_keypress=None):
		self.lines.append([delay, "text", text, branch_on_keypress])

	def take_photo(self, index):
		self.lines.append([1, "photo", index, None])

	def show_overview(self, delay, branch_on_keypress=None):
		self.lines.append([delay, "overview", None, branch_on_keypress])

	def clear_screen(self):
		self.lines.append([1, "clear", None, None])

	def wait_for_button_press(self):
		self.lines.append([1, "wait", None, None])

	def countdown(self, start, end, delay=1000, branch_on_keypress=None, additional_text=""):
		if additional_text!="": additional_text+="\n"
		if (end > start):
			raise "countdown has to go from a large number to a smaller number."
		for number in range(start, end-1, -1):
			self.lines.append([delay, "text", additional_text + str(number), branch_on_keypress])
	
	def branch(self, target):
		self.lines.append([1, "branch", None, target])
	
	def init_run(self):
		self.lines.append([1, "init_run", None, None])

	def start(self):
		Display.clear()
		self.line = 0
		self.next_step()

	def next_step(self):
		Settings.WAIT_FOR_BUTTON_PRESS = False
		Settings.AFTER_ID = None
		delay, command, additional, target_branch = self.lines[self.line]
		self.line += 1
		if self.line>=len(self.lines):
			self.line = 0

		if command=="text":
			if target_branch is not None:
				Settings.ON_BUTTON_PRESS = lambda: target_branch.start()
				Settings.WAIT_FOR_BUTTON_PRESS = True
			Display.display_text(additional)
		elif command=="photo":
			Output.debug("Photo! Number " + str(additional))
			functions.call_photo_thread(additional)
		elif command=="overview":
			if target_branch is not None:
				Settings.ON_BUTTON_PRESS = lambda: target_branch.start()
				Settings.WAIT_FOR_BUTTON_PRESS = True
			Display.show_overview()
		elif command=="clear":
			Display.clear()
		elif command=="branch":
			Display.root().after(delay, lambda: target_branch.start())
			return
		elif command=="wait":
			Settings.ON_BUTTON_PRESS = self.next_step
			Settings.WAIT_FOR_BUTTON_PRESS = True
			return
		elif command=="init_run":
			functions.start_run(self)
			return

		# check if the next command is a "photo"
		if self.lines[self.line][1]=="photo":
			delay = max(delay - Settings.PHOTO_DELAY, 1)

		if Settings.DEBUG_SHORT_DELAYS:
			delay = delay / 100 + 1
			
		#Output.debug("Waiting: " + str(delay))

		Settings.AFTER_ID = Display.root().after(delay, self.next_step)
