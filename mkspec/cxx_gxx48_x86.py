#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the g++ 4.8 compiler for 32 bit
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'gxx_common')
    conf.mkspec_gxx_configure(4,8)
    conf.env['CXXFLAGS'] += ['-m32']
