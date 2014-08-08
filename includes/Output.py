import Settings, Display

__output = []

def debug(str):
	if Settings.DEBUG:
		__echo(str)

def notice(str):
	__echo(str)

def __echo(str):
	__output.append(str)
	if Settings.DEBUG:
		Display.display_debug("\n".join(__output[-20:]))
	print str
