#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the g++ 4.6 compiler for 32 bit linux
"""
def configure(conf):
    if conf.is_mkspec_platform('linux'):
        conf.load('gxx')
        conf.find_program("g++-4.6", var='CXX')
        conf.add_gcc_default_flags()
        conf.env['CXXFLAGS'] += ['-m32']
    else:
        conf.fatal('%s is unsupported for this mkspec.' % conf.get_mkspec_platform())