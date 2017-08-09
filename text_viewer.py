#! /pkg/qct/software/python/2.7.12/bin/python

import urwid
import utils
import re

class MyText(urwid.Text):
    def __init__(self, text):
        self.__super.__init__(text)
        self._w = urwid.AttrMap(self, None)

    def keypress(self, size, key):
        """allow subclasses to intercept keystrokes"""
        return key

    def mouse_event(self, size, event, button, col, row, focus):
        if (button == 1):
            self.set_text("mao")
        
    def selectable(self):
        return True

class TextViewer:
    def __init__(self, text_list):
        text = self.massage(text_list)
        self.walker = urwid.SimpleListWalker([MyText(line) for line in text])
        self.text = MyListBox(self.walker)

    def gen_text_widget(line):
        pass

    def update_text_list(self, text_list):
        # Using a while loop to remove previous contents
        # because automatic update only supports list functions
        # e.g. pop and append
        while(len(self.walker) > 0):
            self.walker.pop()
        text = self.massage(text_list)
        for line in text:
            self.walker.append(MyText(line))

    def massage(self, text_list):
        result = []
        indent = 0
        for line in text_list:
            res_line = []
            flag = 0
            prev_indent = indent
            for word in utils.SV_START_KEYWORD:
                if(re.search(word, line)):
                    indent = indent + 2
                    flag = flag - 1
            for word in utils.SV_END_KEYWORD:
                if(re.search(word, line)):
                    indent = indent - 2
                    flag = flag + 1
            if(flag > 0):
                res_line.append(indent * ' ')
            else:
                res_line.append(prev_indent * ' ')
            words = line.split(" ")
            for word in words:
                if word in utils.SV_KEYWORDS:
                    res_line.append(('sv_keyword', word + ' '))
                else:
                    res_line.append(word + ' ')
            result.append(res_line)
        return result


class MyListBox(urwid.ListBox):
    # Add custom support for scrolling
    def mouse_event(self, size, event, button, col, row, focus):
        if (button == 4):
            self.keypress(size, 'up')
            self.keypress(size, 'up')
        if (button == 5):
            self.keypress(size, 'down')
            self.keypress(size, 'down')
        return self.__super.mouse_event(size, event, button, col, row, focus)

    def keypress(self, size, key):
        return self.__super.keypress(size, key)
