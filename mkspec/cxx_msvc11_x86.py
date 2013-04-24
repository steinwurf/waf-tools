#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the MicroSoft Visual C++ 2012 compiler for 32 bit windows
"""
def configure(conf):
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS  = ['x86']
        conf.mkspec_msvc_configure('11.0')
    else:
        conf.fatal('%s is unsupported for this mkspec.' % conf.get_mkspec_platform())