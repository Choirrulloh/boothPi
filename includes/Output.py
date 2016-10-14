import Settings, Display
import time

__output = []

def debug(str):
	__echo(str, "DEBUG ")

def notice(str):
	__echo(str, "NOTICE")

def __echo(str, level):
	str = "{} [{}] {}".format(time.strftime("%d.%m.%y %H:%H:%S"), level, str)
	__output.append(str)
	if Settings.DEBUG:
		Display.display_debug("\n".join(__output[-20:]))
	print str
