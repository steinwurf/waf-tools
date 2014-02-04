#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

import msvc_common

"""
Detect and setup the Microsoft Visual C++ 2012 compiler for 64-bit windows
"""
@conf
def cxx_msvc11_x64(conf):
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS  = ['x86_amd64']
        conf.mkspec_msvc_configure('11.0')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
                    conf.get_mkspec_platform()))

"""
Detect and setup the Microsoft Visual C++ 2012 compiler for 32-bit windows
"""
@conf
def cxx_msvc11_x86(conf):
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS  = ['x86']
        conf.mkspec_msvc_configure('11.0')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
                    conf.get_mkspec_platform()))

"""
Detect and setup the Microsoft Visual C++ 2013 compiler for 64-bit windows
"""
@conf
def cxx_msvc12_x64(conf):
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS  = ['x86_amd64']
        conf.mkspec_msvc_configure('12.0')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
                    conf.get_mkspec_platform()))

"""
Detect and setup the Microsoft Visual C++ 2013 compiler for 32-bit windows
"""
@conf
def cxx_msvc12_x86(conf):
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS  = ['x86']
        conf.mkspec_msvc_configure('12.0')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
                    conf.get_mkspec_platform()))