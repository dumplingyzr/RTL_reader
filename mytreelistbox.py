#! /pkg/qct/software/python/2.7.12/bin/python
import urwid

class myTreeListBox(urwid.TreeListBox):

	def mouse_event(self, size, event, button, col, row, focus):
		if (button == 4):
			self.keypress(size, 'up')
		if (button == 5):
			self.keypress(size, 'down')
		if(self.__super.mouse_event(size, event, button, col, row, focus) == False):
			if (button == 1):
				self.keypress(size, '+')

	def keypress(self, size, key):
		key = self.__super.keypress(size, key)
		return self.unhandled_input(size, key)