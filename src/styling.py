import os, sys, tty, termios
from enum import Enum

# thx https://misc.flogisoft.com/bash/tip_colors_and_formatting
formatting = {
	# Styling
	'BOLD': 1,
	'DIM': 2,
	'UNDERLINED': 4,
	'BLINK': 5,
	'REVERSE': 7,
	'HIDDEN': 8,
	
	# Reset 
	'RESET_ALL': 0,
	'RESET_BOLD': 21,
	'RESET_DIM': 22,
	'RESET_UNDERLINED': 24,
	'RESET_BLINK': 25,
	'RESET_REVERSE': 27,
	'RESET_HIDDEN': 28,
	
	# Colors
	'BLACK': 30,
	'RED': 31,
	'GREEN': 32,
	'YELLOW': 33,
	'BLUE': 34,
	'MAGENTA': 35,
	'CYAN': 36,
	'DARK_GRAY': 90,
	'GRAY': 90,
	'WHITE': 97,
	
	'LIGHT_RED': 91,
	'LIGHT_GREEN': 92,
	'LIGHT_YELLOW': 93,
	'LIGHT_BLUE': 94,
	'LIGHT_MAGENTA': 95,
	'LIGHT_CYAN': 96,
	'LIGHT_GRAY': 37,
	
	# Background
	'BACKGROUND_BLACK': 40,
	'BACKGROUND_RED': 41,
	'BACKGROUND_GREEN': 42,
	'BACKGROUND_YELLOW': 43,
	'BACKGROUND_BLUE': 44,
	'BACKGROUND_MAGENTA': 45,
	'BACKGROUND_CYAN': 46,
	'BACKGROUND_DARK_GRAY': 100,
	'BACKGROUND_GRAY': 100,
	'BACKGROUND_WHITE': 107,
	
	'BACKGROUND_LIGHT_RED': 101,
	'BACKGROUND_LIGHT_GREEN': 102,
	'BACKGROUND_LIGHT_YELLOW': 103,
	'BACKGROUND_LIGHT_BLUE': 104,
	'BACKGROUND_LIGHT_MAGENTA': 105,
	'BACKGROUND_LIGHT_CYAN': 106,
	'BACKGROUND_LIGHT_GRAY': 47,
	
	# Others
	'DEFAULT_FOREGROUND_COLOR': 39,
	'DEFAULT_BACKGROUND_COLOR': 49
}

class Arrow(Enum):
	UP = 1
	DOWN = 2
	RIGHT = 3
	LEFT = 4

# used https://stackoverflow.com/questions/22397289/finding-the-values-of-the-arrow-keys-in-python-why-are-they-triples
class color():
	# Up to three colors
	def setColors(c1 = None, c2 = None, c3 = None):
		out = '\033['
		if(c1 != None): out += str(c1)
		if(c2 != None): out += ';' + str(c2)
		if(c3 != None): out += ';' + str(c3)
		return out + 'm'

class screen():
	@staticmethod
	def clear():
		# TODO: add support for windows and macos
		os.system('clear')
	
	# Important: You need handle allowed characters yourself
	def getChar():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
	
	def getArrow():
		arrow = []
		# KEYBINDS
		chars = [
			115, # s - Search
			113, # q - Exit
			98,  # b - Back
			100  # d - Download
		]
		is_char = False
		is_enter = False
		for i in range(3):
			if is_char or is_enter:
				break
			while True:
				rawChar = screen.getChar()
				actualChar = ord(rawChar)
				if i == 0 and actualChar in chars:
					is_char = True
					break
				if i == 0 and actualChar == 13:
					is_enter = True
					break
				if(i == 0 and actualChar == 27): break
				if(i == 1 and actualChar == 91): break
				if(i == 2 and actualChar >= 65 and actualChar <= 68): break
			arrow.append(actualChar)
		
		arrs = [Arrow.LEFT, Arrow.RIGHT, Arrow.DOWN, Arrow.UP]
		if is_char:
			return rawChar
		elif is_enter:
			return 'enter'
		else:
			return arrs[68-arrow[2]]

	def getControl():
		"""Same as getArrow(), but special for mpv player"""
		arrow = []
		# KEYBINDS
		chars = [
			115, # s     - skip
			113, # q     - quit
			108, # l     - loop
			76,  # L     - loop playlist
			32,  # space - pause
			43,  # +     - raise volume
			45,  # -     - lower volume
			109  # m     - mute
		]
		is_char = False
		is_enter = False # enter - pause
		for i in range(3):
			if is_char or is_enter:
				break
			while True:
				rawChar = screen.getChar()
				actualChar = ord(rawChar)
				if i == 0 and actualChar in chars:
					is_char = True
					break
				if i == 0 and actualChar == 13:
					is_enter = True
					break
				if(i == 0 and actualChar == 27): break
				if(i == 1 and actualChar == 91): break
				if(i == 2 and actualChar >= 65 and actualChar <= 68): break
			arrow.append(actualChar)
		
		arrs = [Arrow.LEFT, Arrow.RIGHT, Arrow.DOWN, Arrow.UP]
		if is_char:
			return rawChar
		elif is_enter:
			return 'enter'
		else:
			return arrs[68-arrow[2]]
		
