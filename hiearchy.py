#! /pkg/qct/software/python/2.7.12/bin/python
import urwid
import rtl_reader
from mytreelistbox import myTreeListBox

class FlagFileWidget(urwid.TreeWidget):
    # apply an attribute to the expand/unexpand icons
    unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
        'dirmark')
    expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
        'dirmark')

    def __init__(self, node):
        self.__super.__init__(node)
        # insert an extra AttrWrap for our own use
        self._w = urwid.AttrWrap(self._w, None)
        self.flagged = False
        self.update_w()

    def selectable(self):
        return True

    def keypress(self, size, key):
        """allow subclasses to intercept keystrokes"""
        key = self.__super.keypress(size, key)
        if key:
            key = self.unhandled_keys(size, key)
        return key

    def unhandled_keys(self, size, key):
        """
        Override this method to intercept keystrokes in subclasses.
        Default behavior: Toggle flagged on space, ignore other keys.
        """
        if key == " ":
            self.flagged = not self.flagged
            self.update_w()
        else:
            return key

    def update_w(self):
        """Update the attributes of self.widget based on self.flagged.
        """
        if self.flagged:
            self._w.attr = 'flagged'
            self._w.focus_attr = 'flagged focus'
        else:
            self._w.attr = 'body'
            self._w.focus_attr = 'focus'

class ModuleNodeWidget(FlagFileWidget):
    """Widget for a directory."""
    def __init__(self, node, leafnode=False):
        self.leafnode = leafnode
        self.__super.__init__(node)
        if not leafnode:
            self.expanded = (node.depth == 0)
            self.update_expanded_icon()

    def get_display_text(self):
        if not self.leafnode:
            return self.get_node().get_key()
        else:
            return "  " + self.get_node().get_key()

class HierachyLeafNode(urwid.TreeNode):
    """Metadata storage for directories"""

    def __init__(self, module, key='', parent=None, depth=0):
        self.module = module
        self.depth = depth
        urwid.TreeNode.__init__(
            self, module.name, key=key, parent=parent, depth=depth)

    def load_widget(self):
        return ModuleNodeWidget(self, leafnode=True)

class HierachyNode(urwid.ParentNode):
    """Metadata storage for directories"""

    def __init__(self, module, key='', parent=None, depth=0):
        self.module = module
        self.depth = depth
        urwid.ParentNode.__init__(
            self, module.name, key=key, parent=parent, depth=depth)

    def load_child_keys(self):
        return sorted(self.module.sub_modules.keys())

    def load_child_node(self, key):
        child_node = self.module.sub_modules[key]
        if (len(child_node.sub_modules) == 0):
            return HierachyLeafNode(child_node, key, self, self.depth+1)
        else:
            return HierachyNode(child_node, key, self, self.depth+1)

    def load_widget(self):
        return ModuleNodeWidget(self)

class HierachyBrowser:
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


    def __init__(self):
        self.top = rtl_reader.main()
        self.top_name = rtl_reader.get_top_name()
        self.header = urwid.AttrWrap(urwid.Text(""), 'head')
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')
        self.listbox = myTreeListBox(urwid.TreeWalker(HierachyNode(self.top, self.top_name)))
        self.listbox.offset_rows = 1
        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=self.header,
            footer=self.footer)

    def main(self):
        """Run the program."""
        self.loop = urwid.MainLoop(
            self.view, self.palette, unhandled_input=self.unhandled_input)
        self.loop.run()

    def unhandled_input(self, k):
        # update display of focus directory
        if k in ('q','Q'):
            raise urwid.ExitMainLoop()


def main():
    HierachyBrowser().main()


if __name__=="__main__":
    main()