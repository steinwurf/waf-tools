#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the g++ 4.6 cross-compiler for 64 bit Linux
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'gxx_common')
    conf.mkspec_gxx_configure(4, 6, 'crosslinux-gxx46-x64')
    conf.env['CXXFLAGS'] += ['-m64']
