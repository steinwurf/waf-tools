#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the g++ 4.5.4 MacPorts compiler for 64 bit
"""
def configure(conf):
    conf.load('gxx')
    if conf.is_mkspec_platform('mac'):
        conf.find_program("g++-mp-4.5.4", var='CXX')
        
    elif conf.is_mkspec_platform('linux'):
        conf.find_program("g++-4.5.4", var='CXX')
    else:
        conf.fatal('%s is unsupported for this mkspec.' % conf.get_mkspec_platform())    
    conf.add_gcc_default_flags()
    conf.env['CXXFLAGS'] += ['-m64']