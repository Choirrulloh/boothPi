import Settings

__output = []

def debug(str):
	if Settings.DEBUG:
		__echo(str)

def notice(str):
	__echo(str)

def __echo(str):
	__output.append(str)
	print str
