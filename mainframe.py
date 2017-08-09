#! /pkg/qct/software/python/2.7.12/bin/python

import urwid
from hierarchy_browser import HierarchyBrowser
from text_viewer import TextViewer

def main_loop(top, top_name):
    palette = [
        ('body'         , 'white'             , 'black'),
        ('flagged'      , 'black'             , 'dark green'),
        ('focus'        , 'light gray'        , 'dark blue'),
        ('flagged focus', 'yellow'            , 'dark cyan'),
        ('head'         , 'white, bold'       , 'dark blue'),
        ('sv_keyword'   , 'yellow, bold'      , 'black'),
        ('foot'         , 'white'             , 'dark blue'), 
        ('key'          , 'white, underline'  , 'dark blue'),
        ('title'        , 'white, bold'       , 'dark blue'),
        ('dirmark'      , 'black, bold'       , 'dark cyan'),
        ('flag'         , 'dark gray'         , 'black'),
        ('error'        , 'dark red'          , 'black'),
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

    vline = urwid.AttrMap( urwid.SolidFill(u'\u2502'), 'line')
    hb = HierarchyBrowser(top, top_name)
    tv = TextViewer(top.raw_text)

    hb.set_text_viewer(tv)
    
    header = urwid.AttrMap(urwid.Text("RTL Browser"), 'head')
    footer = urwid.AttrMap(urwid.Edit(footer_text), 'foot')
    
    columns = urwid.Columns([
        ('weight', 3, tv.text), 
        ('fixed', 1, vline), 
        ('weight', 2, hb.listbox)],
        dividechars=1, focus_column=0)

    view = urwid.Frame(
        urwid.AttrMap(columns, 'body'),
        header=header,
        footer=footer)

    def unhandled_input(k):
        # update display of focus directory
        if k in ('q','Q'):
            raise urwid.ExitMainLoop()

    def input_filter(keys, raw):
        return keys

    """Run the program."""
    main_loop = urwid.MainLoop(
        view, 
        palette, 
        unhandled_input = unhandled_input,
        input_filter = input_filter)
    main_loop.run()



    


