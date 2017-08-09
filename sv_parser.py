#! /pkg/qct/software/python/2.7.12/bin/python

import re

class SystemVerilogParser(object):
    def __init__(self, top_name, filename):
        self.modules = {}
        self.top_name = top_name
        self.filename = filename
        self.root_module = None
        self._main()

    def get_root_module(self):
        return self.root_module

    def _main(self):
        f = open(self.filename)
        module_raw = []
        push_line = 0
        flag = 0
        for line in f:
            (line, flag) = self._preprocess(line, flag)
            m_module = re.search('module', line)
            m_endmodule = re.search('endmodule', line)
            if m_module:
                push_line = 1
            if m_endmodule:
                push_line = 0
                module_raw.append(line)
                #module = self._gen_module(' '.join(module_raw))
                module = self._gen_module(module_raw)
                if (module.name == self.top_name):
                    self.root_module = module
                self.modules[module.name] = module
                module_raw = []
            if (push_line == 1):
                module_raw.append(line)
    
        self._gen_hierachy(self.root_module)
        
    def _preprocess(self, line, flag):
        # in a /*...*/ segment
        if(flag == 1):  
            m = re.match('^.*\*/(.*)', line)
            if m:
                line = m.group(1)
                flag = 0
            else:
                return ('', 1)
        else:
            m = re.match('(^.*)/\*.*', line)
            if m:
                line = m.group(1)
                flag = 1
        # Remove comments
        result = re.sub('//.*', '', line)
        # Remove leading and trailing spaces
        result = re.sub('^\s*', '', result)
        result = re.sub('\s*$', '', result)
        # Remove consecutive spaces
        result = re.sub('\s+', ' ', result)
        #print(result)
        return (result, flag)
    
    def _gen_module(self, raw):
        #lines = raw.split(';')
        lines = raw
        # Get module name from first statement
        m = re.search('module (\w+)', lines[0])
        module = SystemVerilogModule(m.group(1))
        for line in lines[1:]:
            (line, flag) = self._preprocess(line, 0)
            if(re.match('input|output|inout|wire|reg|logic',line)):
                m_signal = re.match('(\w+).*\s(\w+)',line)
                if m_signal:
                    category = m_signal.group(1)
                    name = m_signal.group(2)
                    module.add_signal(SystemVerilogSignal(name, 1, category))
        module.raw_text = raw
        return module
    
    def _gen_hierachy(self, root):
        if root.sub_modules:
            return
        #lines = root.raw_text.split(';')
        lines = root.raw_text
        for line in lines:
            (line, flag) = self._preprocess(line, 0)
            m = re.match('^(\w+)\s(\w+)\($',line)
            if m:
                module_name = m.group(1)
                inst_name = m.group(2)
                if(module_name in self.modules):
                    root.add_sub_module(self.modules[module_name],inst_name)
    
        for child in root.sub_modules.values():
            self._gen_hierachy(child)

class SystemVerilogModule(object):
    """Systemverilog module object

    Attributes:
        name: module name
        signals: signal list
        sub_modules: modules instantiated within current module
        raw_text: full sv text of current module
    """
    def __init__(self, name):
        self.name = name
        self.raw_text = []
        self.signals = []
        self.sub_modules = {}
    def add_signal(self, signal):
        self.signals.append(signal)
    def add_sub_module(self, module, inst_name):
        self.sub_modules[inst_name] = module

class SystemVerilogSignal(object):
    """Systemverilog signal object

    Attributes:
        name: signal name
        width: signal width
        category: signal type [input,output,inout,reg,wire,logic]
    """
    def __init__(self, name, width, category):
        self.name = name
        self.width = width
        self.category = category

