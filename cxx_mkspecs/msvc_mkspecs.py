#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

from . import msvc_common


@conf
def cxx_msvc12_x64(conf):
    """
    Detect and setup the Microsoft Visual C++ 2013 compiler for 64-bit windows
    """
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS = ['x86_amd64']
        conf.mkspec_msvc_configure('12.0')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_msvc12_x86(conf):
    """
    Detect and setup the Microsoft Visual C++ 2013 compiler for 32-bit windows
    """
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS = ['x86']
        conf.mkspec_msvc_configure('12.0')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_msvc14_x64(conf):
    """
    Detect and setup the Microsoft Visual C++ 2015 compiler for 64-bit
    """
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS = ['x86_amd64']
        conf.mkspec_msvc_configure('14.0')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_msvc14_x86(conf):
    """
    Detect and setup the Microsoft Visual C++ 2015 compiler for 32-bit
    """
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS = ['x86']
        conf.mkspec_msvc_configure('14.0')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_msvc15_x64(conf):
    """
    Detect and setup the Microsoft Visual C++ 2017 compiler for 64-bit
    """
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS = ['x64', 'x86_amd64']
        conf.mkspec_msvc_configure('15.8')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_msvc15_x86(conf):
    """
    Detect and setup the Microsoft Visual C++ 2017 compiler for 32-bit
    """
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_TARGETS = ['x86', 'amd64_x86']
        conf.mkspec_msvc_configure('15.8')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))
