#! /pkg/qct/software/python/2.7.12/bin/python

import urwid

#Self defined TreeListBox class enabling mouse scrolls
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

class HierarchyLeafNode(urwid.TreeNode):
    """Metadata storage for directories"""

    def __init__(self, module, key='', parent=None, depth=0):
        self.module = module
        self.depth = depth
        urwid.TreeNode.__init__(
            self, module.name, key=key, parent=parent, depth=depth)

    def load_widget(self):
        return ModuleNodeWidget(self, leafnode=True)

class HierarchyNode(urwid.ParentNode):
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
            return HierarchyLeafNode(child_node, key, self, self.depth+1)
        else:
            return HierarchyNode(child_node, key, self, self.depth+1)

    def load_widget(self):
        return ModuleNodeWidget(self)

class HierarchyBrowser:
    def __init__(self, top, top_name):
        self.listbox = myTreeListBox(urwid.TreeWalker(HierarchyNode(top, top_name)))
        self.listbox.offset_rows = 1

