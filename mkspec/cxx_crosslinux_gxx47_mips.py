#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the g++ 4.7 cross-compiler for MIPS 32 bit Linux
"""
def configure(conf):

    conf.load_external_tool('mkspec_common', 'gxx_common')
    conf.mkspec_gxx_configure(4, 7, 'crosslinux-gxx47-mips')

    # Statically link in the C++ standard library
    conf.env['LINKFLAGS'] = '-static-libstdc++'


