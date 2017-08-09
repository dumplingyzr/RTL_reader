#! /pkg/qct/software/python/2.7.12/bin/python
from sets import Set

# SystemVerilog keywords for intentation regular expression matching
SV_START_KEYWORD = ["\\bclass\\b", "\\bfunction\\b", "\\bbegin\\b", "\\btask\\b", 
                    "\(", "\{", "\\bcase\\b", "\\bfork\\b", "\\bmodule\\b"]
SV_END_KEYWORD = ["\\bendclass\\b", "\\bendfunction\\b", "\\bend\\b", "\\bendtask\\b", 
                  "\}", "\)", "\\bendcase\\b", "\\bjoin\\b", "\\bjoin_any\\b", 
                  "\\bjoin_none\\b", "\\bendmodule\\b"]
SV_KEYWORDS = Set(["always", "ifnone",  "rpmos", "and", "initial", "rtran", "assign", 
                   "inout", "rtranif0", "begin", "input", "rtranif1", "buf", "integer", 
                   "scalared", "bufif0", "join", "small", "bufif1", "large", "specify", 
                   "case", "macromodule", "specparam", "casex", "medium", "strong0", 
                   "casez", "module", "strong1", "cmos", "nand", "supply0", "deassign", 
                   "negedge", "supply1", "default", "nmos", "table", "defparam", "nor", 
                   "task", "disable", "not", "time", "edge", "notif0", "tran", "else", 
                   "notif1", "tranif0", "end", "or", "tranif1", "endcase", "output", 
                   "tri", "endmodule", "parameter", "tri0", "endfunction", "pmos", 
                   "tri1", "endprimitive", "posedge", "triand", "endspecify", "primitive", 
                   "trior", "endtable", "pull0", "trireg", "endtask", "pull1", "vectored", 
                   "event", "pullup", "wait", "for", "pulldown", "wand", "force", "rcmos", 
                   "weak0", "forever", "real", "weak1", "fork", "realtime", "while", 
                   "function", "reg", "wire", "highz0", "release", "wor", "highz1", 
                   "repeat", "xnor", "if", "rnmos", "xor"])