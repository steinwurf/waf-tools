#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the MicroSoft Visual C++ 2010 compiler for 32 bit windows
"""
def configure(conf):
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_VERSIONS = ['msvc 10.0']
        conf.env.MSVC_TARGETS  = ['x86']
        conf.load('msvc')
        conf.mkspec_set_msvc_flags()
    else:
        conf.fatal('%s is unsupported for this mkspec.' % conf.get_mkspec_platform())
