#! /pkg/qct/software/python/2.7.12/bin/python

from sv_parser import SystemVerilogParser
import mainframe as mf

def main():
    filename = '/usr2/zyao/scripts/noc_rtl_reader/test/smmucfg_noc/test'
    top_name = 'smmucfg_noc'
    parser = SystemVerilogParser(top_name, filename)
    mf.main_loop(parser.get_root_module(), top_name)

if __name__=="__main__":
    main()