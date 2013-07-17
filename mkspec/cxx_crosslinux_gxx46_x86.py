#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the g++ 4.6 cross-compiler for 32 bit Linux
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'gxx_common')
    conf.mkspec_gxx_toolchain_configure('crosslinux-gxx46-x86', 4, 6)
    conf.env['CXXFLAGS'] += ['-m32']
