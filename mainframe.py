#! /pkg/qct/software/python/2.7.12/bin/python

import urwid
from hierarchy_browser import HierarchyBrowser

class MainFrame:
    palette = [
        ('body'         , 'black'     , 'light gray'),
        ('flagged'      , 'black'     , 'dark green', ('bold','underline')),
        ('focus'        , 'light gray', 'dark blue' , ('standout')),
        ('flagged focus', 'yellow'    , 'dark cyan' , ('bold','standout','underline')),
        ('head'         , 'yellow'    , 'black'     , ('standout')),
        ('foot'         , 'light gray', 'black'), 
        ('key'          , 'light cyan', 'black'     , ('underline')),
        ('title'        , 'white'     , 'black'     , ('bold')),
        ('dirmark'      , 'black'     , 'dark cyan' , ('bold')),
        ('flag'         , 'dark gray' , 'light gray'),
        ('error'        , 'dark red'  , 'light gray'),
        ]

    footer_text = [
        ('title', "RTL Browser"), "    ",
        ('key', "UP"), ",", ('key', "DOWN"), ",",
        ('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
        "  ",
        ('key', "SPACE"), "  ",
        ('key', "+"), ",",
        ('key', "-"), "  ",
        ('key', "LEFT"), "  ",
        ('key', "HOME"), "  ",
        ('key', "END"), "  ",
        ('key', "Q"),
        ]

    def __init__(self, top, top_name):

        vline = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        hb = HierarchyBrowser(top, top_name)
        
        header = urwid.AttrWrap(urwid.Text(""), 'head')
        footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')
        
        columns = urwid.Columns([
            ('weight', 3, hb.listbox), 
            ('fixed', 1, vline), 
            ('weight', 2, hb.listbox)],
            dividechars=1, focus_column=2)

        self.view = urwid.Frame(
            urwid.AttrWrap(columns, 'body'),
            header=header,
            footer=footer)
        

    def main(self):
        """Run the program."""
        self.loop = urwid.MainLoop(
            self.view, self.palette, unhandled_input=self.unhandled_input)
        self.loop.run()

    def unhandled_input(self, k):
        # update display of focus directory
        if k in ('q','Q'):
            raise urwid.ExitMainLoop()

